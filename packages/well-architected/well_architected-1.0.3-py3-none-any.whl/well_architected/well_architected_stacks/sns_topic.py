import aws_cdk
import constructs


import well_architected_stack


class SnsTopic(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, display_name=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.sns_topic = aws_cdk.aws_sns.Topic(
            self, id,
            display_name=display_name,
        )