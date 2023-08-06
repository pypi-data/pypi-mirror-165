import aws_cdk
import constructs


import well_architected_constructs.lambda_function
import well_architected_constructs.dynamodb_table

import well_architected_stack


class SnsLambdaDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)


        self.dynamodb_table = well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, "DynamoDbTable",
            partition_key="path",
            error_topic=self.error_topic,
        ).dynamodb_table

        self.lambda_function = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="hit_counter",
            error_topic=self.error_topic,
            environment_variables={
                "HITS_TABLE_NAME": self.dynamodb_table.table_name
            }
        )

        self.dynamodb_table.grant_read_write_data(self.lambda_function)
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                self.lambda_function
            )
        )