from xmlrpc.client import Boolean
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from random import seed
from random import randint

seed(1)

LICENSE_PLATE_LIST = ["B1MAN", "B1234CDA", "B6703WJF", "B7070UH", "B1496YA", "B1545SZS", "W1430TG", "W1421W", "W1767XZ", "N1468C"]
VEHICLE_TYPE = ["CAR", "MOTORCYCLE", "BUS", "TRUCK"]

hostIpAddr = "101.50.3.207"

app_desc = """
Percik App as the server<br><br>
Testwin send a GET request to receive list of licence plates of vehicles that neet to be tested<br>
Use "licensePlateAvailable" query to simulate whether a new list of licenseplate is available or not<br>
<br>
Testwin send a POST request to send vehicle test result to the server, using similar key number format as Testwin In & Out Files Description (but added 'D_' before the key)<br> 
by Hilmy Izzulhaq"""

konsol = FastAPI(
    title="PERCIK - TESTWIN INTEGRATION API DUMMY",
    description=app_desc,
    version="0.0.1",
    contact={
        "name": "Hilmy Izzulhaq",
        "email": "halogas.ijul@gmail.com",
    },
)

class konsolDataA(BaseModel):
    D_10100 : str
    DATAOUT : str
    class Config:
        schema_extra = {
            "example": {
                "D_10050": "TEST021923",
                "D_10100": "B1234CDA",
                "D_10121": "23/10/02",
                "D_10190": 2,
                "D_10191": 2,
                "D_15010": "Felipe",
                "DATAOUT": "DATAOUT",
                "D_40000": 2.69,
                "D_40001": 1.99,
                "D_40010": 25,
                "D_40011": 35,
                "D_40050": 70,
            }
        }


@konsol.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@konsol.get("/license-plate", tags=["Get new license plate"])
async def get_licenseplate(licensePlateAvailable : Boolean):
    value1 = randint(0, 7)
    value2 = randint(0, 2)
    listLp = []
    i = 0
    while i <= value2:
        listLp.append(LICENSE_PLATE_LIST[(value1 + i)])
        i += 1
    jumlahNopol = 0
    dictOut = {}
    for platnom in listLp:
        value3 = randint(0, 3)
        jumlahNopol += 1
        dictOutKey = str(jumlahNopol)
        dictOut[dictOutKey] = {
            'license-plate':platnom,
            'vehicle-type':VEHICLE_TYPE[value3]
        }

    if licensePlateAvailable:
        results = {"result": dictOut}
    else:
        results = {"license-plate": "UNAVAILABLE"}
    return results

@konsol.post("/konsol-data", tags=["Receive console data"])
async def receive_data(itemConsole : konsolDataA):
    dictOutput = {
        'status':"received",
        'license-plate':itemConsole.D_10100,
    }
    return dictOutput


if __name__ == "__main__":
    uvicorn.run(konsol, debug=True, host=hostIpAddr, port=8000, headers=[("server", "arsa-ai_server-1")])