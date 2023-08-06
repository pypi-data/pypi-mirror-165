import aws_cdk
import aws_cdk.aws_lambda
import aws_cdk.aws_sam
import constructs


import well_architected_stack


class LambdaPowerTuner(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        example_lambda_function = aws_cdk.aws_lambda.Function(
            self, "exampleLambda",
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=aws_cdk.aws_lambda.Code.from_inline(
                "def handler(event, context): return 'hi'"),
        )

        aws_cdk.CfnOutput(self, 'LambdaARN', value=example_lambda_function.function_arn)

        aws_cdk.aws_sam.CfnApplication(
            self, 'powerTuner',
            location=self.get_lambda_power_tuner_location(),
            parameters=self.get_parameters(),
        )

    @staticmethod
    def get_lambda_power_tuner_location():
        return {
            "applicationId": "arn:aws:serverlessrepo:us-east-1:451282441545:applications/aws-lambda-power-tuning",
            "semanticVersion": "3.4.0"
        }

    def get_parameters(self):
        return {
            "lambdaResource": '*',
            "PowerValues": self.power_values()
        }

    @staticmethod
    def power_values():
        return '128,256,512,1024,1536,3008'