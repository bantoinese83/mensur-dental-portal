from botocore.exceptions import ClientError

from core.aws_config import ses_client
from core.celery_config import celery_app


@celery_app.task
def send_appointment_reminder(email: str, appointment_time: str):
    subject = "Appointment Reminder"
    body = f"Dear patient, this is a reminder for your appointment scheduled at {appointment_time}."
    try:
        ses_client.send_email(
            Source="your-email@example.com",
            Destination={"ToAddresses": [email]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        return f"Reminder sent to {email}"
    except ClientError as e:
        return f"Failed to send reminder: {e.response['Error']['Message']}"

