import aiofiles
from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels")
async def add_hotel_images(name: int, file_to_load: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    async with aiofiles.open(im_path, "wb+") as file_obj:
        file = await file_to_load.read()
        await file_obj.write(file)
        await file_obj.flush()
    process_pic.delay(im_path)
