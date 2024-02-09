import os
from concurrent.futures.thread import ThreadPoolExecutor
import json
import flexpolyline as fp
import polyline
import folium


class MapCreator:
    FLEX = "flex",
    SIMPLE = "simple"

    def create_map_from_polyline(self, polylines, polyline_type: str):
        if polyline_type == "simple":
            with ThreadPoolExecutor() as executor:
                executor.map(self._make_map_from_google, polylines)
        else:
            with ThreadPoolExecutor() as executor:
                executor.map(self._create_map_from_flex_polyline, polylines)

    @staticmethod
    def _create_map_from_flex_polyline(route: dict):
        poly = route["polyline"]
        decoded_polyline = fp.decode(poly)
        map_route = folium.Map(
            location=[decoded_polyline[0][0], decoded_polyline[0][1]], zoom_start=20
        )
        folium.PolyLine(locations=decoded_polyline, color="blue").add_to(map_route)
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
    # with open(os.path.join("..", "tests", "google_results.json"), "r") as f:
    #     results = json.load(f)
    # create_map_from_polyline(results)

    with open(os.path.join("..", "tests", "here_results.json"), "r") as f:
        results = json.load(f)
    map_creator.create_map_from_polyline(results, "flex")
