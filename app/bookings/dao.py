from datetime import date

from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.__table__.columns,
                    Rooms.image_id.label("rooms_image"),
                    Rooms.name.label("rooms_name"),
                    Rooms.description.label("rooms_description"),
                    Rooms.services.label("rooms_services"),
                )
                .filter_by(user_id=user_id)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
            )
            result = await session.execute(query)
            print(result)
        return result.mappings().all()

    @classmethod
    def rooms_left(cls, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """

        booked_rooms = (
            select(Bookings)
            .where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_from >= date_from,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_from < date_from,
                        ),
                    ),
                )
            )
            .cte("booked_rooms")
        )

        """
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        get_rooms_left = (
            select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                    "rooms_left"
                )
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.id == room_id)
            .group_by(Rooms.quantity, booked_rooms.c.room_id)
        )

        return get_rooms_left

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):

        async with async_session_maker() as session:
            get_rooms_left = BookingDAO.rooms_left(room_id, date_from, date_to)

            rooms_left_raw = await session.execute(get_rooms_left)
            rooms_left: int = (rooms_left_raw.scalar() or 0)

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
