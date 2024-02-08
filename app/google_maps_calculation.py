import time

import folium
from googlemaps import Client
from config import GOOGLE_MAPS_API_KEY


class GetBestRouteHelper:
    INNSBRUCK = ["via:Innsbruck, Austria"]
    LION = ["via:Lion, France"]
    BEAUNE = ["via:Beaune, France"]
    TOTAL_REQUESTS = 0

    def __init__(
        self,
        *,
        alternatives: bool = True,
        avoidable_country: str = "Switzerland",
        waypoints: list[str] | None = None
    ):
        self._alternatives: bool = alternatives
        self._waypoints: list[str] | None = waypoints
        self._avoidable_country: str = avoidable_country
        self._routes: list[dict] | dict | None = None
        self._client: Client = Client(key=GOOGLE_MAPS_API_KEY)

    def find_best_route(
        self,
        origin: str | dict,
        destination: str | dict,
        waypoints: list[str] | None = None,
    ) -> dict:
        start_time = time.time()
        self._get_routes(origin, destination, waypoints)
        self._routes = self._check_if_country_exists()

        if self._routes:
            best_route = min(
                self._routes, key=lambda route: route["legs"][0]["duration"]["value"]
            )
            route_info = best_route["legs"][0]
            end_time = time.time() - start_time
            result = {
                "total_calculation_time": end_time,
                "total_requests": GetBestRouteHelper.TOTAL_REQUESTS,
                "distance": route_info["distance"]["text"],
                "duration": route_info["duration"]["text"],
                "start_address": route_info["start_address"],
                "end_address": route_info["end_address"],
                "polyline": best_route["overview_polyline"]["points"],
            }
            return result
        else:
            return self.find_best_route(
                origin=origin,
                destination=destination,
                waypoints=(
                    GetBestRouteHelper.BEAUNE
                    if "France" in destination or "France" in origin
                    else GetBestRouteHelper.INNSBRUCK
                ),
            )

    def _get_routes(
        self, origin: str | dict, destination: str | dict, waypoints: list[str] | None
    ) -> None:
        GetBestRouteHelper.TOTAL_REQUESTS += 1
        self._routes = self._client.directions(
            origin=origin,
            destination=destination,
            waypoints=waypoints,
            alternatives=self._alternatives,
            mode="driving",
        )

    def _check_if_country_exists(self) -> list[dict]:
        routes_without_country = []
        for route in self._routes:
            country_exists = self._check_one_route(route)
            if country_exists:
                continue
            routes_without_country.append(route)

        return routes_without_country

    def _check_one_route(self, route: dict):
        steps = route["legs"][0]["steps"]

        for location in steps:
            if self._avoidable_country in location["html_instructions"]:
                return True

    @staticmethod
    def _save_map_html(route: dict):
        start_location = route["legs"][0]["start_location"]
        map_route = folium.Map(
            location=[start_location["lat"], start_location["lng"]], zoom_start=10
        )
        legs = route["legs"][0]["steps"]

        for step in legs:
            folium.Marker(
                location=[
                    step["start_location"]["lat"],
                    step["start_location"]["lng"],
                ],
                popup=step["html_instructions"],
            ).add_to(map_route)

        polyline_points = [
            (step["start_location"]["lat"], step["start_location"]["lng"])
            for step in legs
        ]
        folium.PolyLine(locations=polyline_points, color="blue").add_to(map_route)

        map_route.save("google_route_map.html")
