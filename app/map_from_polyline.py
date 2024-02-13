import os
from concurrent.futures.thread import ThreadPoolExecutor
import json
import flexpolyline as fp
import polyline
import folium


class MapCreator:
    def create_map_from_polyline(self, polyline_type: str):
        if polyline_type == "google":
            self._simple_threads()
        elif polyline_type == "here":
            self._flex_threads()

    def _simple_threads(self):
        with open(
                os.path.join("..", "tests", "google_results.json"), "r"
        ) as google:
            gmaps_polylines = json.load(google)
        with ThreadPoolExecutor() as executor:
            executor.map(
                self._make_map_from_google,
                gmaps_polylines
            )

    def _flex_threads(self):
        with open(
                os.path.join("..", "tests", "here_results.json"), "r"
        ) as here:
            here_maps_polylines = json.load(here)
        with ThreadPoolExecutor() as executor:
            executor.map(
                self._create_map_from_flex_polyline,
                here_maps_polylines
            )

    @staticmethod
    def _create_map_from_flex_polyline(route: dict):
        map_route = folium.Map()
        for poly in route["polylines"]:
            decoded_polyline = fp.decode(poly)
            folium.PolyLine(
                locations=decoded_polyline, color="blue"
            ).add_to(map_route)

        file_name = f"{route["start_address"]}-{route["end_address"]}.html"
        save_path = os.path.join("..", "maps", "here", file_name)
        map_route.save(save_path)

    @staticmethod
    def _make_map_from_google(poly: dict):
        encoded_polyline = poly["polyline"]
        decoded_polyline = polyline.decode(encoded_polyline)

        map_route = folium.Map(
            location=[decoded_polyline[0][0], decoded_polyline[0][1]], zoom_start=20
        )
        folium.Marker(
            location=[decoded_polyline[0][0], decoded_polyline[0][1]]
        ).add_to(map_route)
        folium.Marker(
            location=[decoded_polyline[-1][0], decoded_polyline[-1][1]]
        ).add_to(map_route)
        folium.PolyLine(locations=decoded_polyline, color="blue").add_to(map_route)

        file_name = f"{poly["start_address"]}-{poly["end_address"]}.html".replace(
            " ", ""
        )
        save_path = os.path.join("..", "maps", "google", file_name)
        map_route.save(save_path)


if __name__ == "__main__":
    map_creator = MapCreator()
    map_creator.create_map_from_polyline("here")
