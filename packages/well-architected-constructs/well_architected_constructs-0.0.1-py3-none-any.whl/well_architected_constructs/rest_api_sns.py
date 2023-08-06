import aws_cdk
import constructs

from . import rest_api


class RestApiSnsConstruct(rest_api.RestApiConstruct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        error_topic=None,
        rest_api_name=None,
        api=None,
        message=None,
        additional_parameters=None,
        method='POST',
        sns_topic_arn=None,
        **kwargs,
    ):
        super().__init__(
            scope, id,
            error_topic=error_topic,
            api=aws_cdk.aws_apigateway.RestApi(
                scope, 'RestApi',
                rest_api_name=rest_api_name,
                deploy_options=self.get_stage_options(),
            ) if api is None else api,
            **kwargs,
        )
        self.add_method(
            method=method,
            path='SendEvent',
            uri='arn:aws:apigateway:us-east-1:sns:path//',
            success_response_templates={
                "message": 'Message added to SNS topic'
            },
            error_selection_pattern="Error",
            request_parameters={
                'integration.request.header.Content-Type': "'application/x-www-form-urlencoded'"
            },
            request_templates=self.call_sns_publish_api(
                sns_topic_arn=sns_topic_arn,
                additional_parameters=additional_parameters,
                message=message
            ),
        )

    @staticmethod
    def parse_additional_parameters(text):
        if text:
            return f"{text}&"
        return ""

    def call_sns_publish_api(
        self,
        additional_parameters=None,
        sns_topic_arn=None,
        message=None,
    ):
        return (
            "Action=Publish&"
            "Version=2010-03-31&"
            f"Message={message}&"
            f"{self.parse_additional_parameters(additional_parameters)}"
            f"TargetArn=$util.urlEncode('{sns_topic_arn}')"
        )