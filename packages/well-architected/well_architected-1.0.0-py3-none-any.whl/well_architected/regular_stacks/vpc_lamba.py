'''Create A VPC Based Lambda with
    - Security Group with inbound/outbound rules to Target Security Groups
    - SNS Topic for failed invocations
'''
import aws_cdk

from aws_cdk import Duration, RemovalPolicy
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_ec2 import Vpc, SubnetSelection, Subnet
from aws_cdk.aws_ssm import StringParameter
from aws_cdk.aws_events import Rule, EventPattern, Schedule
from aws_cdk.aws_events_targets import LambdaFunction
from aws_cdk.aws_lambda_event_sources import DynamoEventSource
from aws_cdk.aws_lambda_destinations import SnsDestination
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_dynamodb import (
    Table, Attribute, AttributeType, StreamViewType, BillingMode
)
from aws_cdk.aws_lambda import (
    Function, Runtime, S3Code, StartingPosition, LayerVersion
)
from python.cdk.iam.policies import Policies
from python.cdk.iam.roles import IAMRole
from python.cdk.ec2.security_group import TwoWaySecurityGroup


class VPCLambda(aws_cdk.Stack):

    def __init__(
        self, scope, id,
        function_name=None,
        devops_bucket=None,
        layers=None,
        target_security_groups=None,
        subnet_ids=None,
        email_addresses=None,
        topic_name=None,
        retries=0,
        memory_size=128,
        duration=1,
        environment_variables=None,
        vpc_id=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.function_name = function_name
        self.create_role(f"{function_name}_role")
        self.get_vpc()
        self.get_s3_bucket(devops_bucket)

        self.lambda_function = Function(
            self, self.function_name,
            code=self.get_s3_package(f'lambda_functions/{self.function_name}'),
            function_name=self.function_name,
            handler=f"{self.function_name}.handler",
            layers=self.create_layers(layers),
            timeout=Duration.minutes(duration),
            runtime=Runtime.PYTHON_3_9,
            retry_attempts=retries,
            memory_size=memory_size,
            role=self.role,
            security_groups=self.create_security_group(target_security_groups),
            vpc=self.vpc,
            vpc_subnets=self.get_subnets(subnet_ids),
            environment=environment_variables,
            #on_failure=self.get_sns_destination(
            #    email_addresses=email_addresses,
            #    topic_name=topic_name if topic_name else self.function_name,
            #),
        )
        #self.sns_topic.grant_publish(self.lambda_function)

    def create_security_group(self, target_security_groups):
        '''Return Security Group with outbound and inbound rules to target_security_groups'''
        return [
            TwoWaySecurityGroup(
                self, "LambdaSecurityGroup",
                security_group_name=f'lambda-{self.function_name}',
                target_security_groups=target_security_groups,
            ).security_group
        ]

    def get_subnets(self, subnet_ids):
        '''Return SubnetSelection object from given subnet_ids or None'''
        try:
            return SubnetSelection(
                subnets=[
                    Subnet.from_subnet_id(self, subnet_id,
                        subnet_id=subnet_id
                    ) for subnet_id in subnet_ids
                ]
            )
        except TypeError:
            return

    def get_vpc(self):
        '''Return VPC object from vpc_id lookup
           requires credentials to work properly
           use create_cdk_context.py to bypass this
        '''
        self.vpc = Vpc.from_lookup(
            self, "VPC",
            vpc_id=self.node.try_get_context('vpc_id'),
            is_default=False
        )

    def get_s3_bucket(self, devops_bucket):
        '''Return Bucket object from looking up devops_bucket'''
        self.bucket = Bucket.from_bucket_name(
            self, "S3Bucket",
            bucket_name=devops_bucket,
        )

    def managed_policies(self):
        '''Return default managed policy names for VPC based Lambda functions'''
        return (
            "CloudWatchAgentServerPolicy",
            "service-role/AWSLambdaVPCAccessExecutionRole",
        )

    def get_managed_policies(self):
        '''Return Managed Policy Objects from managed policies list'''
        return [
            ManagedPolicy.from_aws_managed_policy_name(name)
            for name in self.managed_policies()
        ]

    def add_managed_policy_to_role(self, *policy_names):
        '''Update Lambda Function Role with given Managed Policies'''
        for policy_name in policy_names:
            self.role.add_managed_policy(
                ManagedPolicy.from_aws_managed_policy_name(policy_name)
            )
        return self

    def add_customer_managed_policy_to_role(self, *policy_names):
        '''Update Lambda Function Role with given Customer Managed Policies'''
        for policy_name in policy_names:
            self.role.add_managed_policy(
                ManagedPolicy.from_managed_policy_name(policy_name)
            )
        return self

    def create_role(self, role_name):
        '''Create Required Role for Lambda Function'''
        # self.role = IAMRole(
        #     role_name=role_name,
        #     assumed_by='lambda',
        #     managed_policies=self.managed_policies(),
        # ).role
        self.role = Role(
            self, role_name,
            assumed_by=ServicePrincipal("lambda.amazonaws.com"),
            description=role_name,
            managed_policies=self.get_managed_policies(),
            # role_name=role_name,
        )
        StringParameter(
            self, "RoleParameter",
            description=role_name,
            parameter_name=role_name,
            string_value=self.role.role_arn,
        )

    def add_ssm_permissions(self):
        '''[optional] Add SSM Permissions to the Lambda Function Role'''
        self.add_managed_policy_to_role("service-role/AmazonSSMAutomationRole")
        self.role.assume_role_policy.add_statements(
            Policies.trust_policy(ServicePrincipal("ssm.amazonaws.com"))
        )
        self.role.add_to_policy(Policies.ssm_get_parameter_policy())
        return self

    def add_policy_to_role(self, *policy_statements):
        '''[optional] Add Custom Policy Statements to Lambda Function Role'''
        for policy_statement in policy_statements:
            self.role.add_to_policy(policy_statement)
        return self

    def get_s3_package(self, filename):
        '''Return Code object referencing location of packaged Lambda Function Code'''
        return S3Code(self.bucket, f'{filename}.zip')

    def add_s3_notification_resource_policy(self, source_account=None, source_bucket=None):
        '''[optional] Add permissions for an S3 object to Invoke this Lambda Function'''
        self.lambda_function.add_permission(
            "ResourcePolicy",
            principal=ServicePrincipal("s3.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_account=source_account,
            source_arn=f"arn:aws:s3:::{source_bucket}"
        )
        return self

    def create_event_bridge_rule(self, rule_name=None, event_pattern=None):
        '''[optional] Add EventPattern to Invoke this Lambda Function'''
        return Rule(
            self, rule_name,
            description=f'Invoke {self.lambda_function.function_name} to {rule_name}',
            enabled=True,
            targets=[LambdaFunction(self.lambda_function)],
            event_pattern=event_pattern
        )

    def add_ssm_event_rule(self, rule_name="LogSystemsManagerAutomationEvents", prefix=None):
        '''[optional] Add EventPattern for Systems Manager Automation Events to Invoke this Lambda Function based on the given prefix

            :params rule_name
            :params prefix
        '''
        self.create_event_bridge_rule(
            rule_name=rule_name,
            event_pattern=EventPattern(
                source=["aws.ssm"],
                detail_type=[
                    "EC2 Automation Step Status-change Notification",
                    "EC2 Automation Execution Status-change Notification"
                ],
                detail=dict(
                    Definition=[
                        dict(
                            prefix=prefix
                        )
                    ]
                )
            )
        )
        return self

    def add_storage_gateway_rule(
        self, rule_name="LogStorageGatewayRefreshComplete",
        prefix=None, storage_gateway_account=None
    ):
        '''[optional] Add EventPattern for StorageGateway Refresh Cache events to Invoke this Lambda Function based on the given prefix

            :params rule_name
            :params prefix
        '''
        self.create_event_bridge_rule(
            rule_name=rule_name,
            event_pattern=EventPattern(
                account=[storage_gateway_account],
                source=["aws.storagegateway"],
                detail_type=["Storage Gateway Refresh Cache Event"],
                detail=dict(
                    folderList=[
                        {
                            "anything-but": [
                                prefix,
                                '/',
                            ]
                        }
                    ]
                )
            )
        )
        return self

    def add_schedule(self, schedule):
        '''[optional] Set Lambda Function to run at given schedule'''
        Rule(
            self, "LambdaSchedule",
            description=f"Invoke Lambda Trigger at {schedule}",
            enabled=True,
            targets=[LambdaFunction(self.lambda_function)],
            schedule=Schedule.cron(**schedule),
        )
        return self

    def add_dynamodb_streams(self, table_name=None, partition_key=None, sort_key=None):
        '''[optional] Invoke Lambda Function based on changes to DynamDB Table table_name'''
        self.database = Table(
            self, table_name,
            server_side_encryption=True,
            billing_mode=BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            partition_key=Attribute(
                name=partition_key,
                type=AttributeType.STRING
            ),
            sort_key=Attribute(
                name=sort_key,
                type=AttributeType.STRING
            ),
            stream=StreamViewType.NEW_AND_OLD_IMAGES,
            #time_to_live_attribute="ttl",
        )

        self.lambda_function.add_event_source(
            DynamoEventSource(
                table=self.database,
                starting_position=StartingPosition.LATEST,
            )
        )

        StringParameter(
            self, "TableNameParameter",
            description=table_name,
            parameter_name=table_name,
            string_value=self.database.table_name,
        )
        return self

    def create_sns_topic(self, topic_name):
        '''Create SNS Topic and SSM Parameter Store value for topic_name'''
        self.sns_topic = Topic(
            self, f"{self.function_name}Topic",
            display_name=topic_name,
        )

    def add_email_subscriptions(self, email_addresses=None):
        '''Add Email Subscriptions to SNS Topic for this Lambda Function'''
        try:
            for email_address in email_addresses:
                self.sns_topic.add_subscription(
                    EmailSubscription(email_address=email_address)
                )
        except TypeError:
            'No Email Addresses'

    def get_sns_destination(self, email_addresses=None, topic_name=None):
        '''Return SNS Destination Object for Lambda Function object'''
        self.create_sns_topic(topic_name)
        self.add_email_subscriptions(email_addresses=email_addresses)
        try:
            return SnsDestination(self.sns_topic)
        except AttributeError:
            return

    def create_layers(self, layers):
        '''[optional] Create new Layer Version replacing previous version if it exists'''
        message = f'Creating Layer for {layers}'
        try:
            return [
                LayerVersion(
                    self, f"{layer} Layer",
                    code=self.get_s3_package(f"lambda_layers/{layer}"),
                    description=f"{layer} Layer",
                    layer_version_name=layer,
                    removal_policy=RemovalPolicy.DESTROY,
                ) for layer in layers
            ]
        except TypeError as error:
            f'{message}::FAILED::{error}'


class VpcLambdaConstruct(cdk.Construct):

    def __init__(
        self, scope: cdk.Construct, id,
        function_name=None,
        devops_bucket=None,
        layers=None,
        target_security_groups=None,
        subnet_ids=None,
        email_addresses=None,
        topic_name=None,
        retries=0,
        memory_size=128,
        duration=1,
        environment_variables=None,
        vpc_id=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.function_name = function_name
        self.create_role(f"{function_name}_role")
        self.get_vpc()
        self.get_s3_bucket(devops_bucket)

        self.lambda_function = Function(
            self, self.function_name,
            code=self.get_s3_package(f'lambda_functions/{self.function_name}'),
            function_name=self.function_name,
            handler=f"{self.function_name}.handler",
            layers=self.create_layers(layers),
            timeout=Duration.minutes(duration),
            runtime=Runtime.PYTHON_3_9,
            retry_attempts=retries,
            memory_size=memory_size,
            role=self.role,
            security_groups=self.create_security_group(target_security_groups),
            vpc=self.vpc,
            vpc_subnets=self.get_subnets(subnet_ids),
            environment=environment_variables,
            on_failure=self.get_sns_destination(
               email_addresses=email_addresses,
               topic_name=topic_name if topic_name else self.function_name,
            ),
        )
        #self.sns_topic.grant_publish(self.lambda_function)

    def create_security_group(self, target_security_groups):
        '''Return Security Group with outbound and inbound rules to target_security_groups'''
        return [
            TwoWaySecurityGroup(
                self, "LambdaSecurityGroup",
                security_group_name=f'lambda-{self.function_name}',
                target_security_groups=target_security_groups,
            ).security_group
        ]

    def get_subnets(self, subnet_ids):
        '''Return SubnetSelection object from given subnet_ids or None'''
        try:
            return SubnetSelection(
                subnets=[
                    Subnet.from_subnet_id(self, subnet_id,
                        subnet_id=subnet_id
                    ) for subnet_id in subnet_ids
                ]
            )
        except TypeError:
            return

    def get_vpc(self):
        '''Return VPC object from vpc_id lookup
           requires credentials to work properly
           use create_cdk_context.py to bypass this
        '''
        self.vpc = Vpc.from_lookup(
            self, "VPC",
            vpc_id=self.node.try_get_context('vpc_id'),
            is_default=False
        )

    def get_s3_bucket(self, devops_bucket):
        '''Return Bucket object from looking up devops_bucket'''
        self.bucket = Bucket.from_bucket_name(
            self, "S3Bucket",
            bucket_name=devops_bucket,
        )

    def managed_policies(self):
        '''Return default managed policy names for VPC based Lambda functions'''
        return (
            "CloudWatchAgentServerPolicy",
            "service-role/AWSLambdaVPCAccessExecutionRole",
        )

    def get_managed_policies(self):
        '''Return Managed Policy Objects from managed policies list'''
        return [
            ManagedPolicy.from_aws_managed_policy_name(name)
            for name in self.managed_policies()
        ]

    def add_managed_policy_to_role(self, *policy_names):
        '''Update Lambda Function Role with given Managed Policies'''
        for policy_name in policy_names:
            self.role.add_managed_policy(
                ManagedPolicy.from_aws_managed_policy_name(policy_name)
            )
        return self

    def add_customer_managed_policy_to_role(self, *policy_names):
        '''Update Lambda Function Role with given Customer Managed Policies'''
        for policy_name in policy_names:
            self.role.add_managed_policy(
                ManagedPolicy.from_managed_policy_name(policy_name)
            )
        return self

    def create_role(self, role_name):
        '''Create Required Role for Lambda Function'''
        # self.role = IAMRole(
        #     role_name=role_name,
        #     assumed_by='lambda',
        #     managed_policies=self.managed_policies(),
        # ).role
        self.role = Role(
            self, role_name,
            assumed_by=ServicePrincipal("lambda.amazonaws.com"),
            description=role_name,
            managed_policies=self.get_managed_policies(),
            # role_name=role_name,
        )
        StringParameter(
            self, "RoleParameter",
            description=role_name,
            parameter_name=role_name,
            string_value=self.role.role_arn,
        )

    def add_ssm_permissions(self):
        '''[optional] Add SSM Permissions to the Lambda Function Role'''
        self.add_managed_policy_to_role("service-role/AmazonSSMAutomationRole")
        self.role.assume_role_policy.add_statements(
            Policies.trust_policy(ServicePrincipal("ssm.amazonaws.com"))
        )
        self.role.add_to_policy(Policies.ssm_get_parameter_policy())
        return self

    def add_policy_to_role(self, *policy_statements):
        '''[optional] Add Custom Policy Statements to Lambda Function Role'''
        for policy_statement in policy_statements:
            self.role.add_to_policy(policy_statement)
        return self

    def get_s3_package(self, filename):
        '''Return Code object referencing location of packaged Lambda Function Code'''
        return S3Code(self.bucket, f'{filename}.zip')

    def add_s3_notification_resource_policy(self, source_account=None, source_bucket=None):
        '''[optional] Add permissions for an S3 object to Invoke this Lambda Function'''
        self.lambda_function.add_permission(
            "ResourcePolicy",
            principal=ServicePrincipal("s3.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_account=source_account,
            source_arn=f"arn:aws:s3:::{source_bucket}"
        )
        return self

    def create_event_bridge_rule(self, rule_name=None, event_pattern=None):
        '''[optional] Add EventPattern to Invoke this Lambda Function'''
        return Rule(
            self, rule_name,
            description=f'Invoke {self.lambda_function.function_name} to {rule_name}',
            enabled=True,
            targets=[LambdaFunction(self.lambda_function)],
            event_pattern=event_pattern
        )

    def add_ssm_event_rule(self, rule_name="LogSystemsManagerAutomationEvents", prefix=None):
        '''[optional] Add EventPattern for Systems Manager Automation Events to Invoke this Lambda Function based on the given prefix

            :params rule_name
            :params prefix
        '''
        self.create_event_bridge_rule(
            rule_name=rule_name,
            event_pattern=EventPattern(
                source=["aws.ssm"],
                detail_type=[
                    "EC2 Automation Step Status-change Notification",
                    "EC2 Automation Execution Status-change Notification"
                ],
                detail=dict(
                    Definition=[
                        dict(
                            prefix=prefix
                        )
                    ]
                )
            )
        )
        return self

    def add_storage_gateway_rule(
        self, rule_name="LogStorageGatewayRefreshComplete",
        prefix=None, storage_gateway_account=None
    ):
        '''[optional] Add EventPattern for StorageGateway Refresh Cache events to Invoke this Lambda Function based on the given prefix

            :params rule_name
            :params prefix
        '''
        self.create_event_bridge_rule(
            rule_name=rule_name,
            event_pattern=EventPattern(
                account=[storage_gateway_account],
                source=["aws.storagegateway"],
                detail_type=["Storage Gateway Refresh Cache Event"],
                detail=dict(
                    folderList=[
                        {
                            "anything-but": [
                                prefix,
                                '/',
                            ]
                        }
                    ]
                )
            )
        )
        return self

    def add_schedule(self, schedule):
        '''[optional] Set Lambda Function to run at given schedule'''
        Rule(
            self, "LambdaSchedule",
            description=f"Invoke {self.function_name} at {schedule}",
            enabled=True,
            targets=[LambdaFunction(self.lambda_function)],
            schedule=Schedule.cron(**schedule),
        )
        return self

    def add_dynamodb_streams(self, table_name=None, partition_key=None, sort_key=None):
        '''[optional] Invoke Lambda Function based on changes to DynamDB Table table_name'''
        self.database = Table(
            self, table_name,
            server_side_encryption=True,
            billing_mode=BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            partition_key=Attribute(
                name=partition_key,
                type=AttributeType.STRING
            ),
            sort_key=Attribute(
                name=sort_key,
                type=AttributeType.STRING
            ),
            stream=StreamViewType.NEW_AND_OLD_IMAGES,
            #time_to_live_attribute="ttl",
        )

        self.lambda_function.add_event_source(
            DynamoEventSource(
                table=self.database,
                starting_position=StartingPosition.LATEST,
            )
        )

        StringParameter(
            self, "TableNameParameter",
            description=table_name,
            parameter_name=table_name,
            string_value=self.database.table_name,
        )
        return self

    def create_sns_topic(self, topic_name):
        '''Create SNS Topic and SSM Parameter Store value for topic_name'''
        self.sns_topic = Topic(
            self, f"{self.function_name}Topic",
            display_name=topic_name,
        )

    def add_email_subscriptions(self, email_addresses=None):
        '''Add Email Subscriptions to SNS Topic for this Lambda Function'''
        try:
            for email_address in email_addresses:
                self.sns_topic.add_subscription(
                    EmailSubscription(email_address=email_address)
                )
        except TypeError:
            'No Email Addresses'

    def get_sns_destination(self, email_addresses=None, topic_name=None):
        '''Return SNS Destination Object for Lambda Function object'''
        self.create_sns_topic(topic_name)
        self.add_email_subscriptions(email_addresses=email_addresses)
        try:
            return SnsDestination(self.sns_topic)
        except AttributeError:
            return

    def create_layers(self, layers):
        '''[optional] Create new Layer Version replacing previous version if it exists'''
        message = f'Creating Layer for {layers}'
        try:
            return [
                LayerVersion(
                    self, f"{layer} Layer",
                    code=self.get_s3_package(f"lambda_layers/{layer}"),
                    description=f"{layer} Layer",
                    layer_version_name=layer,
                    removal_policy=RemovalPolicy.DESTROY,
                ) for layer in layers
            ]
        except TypeError as error:
            f'{message}::FAILED::{error}'