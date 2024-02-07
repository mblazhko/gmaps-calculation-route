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
        origin="Madrid, Spain", destination="Vilnius, Lithuania", waypoints=None
    )
    pprint(best)
