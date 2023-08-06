import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs

from . import api


class HttpApiStepFunctionsConstruct(api.Api):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None,
        state_machine_arn=None,
        api_gateway_service_role=None,
        **kwargs,
    ):
        super().__init__(
            scope, id,
            error_topic=error_topic,
            api_gateway_service_role=api_gateway_service_role,
            api=aws_cdk.aws_apigatewayv2_alpha.HttpApi(
                scope, 'HttpApi',
                create_default_stage=True,
            ),
            **kwargs,
        )
        self.create_http_api_step_functions_route(state_machine_arn)

    def create_http_api_step_functions_route(
        self, state_machine_arn
    ):
        return aws_cdk.aws_apigatewayv2.CfnRoute(
            self, 'HttpApiStateMachineDefaultRoute',
            api_id=self.api_id,
            route_key=aws_cdk.aws_apigatewayv2_alpha.HttpRouteKey.DEFAULT.key,
            target=f'integrations/{self.create_http_api_stepfunctions_integration(state_machine_arn)}',
        )

    def create_http_api_stepfunctions_integration(
        self, state_machine_arn
    ):
        return aws_cdk.aws_apigatewayv2.CfnIntegration(
            self, 'HttpApiStateMachineIntegration',
            api_id=self.api_id,
            integration_type='AWS_PROXY',
            connection_type='INTERNET',
            integration_subtype='StepFunctions-StartSyncExecution',
            credentials_arn=self.api_gateway_service_role.role_arn,
            request_parameters={
                "Input": "$request.body",
                "StateMachineArn": state_machine_arn,
            },
            payload_format_version="1.0",
            timeout_in_millis=10000
        ).ref