from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import re
from fastapi.middleware.cors import CORSMiddleware
from math import radians, sin, cos, sqrt, atan2

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(R * c, 2)


class PincodeRequest(BaseModel):
    pincode: str
    user_lat: float | None = None
    user_lon: float | None = None


@app.get("/")
def home():
    return {"message": "Medical Store Locator API is running"}


@app.post("/search-by-pincode")
def search_by_pincode(data: PincodeRequest):
    pincode = data.pincode

    geocode_url = "https://api.geoapify.com/v1/geocode/search"
    geocode_params = {
        "text": pincode,
        "filter": "countrycode:in",
        "apiKey": GEOAPIFY_API_KEY,
    }

    geo_response = requests.get(geocode_url, params=geocode_params)
    geo_data = geo_response.json()

    if not geo_data.get("features"):
        return {"error": "Invalid pincode or location not found"}

    location = geo_data["features"][0]["geometry"]["coordinates"]
    lon = location[0]
    lat = location[1]

    places_url = "https://api.geoapify.com/v2/places"
    places_params = {
        "categories": "healthcare.pharmacy",
        "filter": f"circle:{lon},{lat},5000",
        "bias": f"proximity:{lon},{lat}",
        "limit": 10,
        "apiKey": GEOAPIFY_API_KEY,
    }

    places_response = requests.get(places_url, params=places_params)
    places_data = places_response.json()

    stores = []

    for place in places_data.get("features", []):
        props = place.get("properties", {})

        store_lat = props.get("lat")
        store_lon = props.get("lon")

        if store_lat is None or store_lon is None:
            continue

        if data.user_lat is not None and data.user_lon is not None:
            distance = calculate_distance(
                data.user_lat,
                data.user_lon,
                store_lat,
                store_lon
            )
        else:
            distance = calculate_distance(lat, lon, store_lat, store_lon)

        stores.append({
            "name": props.get("name", "Unnamed Medical Store"),
            "address": props.get("formatted", "Address not available"),
            "distance_km": distance,
            "map_link": f"https://www.google.com/maps/search/?api=1&query={store_lat},{store_lon}",
        })

    return {
        "pincode": pincode,
        "latitude": lat,
        "longitude": lon,
        "stores": stores,
    }


@app.post("/search-by-voice")
async def search_by_voice(audio: UploadFile = File(...)):
    temp_file = f"temp_{audio.filename}"

    with open(temp_file, "wb") as buffer:
        buffer.write(await audio.read())

    with open(temp_file, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    os.remove(temp_file)

    text = transcript.text.replace(" ", "")

    print("Whisper Output:", text)

    match = re.search(r"\b\d{6}\b", text)

    if not match:
        return {"error": "No valid pincode detected"}

    pincode = match.group()

    return search_by_pincode(PincodeRequest(pincode=pincode))