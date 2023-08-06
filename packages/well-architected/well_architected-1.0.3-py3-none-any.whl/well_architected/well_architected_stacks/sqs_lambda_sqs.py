import aws_cdk
import constructs

import well_architected_constructs.lambda_function
import well_architected_constructs.sns_lambda

import well_architected_stack


class SqsLambdaSqs(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.sqs_queue = aws_cdk.aws_sqs.Queue(
            self, 'SqsQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )
        self.create_sqs_publishing_lambda(
            sqs_queue=self.sqs_queue,
            sns_topic=sns_topic,
            error_topic=self.error_topic,
        )
        self.create_sqs_subscribing_lambda(
            sqs_queue=self.sqs_queue,
            error_topic=self.error_topic,
        )

    def create_sqs_publishing_lambda(
        self, sqs_queue: aws_cdk.aws_sqs.Queue=None,
        sns_topic: aws_cdk.aws_sns.Topic=None,
        error_topic=None,
    ):
        sqs_publisher = well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, 'SqsPublisher',
            function_name='sqs_publisher',
            error_topic=error_topic,
            sns_topic=sns_topic,
            environment_variables={
                'SQS_URL': sqs_queue.queue_url
            }
        ).lambda_function
        sqs_queue.grant_send_messages(sqs_publisher)
        return sqs_publisher

    def create_sqs_subscribing_lambda(
        self, sqs_queue: aws_cdk.aws_sqs.Queue=None, error_topic=None,
    ):
        sqs_subscriber = well_architected_constructs.lambda_function.create_python_lambda_function(
            self, function_name="sqs_subscriber",
            error_topic=error_topic,
        )
        sqs_subscriber.add_event_source(
            aws_cdk.aws_lambda_event_sources.SqsEventSource(sqs_queue)
        )
        sqs_queue.grant_consume_messages(sqs_subscriber)
        return sqs_subscriber