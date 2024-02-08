import os
from concurrent.futures.thread import ThreadPoolExecutor
from pprint import pprint
import json
import polyline
import folium


def make_map(poly):
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
    save_path = os.path.join("..", "maps", file_name)
    map_route.save(save_path)


def create_map_from_polyline(polylines):
    with ThreadPoolExecutor() as executor:
        executor.map(make_map, polylines)


if __name__ == "__main__":
    with open(os.path.join("..", "tests", "results.json"), "r") as f:
        results = json.load(f)
    create_map_from_polyline(results)
