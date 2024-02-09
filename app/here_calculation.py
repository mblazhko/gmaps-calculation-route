import json
import time
import httpx
from config import HERE_API_KEY


def get_route(origin: str, destination: str):
    with httpx.Client() as client:
        start_time = time.time()
        url = "https://router.hereapi.com/v8/routes"
        payload = {
            "apiKey": HERE_API_KEY,
            "transportMode": "car",
            "origin": origin,
            "destination": destination,
            "exclude[countries]": "CHE,RUS,BLR",
            "return": "polyline,summary",
            "avoid[features]": "ferry",
            "alternatives": 0,
        }

        headers = {"apiKey": HERE_API_KEY, "ContentType": "application/json"}

        response = client.get(url, params=payload, headers=headers)
        end_time = time.time() - start_time
        response = response.json()

    end_address = response["routes"][0]["sections"][0]["arrival"]["place"]["location"]
    start_address = response["routes"][0]["sections"][0]["departure"]["place"]["location"]

    result = {
        "total_calculation_time": end_time,
        "distance": f"{round(
            response["routes"][0]["sections"][0]["summary"]["length"]/1000, 2
        )} km",
        "duration": f"{round(
            response["routes"][0]["sections"][0]["summary"]["duration"]/3600, 2
        )} hours",
        "start_address": f"{start_address["lat"]},{start_address["lng"]}",
        "end_address": f"{end_address["lat"]},{end_address["lng"]}",
        "polyline": response["routes"][0]["sections"][0]["polyline"],
    }

    return result


if __name__ == '__main__':
    result = get_route(
        destination="45.0702306,7.5876887",
        origin="60.4377703,26.7743319"
    )

    with open("here.json", "w") as f:
        json.dump(result, f, indent=2)
