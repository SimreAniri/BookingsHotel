from datetime import date
from app.exceptions import InvalidBookingDateExeption
from app.hotels.rooms.schemas import SRoomsInHotelDate

from app.hotels.router import router

from app.hotels.rooms.dao import RoomsDAO


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[SRoomsInHotelDate]:
    if date_from >= date_to:
        raise InvalidBookingDateExeption

    return await RoomsDAO.left_rooms(hotel_id, date_from, date_to)
