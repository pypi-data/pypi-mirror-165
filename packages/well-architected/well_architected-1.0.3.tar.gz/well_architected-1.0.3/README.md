# Well Architected

Well-Architected CDK Patterns in Python from https://cdkpatterns.com/patterns/well-architected/

# Available Stacks
- ApiLambdaRds
- ApiLambdaDynamodb
- ApiLambdaDynamodbEventBridgeLambda
- AutoscalingEcsService
- AutoscalingEcsServiceWithPlacement
- AutoscalingEcsCluster
- AlbAutoscalingEcsService
- NlbAutoscalingEcsService
- NlbFargateService
- NlbAutoscalingFargateService
- ApiLambdaEventBridgeLambda
- ApiLambdaSqsLambdaDynamodb
- ApiSnsLambdaEventBridgeLambda
- ApiSnsSqsLambda
- ApiStepFunctions
- LambdaFat
- LambdaLith
- LambdaPowerTuner
- LambdaSinglePurpose
- RestApiDynamodb
- RestApiSns
- S3SqsLambdaEcsEventBridgeLambdaDynamodb
- SagaStepFunction
- SimpleGraphqlService
- SnsLambda
- SnsLambdaSns
- SnsLambdaDynamodb
- SqsLambdaSqs
- WafApiLambdaDynamodb

# Available Constructs
- Api
- ApiLambda
- ApiLambdaDynamodb
- DynamodbTable
- HttpApiStepFunctions
- LambdaFunction
- RestApi
- RestApiSns
- SnsLambda
- WebApplicationFirewall

# Examples

## Using a Well Architected Stack
```Python
import aws_cdk
import well_architected_stacks

app = aws_cdk.App()
well_architected_stacks.api_lambda_eventbridge_lambda.ApiLambdaDynamodbEventBridgeLambda(
    app, 'ApiLambdaDynamodbEventBridgeLambda
)
app.synth()
```

## Creating a Stack using Well Architected Constructs
```Python
import constructs
import well_architected_constructs.web_application_firewall
import well_architected_constructs.api_lambda_dynamodb

import well_architected_stack


class WafApiLambdaDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key='path',
        sort_key=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        self.name = self.camel_to_snake(id)
        self.api_lambda_dynamodb = well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'ApiLambdaDynamoDb',
            function_name=self.name,
            partition_key=partition_key,
            error_topic=self.error_topic,
        )

        self.web_application_firewall = well_architected_constructs.web_application_firewall.WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            error_topic=self.error_topic,
            target_arn= f"arn:aws:apigateway:region::/restapis/{self.api_lambda_dynamodb.rest_api.api_id}/stages/{self.api_lambda_dynamodb.rest_api.api.deployment_stage.stage_name}",
        )

    @staticmethod
    def camel_to_snake(text):
        return ''.join([
            '_'+character.lower()
            if character.isupper()
            else character
            for character in text
        ]).lstrip('_')
```
