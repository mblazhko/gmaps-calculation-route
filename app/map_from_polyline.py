import os
from pprint import pprint
import json
import polyline
import folium

with open(os.path.join("..", "tests", "results.json"), "r") as f:
    results = json.load(f)

encoded_polyline = results[9]["polyline"]
decoded_polyline = polyline.decode(encoded_polyline)
map_route = folium.Map(
    location=[decoded_polyline[0][0], decoded_polyline[0][1]], zoom_start=10
)

folium.PolyLine(locations=decoded_polyline, color='blue').add_to(map_route)


if __name__ == "__main__":
    map_route.save('here_route_map.html')
    pprint(decoded_polyline)
