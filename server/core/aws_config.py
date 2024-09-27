import boto3
from pydantic.v1 import BaseSettings


class AWSSettings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    class Config:
        env_file = ".env"


aws_settings = AWSSettings()

# Create the Boto3 session
session = boto3.Session(
    aws_access_key_id=aws_settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=aws_settings.AWS_SECRET_ACCESS_KEY,
    region_name=aws_settings.AWS_REGION,
)

# Initialize the SES client
ses_client = session.client("ses")
