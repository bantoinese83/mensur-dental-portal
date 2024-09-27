from sqlalchemy.orm import Session

from crud.appointment_crud import get_appointment
from utils.date_utils import get_days_between_dates


def days_between_appointments(db: Session, appointment_id1: int, appointment_id2: int) -> int:
    appointment1 = get_appointment(db, appointment_id1)
    appointment2 = get_appointment(db, appointment_id2)
    if appointment1 and appointment2:
        return get_days_between_dates(appointment1.appointment_time, appointment2.appointment_time)
    return 0
