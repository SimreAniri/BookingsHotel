import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("date_from,date_to,status_code", [
    ("2030-05-01", "2030-05-15", 200),
    ("2030-05-02", "2030-05-16", 200),
    ("2030-05-03", "2030-04-17", 400),
    ("2030-05-04", "2030-05-04", 400),
])
async def test_get_hotels(
    date_from, date_to, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get("/hotels", params={
        "location": "Altay",
        "date_from": date_from,
        "date_to": date_to
        })

    assert response.status_code == status_code
