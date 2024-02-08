from time import time
from pprint import pprint

from app import GetBestRouteHelper


def main(origin, destination, waypoints):
    helper = GetBestRouteHelper()
    return helper.find_best_route(
        origin=origin, destination=destination, waypoints=waypoints
    )


if __name__ == "__main__":
    best = main(
        origin="Sarajevo,  Bosnia and Herzegovina", destination="Besançon, France", waypoints=None
    )
    pprint(best)
