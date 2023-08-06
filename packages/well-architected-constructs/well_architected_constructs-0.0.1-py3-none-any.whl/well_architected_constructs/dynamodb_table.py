import aws_cdk
import constructs

from . import well_architected_construct


class DynamodbTableConstruct(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
            table_name=None,
            error_topic=None,
            partition_key: str=None,
            sort_key: str=None,
            time_to_live_attribute=None,
            stream=None,
            **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )

        self.dynamodb_table = aws_cdk.aws_dynamodb.Table(
            self, id,
            table_name=table_name,
            billing_mode=aws_cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=self.get_dynamodb_key(partition_key),
            sort_key=self.get_dynamodb_key(sort_key),
            stream=stream,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            time_to_live_attribute=time_to_live_attribute,
        )
        self.create_user_errors_alarm()
        self.create_throttles_alarm()
        self.create_cloudwatch_dashboard(
            self.create_cloudwatch_widgets()
        )

    @staticmethod
    def get_dynamodb_key(key):
        # if key is not None:
        if isinstance(key, str):
            return aws_cdk.aws_dynamodb.Attribute(
                name=key,
                type=aws_cdk.aws_dynamodb.AttributeType.STRING,
            )
        if isinstance(key, aws_cdk.aws_dynamodb.Attribute):
            return key
        return None

    def get_dynamodb_metric(self, metric_name, statistic='sum'):
        return self.dynamodb_table.metric(metric_name=metric_name, statistic=statistic)

    def create_throttles_metric(self, action='Read'):
        return self.get_dynamodb_metric(f'{action}ThrottleEvents')

    def create_throttles_alarm(self):
        return self.create_cloudwatch_alarm(
            id="ReadsWritesThrottled",
            metric=self.cloudwatch_math_sum(
                label="dynamodb_throttles",
                m1=self.create_throttles_metric(),
                m2=self.create_throttles_metric('Write'),
            ),
        )

    def create_user_errors_alarm(self):
        return self.create_cloudwatch_alarm(
            id='UserErrorsGreaterThanZero',
            metric=self.dynamodb_table.metric_user_errors(),
            threshold=0,
        )

    def create_system_errors_alarm(self):
        # creates jsii.errors.JSIIError: Alarms on math expressions cannot contain more than 10 individual metrics
        return self.create_cloudwatch_alarm(
            id='SystemErrorsGreaterThanZero',
            metric=self.dynamodb_table.metric_system_errors_for_operations(),
            threshold=0,
        )

    def create_latency_widget(self):
        return self.create_cloudwatch_widget(
            title="dynamodb_latency",
            left=[
                self.dynamodb_table.metric_successful_request_latency(
                    dimensions_map={
                        'TableName': self.dynamodb_table.table_name,
                        'Operation': action,
                    }
                ) for action in (
                    'GetItem', 'UpdateItem', 'PutItem', 'DeleteItem', 'Query',
                )
            ],
        )

    def create_read_write_capacity_widget(self):
        return self.create_cloudwatch_widget(
            title="dynamodb_consumed_read_write_units",
            stacked=False,
            left=[
                self.get_dynamodb_metric(metric_name, statistic='avg') for metric_name in (
                    'ConsumedReadCapacityUnits', 'ConsumedWriteCapacityUnits',
                )
            ]
        )

    def create_throttles_widget(self):
        return self.create_cloudwatch_widget(
            title="dynamodb_throttles",
            left=[
                self.create_throttles_metric(),
                self.create_throttles_metric('Write')
            ],
        )

    def create_cloudwatch_widgets(self):
        return  (
            self.create_latency_widget(),
            self.create_read_write_capacity_widget(),
            self.create_throttles_widget(),
        )