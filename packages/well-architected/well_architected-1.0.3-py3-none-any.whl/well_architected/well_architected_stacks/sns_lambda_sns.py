import aws_cdk
import constructs

import well_architected_constructs.lambda_function
import well_architected_constructs.sns_lambda

import well_architected_stack


class SnsLambdaSns(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        topic = aws_cdk.aws_sns.Topic(
            self, 'SnsTopic',
            display_name='SnsTopic'
        )

        well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, 'SnsSubscriber',
            function_name="sns_subscriber",
            sns_topic=topic,
            error_topic=self.error_topic,
        )

        sns_publisher = well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, 'SnsPublisher',
            function_name='sns_publisher',
            sns_topic=sns_topic,
            error_topic=self.error_topic,
            environment_variables={
                'TOPIC_ARN': topic.topic_arn,
            }
        ).lambda_function

        topic.grant_publish(sns_publisher)