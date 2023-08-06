import constructs

from . import api_lambda
from . import dynamodb_table
from . import lambda_function
from . import well_architected_construct


class ApiLambdaDynamodbConstruct(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        function_name=None,
        partition_key=None,
        error_topic=None,
        **kwargs
    ) -> None:
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        self.dynamodb_table = self.create_dynamodb_table(
            partition_key=partition_key,
            error_topic=error_topic,
        )
        self.lambda_function = self.create_lambda_function(
            dynamodb_table_name=self.dynamodb_table.table_name,
            function_name=function_name,
            error_topic=error_topic,
        )
        self.dynamodb_table.grant_read_write_data(self.lambda_function)

        self.http_api = api_lambda.create_http_api_lambda(
            self, lambda_function=self.lambda_function,
            error_topic=error_topic,
        )
        self.rest_api = api_lambda.create_rest_api_lambda(
            self, lambda_function=self.lambda_function,
            error_topic=error_topic,
        )

    def create_dynamodb_table(self, partition_key=None, error_topic=None):
        return dynamodb_table.DynamodbTableConstruct(
            self, 'DynamoDbTable',
            partition_key=partition_key,
            error_topic=error_topic,
        ).dynamodb_table

    def create_lambda_function(
        self, dynamodb_table_name=None, function_name=None,
        error_topic=None,
    ):
        return lambda_function.LambdaFunctionConstruct(
            self, 'LambdaFunction',
            error_topic=error_topic,
            function_name=function_name,
            environment_variables={
                'DYNAMODB_TABLE_NAME': dynamodb_table_name
            }
        ).lambda_function