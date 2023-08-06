import constructs
import well_architected_constructs.api_lambda_dynamodb

import well_architected_stack


class ApiLambdaDynamodbStack(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None, partition_key=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        well_architected_constructs.api_lambda_dynamodb.ApiLambdaDynamodbConstruct(
            self, 'ApiLambdaDynamodb',
            function_name=function_name,
            error_topic=self.error_topic,
            partition_key=partition_key,
        )