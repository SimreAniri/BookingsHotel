from datetime import date

from fastapi import APIRouter

from app.exceptions import InvalidBookingDateExeption
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels, SLeftRoomsInHotels

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> list[SLeftRoomsInHotels]:
    if date_from >= date_to:
        raise InvalidBookingDateExeption

    return await HotelsDAO.find_all_left_by_location(location, date_from, date_to)


@router.get("/{hotel_id}")
async def get_about_hotel(hotel_id: int) -> SHotels:
    return await HotelsDAO.find_by_id(hotel_id)
