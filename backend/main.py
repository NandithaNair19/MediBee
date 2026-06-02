import logging
import time
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://medi-bee.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key-for-ci"))


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
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/search-by-pincode")
def search_by_pincode(data: PincodeRequest):
    start_time = time.time()

    logger.info(f"Received pincode search: {data.pincode}")

    pincode = data.pincode

    geocode_url = "https://api.geoapify.com/v1/geocode/search"
    geocode_params = {
        "text": pincode,
        "filter": "countrycode:in",
        "apiKey": GEOAPIFY_API_KEY,
    }

    logger.info("Calling Geoapify Geocoding API...")

    geo_response = requests.get(geocode_url, params=geocode_params)
    geo_data = geo_response.json()

    logger.info("Geocoding completed")

    if not geo_data.get("features"):
        logger.warning(f"Invalid pincode or location not found: {pincode}")
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

    logger.info("Searching nearby pharmacies...")

    places_response = requests.get(places_url, params=places_params)
    places_data = places_response.json()

    logger.info("Pharmacy search completed")

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
    logger.info(f"Stores before sorting: {[store['distance_km'] for store in stores]}")
    stores.sort(key=lambda store: float(store["distance_km"]))
    logger.info(f"Stores after sorting: {[store['distance_km'] for store in stores]}")
    end_time = time.time()

    logger.info(
        f"Found {len(stores)} stores in "
        f"{round(end_time - start_time, 2)} seconds"
    )

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

    logger.info(f"Whisper Output: {text}")

    match = re.search(r"\b\d{6}\b", text)

    if not match:
        logger.warning("No valid pincode detected from voice input")
        return {"error": "No valid pincode detected"}

    pincode = match.group()

    return search_by_pincode(PincodeRequest(pincode=pincode))

    