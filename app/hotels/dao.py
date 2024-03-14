from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all_left_by_location(
        cls, location: str, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Bookings.room_id.label("rooms_id"),
                    func.count(Bookings.id).label("count_booking"),
                )
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_from > date_from,
                        ),
                    )
                )
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )

            left_rooms = (
                select(
                    Rooms.hotel_id.label("hotel_id"),
                    Rooms.id.label("rooms_id"),
                    (
                        Rooms.quantity - func.coalesce(booked_rooms.c.count_booking, 0)
                    ).label("count_left_rooms"),
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.rooms_id, isouter=True)
                .cte()
            )

            get_all_hotels_rooms = (
                select(
                    Hotels.__table__.columns,
                    func.sum(left_rooms.c.count_left_rooms).label("count_left_rooms"),
                )
                .select_from(Hotels)
                .join(left_rooms, Hotels.id == left_rooms.c.hotel_id, isouter=True)
                .where(Hotels.location.like(f"%{location}%"))
                .group_by(Hotels.id)
                .having(func.sum(left_rooms.c.count_left_rooms) > 0)
            )

            all_hotels = await session.execute(get_all_hotels_rooms)
        return all_hotels.mappings().all()
