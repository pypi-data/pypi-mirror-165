import aws_cdk
import aws_cdk.aws_apigatewayv2_alpha
import constructs

from . import well_architected_construct


class Api(well_architected_construct.Construct):

    def __init__(
        self,scope: constructs.Construct, id: str,
        error_topic=None,
        api=None,
        api_gateway_service_role=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        self.api = api
        self.api_id = self.get_api_id(api)
        self.api_gateway_service_role = self.create_api_gateway_service_role(api_gateway_service_role)
        self.create_api_gateway_4xx_alarm()
        self.create_api_gateway_5xx_alarm()
        self.create_api_gateway_latency_alarm()
        self.create_cloudwatch_dashboard(self.create_cloudwatch_widgets())
        aws_cdk.CfnOutput(self, f'{id} URL', value=api.url)

    def get_api_id(self, api):
        try:
            return api.api_id
        except AttributeError:
            return api.rest_api_id

    def create_api_gateway_service_role(self, iam_role):
        if iam_role:
            return iam_role
        if iam_role == False:
            return
        if iam_role is None:
            return aws_cdk.aws_iam.Role(
                self, 'ApiGatewayServiceRole',
                assumed_by=aws_cdk.aws_iam.ServicePrincipal('apigateway.amazonaws.com'),
            )

    def add_api_gateway_metric(self, metric_name: str = None, label: str = None,
            period=aws_cdk.Duration.seconds(900), statistic: str = 'sum',
        ):
        return aws_cdk.aws_cloudwatch.Metric(
            metric_name=metric_name,
            namespace="AWS/ApiGateway",
            dimensions_map={"ApiId": self.api_id},
            unit=aws_cdk.aws_cloudwatch.Unit.COUNT,
            label=label,
            statistic=statistic,
            period=period,
        )

    def create_api_gateway_4xx_alarm(self):
        return self.create_cloudwatch_alarm(
            id="4XXErrorsGreaterThanOnePercent",
            metric=self.create_cloudwatch_math_expression(
                expression="m1 / m2 * 100",
                label="api_gateway_4XX_errors_percentage",
                using_metrics={
                    "m1": self.add_api_gateway_metric(
                        metric_name='4XXError',
                        label='4XX_errors',
                    ),
                    "m2": self.add_api_gateway_metric(
                        metric_name='Count',
                        label='number_of_requests',
                    ),
                },
            ),
        )

    def create_api_gateway_5xx_alarm(self):
        return self.create_cloudwatch_alarm(
            id="5XXErrorsGreaterThanZero",
            metric=self.add_api_gateway_metric(
                metric_name="5XXError",
                label="api_gateway_5XX_errors",
                statistic="p99",
            ),
            threshold=0,
        )

    def create_api_gateway_latency_alarm(self):
        return self.create_cloudwatch_alarm(
            id="P99LatencyGreaterThanOneSecond",
            metric=self.add_api_gateway_metric(
                metric_name="Latency",
                label="api_gateway_latency",
                statistic="p99",
            ),
            threshold=1000,
        )

    @staticmethod
    def percentile_statistics():
        return ("p50", "p90", "p99",)

    @staticmethod
    def metric_names():
        return (f'{code}XXError' for code in ('4', '5'))

    def create_api_gateway_errors_widget(self):
        return self.create_cloudwatch_widget(
            title="api_gateway_errors",
            left=[
                self.add_api_gateway_metric(
                    metric_name=metric_name,
                    label=f'api_gateway_{metric_name}s',
                ) for metric_name in self.metric_names()
            ]
        )

    def create_api_gateway_latency_widget(self):
        return self.create_cloudwatch_widget(
            title="api_gateway_latency",
            left=[
                self.add_api_gateway_metric(
                    metric_name="Latency",
                    label=f'api_gateway_latency_{statistic}',
                    statistic=statistic,
                ) for statistic in self.percentile_statistics()
            ]
        )

    def create_api_gateway_number_of_requests_widget(self):
        return self.create_cloudwatch_widget(
            title="Requests",
            stacked=False,
            left=[
                self.add_api_gateway_metric(
                    metric_name="Count",
                    label="# Requests",
                )
            ]
        )

    def create_cloudwatch_widgets(self):
        return (
            self.create_api_gateway_number_of_requests_widget(),
            self.create_api_gateway_latency_widget(),
            self.create_api_gateway_errors_widget(),
        )