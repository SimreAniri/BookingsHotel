from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Computed, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в
    # PyCharm и VSCode
    from app.hotels.rooms.models import Rooms
    from app.users.models import Users


class Bookings(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to-date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to-date_from"))

    user: Mapped["Users"] = relationship(back_populates="booking")
    room: Mapped["Rooms"] = relationship(back_populates="bookings")

    def __str__(self):
        return f"Booking #{self.id}"
