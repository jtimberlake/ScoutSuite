from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade


class DynamoDBFacade(AWSBaseFacade):
    async def get_backups(self, region, table_name):
        try:
            return await AWSFacadeUtils.get_all_pages(
                "dynamodb",
                region,
                self.session,
                "list_backups",
                "BackupSummaries",
                TableName=table_name,
            )
        except Exception as e:
            print_exception("Failed to get DynamoDB Backups for {}".format(table_name))
            return []

    async def get_tables(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages(
                "dynamodb", region, self.session, "list_tables", "TableNames"
            )
        except Exception as e:
            print_exception("Failed to get DynamoDB tables")
            return []

    async def get_tags_for_resource(self, region, resource_arn):
        try:
            return await AWSFacadeUtils.get_all_pages(
                "dynamodb",
                region,
                self.session,
                "list_tags_of_resource",
                "Tags",
                ResourceArn=resource_arn,
            )
        except Exception as e:
            print_exception(
                "Failed to get DynamoDB tags for resource {}".format(resource_arn)
            )
            return []

    async def get_table(self, region, table_name):
        client = AWSFacadeUtils.get_client("dynamodb", self.session, region)
        try:
            raw_table = await run_concurrently(
                lambda: client.describe_table(TableName=table_name)
            )
        except Exception as e:
            print_exception("Failed to get table {}: {}".format(table_name, e))
            raw_table = None
        return raw_table
