from datetime import date
from sqlalchemy import and_, func, or_, select

from app.database import async_session_maker

from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def left_rooms(cls, hotel_id: int, date_from: date, date_to: date):
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

            get_left_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * (date_to - date_from).days).label("total_cost"),
                    (
                        Rooms.quantity - func.coalesce(booked_rooms.c.count_booking, 0)
                    ).label("count_left_rooms"),
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.rooms_id, isouter=True)
                .where(
                    and_(
                        Rooms.hotel_id == hotel_id,
                        (
                            Rooms.quantity
                            - func.coalesce(booked_rooms.c.count_booking, 0)
                        )
                        > 0,
                    )
                )
            )

            left_rooms = await session.execute(get_left_rooms)

        return left_rooms.mappings().all()
