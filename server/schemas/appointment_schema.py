# server/schemas/appointment_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    patient_id: int
    dentist_id: int
    appointment_time: datetime
    status: str = "scheduled"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    status: Optional[str] = None


class AppointmentInDBBase(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Appointment(AppointmentInDBBase):
    pass


class AppointmentInDB(AppointmentInDBBase):
    pass
