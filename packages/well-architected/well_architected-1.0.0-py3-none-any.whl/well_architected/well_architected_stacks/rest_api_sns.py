import constructs


import well_architected_constructs.rest_api_sns

import well_architected_stack


class RestApiSnsStack(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None, display_name=None,
        sns_topic_arn=None,
        error_topic=None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)
        well_architected_constructs.rest_api_sns.RestApiSnsConstruct(
            self, 'RestApiSns',
            message="$util.urlEncode($context.path)",
            error_topic=error_topic,
            sns_topic_arn=sns_topic_arn,
        )