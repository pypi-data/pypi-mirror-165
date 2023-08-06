import constructs
import aws_cdk

from . import well_architected_construct


class LambdaFunctionConstruct(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        concurrent_executions=None,
        duration=60,
        environment_variables=None,
        error_topic:aws_cdk.aws_sns.Topic=None,
        event_bridge_rule=None,
        function_name=None,
        handler_name='handler',
        layers:list[str]=None,
        on_success=None,
        on_failure=None,
        retry_attempts=None,
        vpc=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        # handler_name = 'handler' if handler_name is None else handler_name
        function_name = function_name if function_name is not None else id
        self.lambda_function = aws_cdk.aws_lambda.Function(
            self, 'LambdaFunction',
            runtime=aws_cdk.aws_lambda.Runtime.PYTHON_3_9,  # type: ignore
            handler=f'{function_name}.{handler_name}',
            code=aws_cdk.aws_lambda.Code.from_asset(f"lambda_functions/{function_name}"),
            timeout=aws_cdk.Duration.seconds(duration) if duration else None,
            tracing=aws_cdk.aws_lambda.Tracing.ACTIVE,
            layers=self.create_layers(layers),
            vpc=vpc,
            reserved_concurrent_executions=concurrent_executions,
            environment=environment_variables,
            retry_attempts=retry_attempts,
            on_success=on_success,
            on_failure=on_failure,
        )
        self.add_event_bridge_rule(event_bridge_rule)
        self.create_invocations_error_greater_than_2_percent_alarm()
        self.create_invocation_longer_than_1_second_alarm()
        self.create_throttled_invocations_greater_than_2_percent_alarm()
        self.create_cloudwatch_dashboard(
            self.create_cloudwatch_widgets()
        )

    @staticmethod
    def to_camel_case(text):
        return ''.join(text.title().split('-'))

    def create_layer(self, layer):
        return aws_cdk.aws_lambda.LayerVersion(
            self, f'{self.to_camel_case(layer)}LambdaLayer',
            code=aws_cdk.aws_lambda.Code.from_asset(f"lambda_layers/{layer}"),
            description=f"{layer} Lambda Layer"
        )

    def create_layers(self, layers):
        result = [self.create_layer('aws-xray-sdk')]
        try:
            for layer in layers:
                result.append(self.create_layer(layer))
        except TypeError:
            'No additional layers specified'
        return result

    def get_lambda_function_metric(self, metric_name):
        return self.lambda_function.metric(metric_name=metric_name, statistic="sum")

    def create_lambda_error_percentage_metric(self):
        return self.create_cloudwatch_math_expression(
            label="invocations_errored_percentage_last_5_mins",
            expression="(errors / invocations) * 100",
            using_metrics={
                "invocations": self.get_lambda_function_metric('Invocations'),
                "errors": self.get_lambda_function_metric("Errors"),
            },
        )

    def create_lambda_throttled_percentage_metric(self):
        # NOTE: throttled requests are not counted in total number of invocations
        return self.create_cloudwatch_math_expression(
            label="throttled_requests_percentage_last_30_mins",
            expression="(throttles * 100) / (invocations + throttles)",
            using_metrics={
                "invocations": self.get_lambda_function_metric("Invocations"),
                "throttles": self.get_lambda_function_metric("Throttles"),
            },
        )

    def create_invocations_error_greater_than_2_percent_alarm(self):
        return self.create_cloudwatch_alarm(
            id="LambdaInvocationsErrorsGreaterThan2Percent",
            metric=self.create_lambda_error_percentage_metric(),
            threshold=2,
        )

    def create_invocation_longer_than_1_second_alarm(self):
        return self.create_cloudwatch_alarm(
            id="LambdaP99LongDurationGreaterThan1s",
            metric=self.lambda_function.metric_duration(statistic="p99"),
            threshold=1000,
        )

    def create_throttled_invocations_greater_than_2_percent_alarm(self):
        return self.create_cloudwatch_alarm(
            id="LambdaThrottledInvocationsGreaterThan2Percent",
            metric=self.create_lambda_throttled_percentage_metric(),
            threshold=2,
        )

    def create_lambda_error_percentage_widget(self):
        return self.create_cloudwatch_widget(
            title="lambda_error_percentage",
            stacked=False,
            left=[self.create_lambda_error_percentage_metric()],
        )

    def create_lambda_duration_widget(self):
        return self.create_cloudwatch_widget(
            title="lambda_duration",
            left=[
                self.lambda_function.metric_duration(statistic=statistic)
                for statistic in ('p50', 'p90', 'p99')
            ],
        )

    def create_lambda_throttled_percentage_widget(self):
        return self.create_cloudwatch_widget(
            title="lambda_throttle_percentage",
            left=[self.create_lambda_throttled_percentage_metric()],
            stacked=False,
        )

    def create_cloudwatch_widgets(self):
        return (
            self.create_lambda_error_percentage_widget(),
            self.create_lambda_duration_widget(),
            self.create_lambda_throttled_percentage_widget(),
        )

    def add_event_bridge_rule(self, event_bridge_rule):
        try:
            event_bridge_rule.add_target(
                aws_cdk.aws_events_targets.LambdaFunction(self.lambda_function)
            )
        except AttributeError:
            return

def create_python_lambda_function(
        stack,
        function_name=None,
        environment_variables=None,
        duration=60, error_topic=None, vpc=None,
        concurrent_executions=None,
    ):
    return LambdaFunctionConstruct(
        stack, function_name,
        function_name=function_name,
        environment_variables=environment_variables,
        duration=duration,
        error_topic=error_topic,
        vpc=vpc,
        concurrent_executions=concurrent_executions,
    ).lambda_function