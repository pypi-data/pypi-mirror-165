import aws_cdk
import constructs

from . import lambda_function
from . import well_architected_construct


class SnsLambdaConstruct(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic: aws_cdk.aws_sns.Topic=None,
        error_topic=None,
        function_name=None,
        environment_variables=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )

        self.lambda_function = lambda_function.create_python_lambda_function(
            scope,
            function_name=function_name,
            error_topic=error_topic,
            environment_variables=environment_variables,
        )
        sns_topic.add_subscription(
            aws_cdk.aws_sns_subscriptions.LambdaSubscription(
                self.lambda_function
            )
        )