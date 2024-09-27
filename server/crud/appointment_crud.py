from sqlalchemy.orm import Session

from models.appointment_model import Appointment
from schemas.appointment_schema import AppointmentCreate, AppointmentUpdate
from utils.date_utils import get_current_datetime


def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Appointment).offset(skip).limit(limit).all()


def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        dentist_id=appointment.dentist_id,
        appointment_time=appointment.appointment_time,
        status=appointment.status,
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def update_appointment(
        db: Session, appointment_id: int, appointment: AppointmentUpdate
):
    db_appointment = (
        db.query(Appointment).filter(Appointment.id == appointment_id).first()
    )
    if db_appointment:
        for key, value in appointment.dict(exclude_unset=True).items():
            setattr(db_appointment, key, value)
        db_appointment.updated_at = get_current_datetime()
        db.commit()
        db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    db_appointment = (
        db.query(Appointment).filter(Appointment.id == appointment_id).first()
    )
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
    return db_appointment
