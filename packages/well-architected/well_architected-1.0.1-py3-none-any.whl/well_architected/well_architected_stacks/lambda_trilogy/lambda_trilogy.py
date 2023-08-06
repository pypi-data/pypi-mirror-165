import aws_cdk
import constructs
import aws_cdk.aws_apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha


import well_architected_constructs.api
import well_architected_constructs.api_lambda
import well_architected_constructs.lambda_function


class LambdaTrilogy(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.function_name = function_name
        add = 'add'
        subtract = 'subtract'
        multiply = 'multiply'

        adder = self.create_lambda_function(add)
        rest_api = self.create_rest_api(
            error_topic=self.error_topic,
            lambda_function=adder,
        )

        http_api = self.create_http_api(self.error_topic)

        self.create_api_methods(
            http_api=http_api,
            rest_api=rest_api,
            lambda_functions=(
                (add, adder),
                (subtract, self.create_lambda_function(subtract)),
                (multiply, self.create_lambda_function(multiply)),
            ),
        )

    def create_api_methods(self, lambda_functions=None, rest_api=None, http_api=None):
        for path, lambda_function in lambda_functions:
            self.create_rest_api_method(
                rest_api=rest_api,
                path=path,
                lambda_function=lambda_function,
            )
            self.create_http_api_method(
                http_api=http_api,
                path=path,
                lambda_function=lambda_function,
            )

    @staticmethod
    def create_http_api_method(http_api=None, path=None, lambda_function=None):
        return http_api.add_routes(
            path=f'/{path}',
            methods=[aws_cdk.aws_apigatewayv2_alpha.HttpMethod.GET],
            integration=aws_cdk.aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                f'HttpApi{path.title()}Integration',
                handler=lambda_function
            ),
        )

    @staticmethod
    def create_rest_api_method(rest_api=None, path=None, lambda_function=None):
        return rest_api.root.resource_for_path(path).add_method(
            'GET', aws_cdk.aws_apigateway.LambdaIntegration(lambda_function)
        )

    def create_rest_api(self, error_topic=None, lambda_function=None):
        return well_architected_constructs.api_lambda.create_rest_api_lambda(
            self,
            error_topic=error_topic,
            lambda_function=lambda_function,
            proxy=False,
        ).api

    def create_http_api(self, error_topic):
        return well_architected_constructs.api.Api(
            self, 'HttpApiGateway',
            error_topic=error_topic,
            api_gateway_service_role=False,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                self, 'HttpApi',
            )
        ).api

    def create_lambda_function(self, handler_name):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, handler_name,
            error_topic=self.error_topic,
            function_name=self.function_name,
            handler_name=handler_name,
        ).lambda_function