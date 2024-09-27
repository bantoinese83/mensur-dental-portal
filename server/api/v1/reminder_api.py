# server/api/v1/reminder_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from utils.tasks_util import send_appointment_reminder

router = APIRouter()


class ReminderRequest(BaseModel):
    email: EmailStr
    appointment_time: str


@router.post("/send-reminder", summary="Send Appointment Reminder", description="Send an appointment reminder email.")
def send_reminder(request: ReminderRequest):
    try:
        send_appointment_reminder.delay(request.email, request.appointment_time)
        return {"message": "Reminder is being sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
