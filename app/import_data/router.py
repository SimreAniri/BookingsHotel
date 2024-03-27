import codecs
import csv
from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/import",
    tags=["Импорт данных"]
)

@router.post("/hotels")
async def add_hotels(file: UploadFile):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'Windows-1251'), delimiter=';')
    data = {}
    for rows in csvReader:             

        print(rows)

    
    file.file.close()
    return data