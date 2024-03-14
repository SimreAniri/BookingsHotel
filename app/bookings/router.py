from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import InvalidBookingDateExeption, RoomCannotBeBooking
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    current_user: Users = Depends(get_current_user),
):
    if date_from >= date_to:
        raise InvalidBookingDateExeption

    booking = await BookingDAO.add(current_user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooking
    booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump()

    send_booking_confirmation_email(booking_dict, current_user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def del_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
