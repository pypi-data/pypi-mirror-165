import aws_cdk
import constructs


class Stack(aws_cdk.Stack):

    def __init__(self, scope: constructs.Construct, id: str, error_topic=None, **kwargs):
        super().__init__(
            scope, id,
            synthesizer=aws_cdk.LegacyStackSynthesizer(),
            **kwargs,
        )
        self.error_topic = error_topic if error_topic else self.create_sns_topic(f'{id}ErrorTopic')

    def create_sns_topic(self, display_name):
        return aws_cdk.aws_sns.Topic(
            self, display_name,
            display_name=display_name,
        )