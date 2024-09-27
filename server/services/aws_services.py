# server/aws_services.py
from typing import Optional

from botocore.exceptions import NoCredentialsError, ClientError

from core.aws_config import session

# Initialize AWS clients using the session from aws_config.py
s3_client = session.client("s3")
ses_client = session.client("ses")
dynamodb_client = session.client("dynamodb")
rds_client = session.client("rds")


def upload_file_to_s3(
    file_name: str, bucket: str, object_name: Optional[str] = None
) -> bool:
    """Upload a file to an S3 bucket."""
    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def send_email_via_ses(sender: str, recipient: str, subject: str, body: str) -> bool:
    """Send an email using AWS SES."""
    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={"ToAddresses": [recipient]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        return True
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return False


def put_item_in_dynamodb(table_name: str, item: dict) -> bool:
    """Put an item into a DynamoDB table."""
    try:
        dynamodb_client.put_item(TableName=table_name, Item=item)
        return True
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return False


def execute_rds_query(query: str, db_instance_identifier: str) -> Optional[list]:
    """Execute a query on an RDS instance."""
    try:
        response = rds_client.execute_statement(
            resourceArn=db_instance_identifier, sql=query
        )
        return response["records"]
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return None
