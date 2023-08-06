import aws_cdk
import constructs

import well_architected_constructs.dynamodb_table
import well_architected_constructs.lambda_function
import well_architected_constructs.rest_api
import json

import well_architected_stack


class RestApiDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key:str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        dynamodb_table = self.create_dynamodb_table(
            partition_key=partition_key,
            error_topic=self.error_topic,
        )

        self.create_lambda_function_with_dynamodb_event_source(
            dynamodb_table=dynamodb_table,
            error_topic=self.error_topic,
        )

        rest_api = self.create_rest_api(self.error_topic)
        rest_api.add_method(
            method='POST',
            path='InsertItem',
            uri='arn:aws:apigateway:us-east-1:dynamodb:action/PutItem',
            request_templates=self.get_request_template(dynamodb_table.table_name),
            success_response_templates={
                partition_key: 'item added to db'
            },
            error_selection_pattern="BadRequest",
        )

        dynamodb_table.grant_read_write_data(rest_api.api_gateway_service_role)

    def get_request_template(self, table_name):
        return json.dumps({
            "TableName": table_name,
            "Item": {
                "message": { "S": "$input.path('$.message')" }
            }
        })

    def create_dynamodb_table(self, partition_key=None, error_topic=None):
        return well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, 'DynamoDbTable',
            stream=aws_cdk.aws_dynamodb.StreamViewType.NEW_IMAGE,
            error_topic=error_topic,
            partition_key=partition_key,
        ).dynamodb_table

    def create_lambda_function_with_dynamodb_event_source(
        self, dynamodb_table=None, error_topic=None
    ):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=error_topic,
            function_name='subscribe',
        ).lambda_function.add_event_source(
            aws_cdk.aws_lambda_event_sources.DynamoEventSource(
                table=dynamodb_table,
                starting_position=aws_cdk.aws_lambda.StartingPosition.LATEST,
            )
        )

    def create_rest_api(self, error_topic):
        return well_architected_constructs.rest_api.RestApiConstruct(
            self, 'RestApiDynamodb',
            error_topic=error_topic,
        )