# server/api/v1/analytics_api.py
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.dependencies import get_db_session
from crud.appointment_crud import get_appointments
from crud.user_crud import get_users
from schemas.appointment_schema import Appointment

router = APIRouter()


@router.get("/user-analytics", summary="Get user analytics", description="Retrieve analytics data for users.")
def user_analytics(db: Session = Depends(get_db_session)):
    users = get_users(db)
    total_users = len(users)
    active_users = len([user for user in users if user.is_active])
    dentists = len([user for user in users if user.is_dentist])
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_dentists": dentists,
    }


@router.get("/dental-portal-analytics", summary="Get dental portal analytics",
            description="Retrieve analytics data for the dental portal.")
def dental_portal_analytics(db: Session = Depends(get_db_session)):
    appointments = get_appointments(db)
    total_appointments = len(appointments)
    upcoming_appointments = len([appt for appt in appointments if appt.status == "scheduled"])
    completed_appointments = len([appt for appt in appointments if appt.status == "completed"])
    avg_appointment_duration = db.query(func.avg(Appointment.duration)).scalar()
    appointments_per_dentist = db.query(Appointment.dentist_id, func.count(Appointment.id)).group_by(
        Appointment.dentist_id).all()
    return {
        "total_appointments": total_appointments,
        "upcoming_appointments": upcoming_appointments,
        "completed_appointments": completed_appointments,
        "avg_appointment_duration": avg_appointment_duration,
        "appointments_per_dentist": appointments_per_dentist,
    }
