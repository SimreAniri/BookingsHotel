from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SRoomsInHotelDate(SRooms):
    total_cost: int
    count_left_rooms: int
