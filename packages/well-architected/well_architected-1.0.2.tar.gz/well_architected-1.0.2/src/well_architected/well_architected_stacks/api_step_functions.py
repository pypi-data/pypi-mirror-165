import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs
import well_architected_constructs.http_api_step_functions
import well_architected_constructs.lambda_function
import well_architected_constructs.api


import well_architected_stack


class ApiStepFunctions(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.result_path = '$.resultPath'
        self.state_machine = self.create_state_machine(
            self.create_lambda_function(
                self.error_topic
            )
        )
        self.api_gateway_service_role = self.create_api_gateway_service_role(self.state_machine.state_machine_arn)

        self.rest_api = self.create_rest_api(
            error_topic=self.error_topic,
            state_machine=self.state_machine,
            api_gateway_service_role=self.api_gateway_service_role,
        )

        self.http_api = self.create_http_api(
            error_topic=self.error_topic,
            api_gateway_service_role=self.api_gateway_service_role,
            state_machine_arn=self.state_machine.state_machine_arn,
        )

    def failure_message(self):
        return aws_cdk.aws_stepfunctions.Fail(
            self, 'Failed',
            cause='Excpetion',
            error='Error'
        )

    def condition(self):
        return aws_cdk.aws_stepfunctions.Condition.boolean_equals(
            f'{self.result_path}.isValid', True
        )

    def invoke_lambda_function(self, lambda_function):
        return aws_cdk.aws_stepfunctions_tasks.LambdaInvoke(
            self, 'InvokeLambdaFunction',
            lambda_function=lambda_function,
            input_path='$.inputPath',
            result_path=self.result_path,
            payload_response_only=True
        )

    def success_message(self):
        return aws_cdk.aws_stepfunctions.Succeed(
            self, 'Success',
            output_path=self.result_path
        )

    def make_decision(self):
        return (
            aws_cdk.aws_stepfunctions.Choice(
                self, 'isValid?'
            ).when(
                self.condition(),
                self.failure_message()
            ).otherwise(
                self.success_message()
            )
        )

    def state_machine_definition(self, lambda_function):
        return (
            aws_cdk.aws_stepfunctions
                .Chain
                .start(self.invoke_lambda_function(lambda_function))
                .next(self.make_decision())
        )

    def create_lambda_function(self, error_topic):
        return well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name='lambda_function',
            error_topic=error_topic
        )

    @staticmethod
    def state_machine_execution_permissions(state_machine_arn):
        return aws_cdk.aws_iam.PolicyDocument(
            statements=[
                aws_cdk.aws_iam.PolicyStatement(
                    actions=["states:StartSyncExecution"],
                    effect=aws_cdk.aws_iam.Effect.ALLOW,
                    resources=[state_machine_arn]
                )
            ]
        )

    def create_api_gateway_service_role(self, state_machine_arn):
        return aws_cdk.aws_iam.Role(
            self, 'StateMachineApiGatewayIamServiceRole',
            assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com'),
            inline_policies={
                "AllowSFNExec": self.state_machine_execution_permissions(state_machine_arn)
            }
        )

    def create_state_machine(self, lambda_function):
        return aws_cdk.aws_stepfunctions.StateMachine(
            self, 'StateMachine',
            definition=self.state_machine_definition(lambda_function),
            timeout=aws_cdk.Duration.minutes(5),
            tracing_enabled=True,
            state_machine_type=aws_cdk.aws_stepfunctions.StateMachineType.EXPRESS
        )

    def create_http_api(self, error_topic=None, state_machine_arn=None, api_gateway_service_role=None):
        well_architected_constructs.http_api_step_functions.HttpApiStepFunctionsConstruct(
            self, 'HttpApiStepFunctions',
            error_topic=error_topic,
            api_gateway_service_role=api_gateway_service_role,
            state_machine_arn=state_machine_arn,
        )

    def create_rest_api(
        self, error_topic=None, state_machine=None, api_gateway_service_role=None
    ):
        return well_architected_constructs.api.Api(
            self, 'RestApi',
            error_topic=error_topic,
            api_gateway_service_role=api_gateway_service_role,
            api=aws_cdk.aws_apigateway.StepFunctionsRestApi(
                self, 'RestApiStepFunctions',
                state_machine=state_machine,
                deploy=True,
            )
        )