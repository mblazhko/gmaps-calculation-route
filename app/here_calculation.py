import json
import time
from pprint import pprint

import httpx
from config import HERE_API_KEY


class HereMapsCalculating:
    def __init__(self):
        self._api_key = HERE_API_KEY

    def get_route(self, origin: str, destination: str):
        with self._make_client() as client:
            start_time = time.time()
            url = "https://router.hereapi.com/v8/routes"
            payload = self._get_routes_payload(origin, destination)

            headers = self._get_headers()

            response = client.get(url, params=payload, headers=headers)
            end_time = time.time() - start_time
            response = response.json()

        duration = 0
        distance = 0
        polylines = []

        for section in response["routes"][0]["sections"]:
            duration += section["summary"]["duration"]
            distance += section["summary"]["length"]
            polylines.append(section["polyline"])

        result = {
            "total_calculation_time": end_time,
            "distance": f"{round(distance/1000, 2)} km",
            "duration": f"{round(duration/3600, 2)} hours",
            "start_address": origin,
            "end_address": destination,
            "polylines": polylines,
        }

        return result

    def _get_routes_payload(self, origin, destination) -> dict:
        origin_geocode = self.get_geocode_by_address(origin)
        destination_geocode = self.get_geocode_by_address(destination)

        payload = {
            "apiKey": self._api_key,
            "transportMode": "car",
            "origin": origin_geocode,
            "destination": destination_geocode,
            "exclude[countries]": "CHE,RUS,BLR",
            "return": "polyline,summary",
            "alternatives": 0,
        }

        return payload

    def _get_headers(self):
        return {"apiKey": self._api_key, "ContentType": "application/json"}

    def get_geocode_by_address(self, address: str) -> str:
        url = "https://geocode.search.hereapi.com/v1/geocode"
        with self._make_client() as client:
            headers = self._get_headers()
            payload = {
                "apiKey": self._api_key,
                "q": address
            }

            response = client.get(url, headers=headers, params=payload)
            data = response.json()

            return f"{data["items"][0]["position"]["lat"]},{data["items"][0]["position"]["lng"]}"

    @staticmethod
    def _make_client():
        return httpx.Client()


# Usage Example
if __name__ == '__main__':
    here_maps = HereMapsCalculating()
    result = here_maps.get_route(
        destination="Kotka, Finland",
        origin="Torino, Italy"
    )

    with open("here.json", "w") as f:
        json.dump(result, f, indent=2)
