import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha
import constructs

import well_architected_constructs.lambda_function
import well_architected_constructs.api_lambda

import well_architected_stack


class ApiLambdaRds(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_cdk.aws_ec2.Vpc(self, 'Vpc', max_azs=2)
        db_credentials_secret = self.create_credentials_secret(id)
        self.create_parameter_store_for_db_credentials(db_credentials_secret.secret_arn)
        rds_instance = self.create_rds_instance(
            credentials_secret=db_credentials_secret,
            vpc=vpc
        )

        rds_proxy = rds_instance.add_proxy(
            f'{id}-proxy',
            secrets=[db_credentials_secret],
            debug_logging=True,
            vpc=vpc,
        )

        rds_lambda = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name='rds',
            vpc=vpc,
            environment_variables={
                "PROXY_ENDPOINT": rds_proxy.endpoint,
                "RDS_SECRET_NAME": f'{id}-rds-credentials',
            }
        )

        db_credentials_secret.grant_read(rds_lambda)

        for security_group, description in (
            (rds_proxy, 'allow db connection'),
            (rds_lambda, 'allow lambda connection'),
        ):
            rds_instance.connections.allow_from(
                security_group,
                aws_cdk.aws_ec2.Port.tcp(3306),
                description=description
            )

        well_architected_constructs.api_lambda.create_http_api_lambda(
            self, lambda_function=rds_lambda,
            error_topic=self.error_topic,
        )
        well_architected_constructs.api_lambda.create_rest_api_lambda(
            self, lambda_function=rds_lambda,
            error_topic=self.error_topic,
        )

    def create_credentials_secret(self, id):
        return aws_cdk.aws_secretsmanager.Secret(
            self, 'DBCredentialsSecret',
            secret_name=f'{id}-rds-credentials',
            generate_secret_string=aws_cdk.aws_secretsmanager.SecretStringGenerator(
                secret_string_template="{\"username\":\"syscdk\"}",
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password"
            )
        )

    def create_parameter_store_for_db_credentials(self, db_credentials_arn):
        return aws_cdk.aws_ssm.StringParameter(
            self, 'DBCredentialsArn',
            parameter_name='rds-credentials-arn',
            string_value=db_credentials_arn
        )

    def create_rds_instance(self, credentials_secret=None, vpc=None):
        return aws_cdk.aws_rds.DatabaseInstance(
            self, 'DBInstance',
            engine=aws_cdk.aws_rds.DatabaseInstanceEngine.mysql(
                version=aws_cdk.aws_rds.MysqlEngineVersion.VER_5_7_30
            ),
            credentials=aws_cdk.aws_rds.Credentials.from_secret(credentials_secret),
            instance_type=aws_cdk.aws_ec2.InstanceType.of(
                aws_cdk.aws_ec2.InstanceClass.BURSTABLE2,
                aws_cdk.aws_ec2.InstanceSize.SMALL
            ),
            vpc=vpc,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            deletion_protection=False,
        )