from app import GetBestRouteHelper
import json
import pytest


@pytest.fixture
def run_and_save_to_json(request):
    results = []

    def run_and_save(inputs):
        local_results = []  # Declare a local list for each test run

        for input_data in inputs:
            result = GetBestRouteHelper().find_best_route(input_data[0], input_data[1])
            local_results.append(result)

        # Save results to a local JSON file
        json_path = "results.json"
        with open(json_path, "a") as json_file:
            json.dump(local_results, json_file, indent=2)

        results.extend(local_results)

    return run_and_save


def test_route_calculation(run_and_save_to_json):
    input_list = [
        ("Paris, France", "Milano, Italy"),
        ("Freiburg, Germany", "Milano, Italy"),
        ("Paris, France", "Bratislava, Slovakia"),
        ("Helsinki, Finland", "Ljubljana, Slovenia"),
        ("Madrid, Spain", "Vilnius, Lithuania"),
        ("Rome, Italy", "Helsinki, Finland"),
        ("Berlin, Germany", "Lisbon, Portugal"),
        ("Prague, Czech Republic", "Lisbon, Portugal"),
        ("Warsaw, Poland", "Marseille, France"),
        ("Athens, Greece", "Brussel, Belgium"),
        ("Milano, Italy", "Berlin, Germany"),
        ("Dijon, France", "Vienna, Austria"),
        ("Lion, France", "Prague, Czech Republic"),
        ("Bratislava, Slovakia", "Valencia, Spain"),
        ("Ljubljana, Slovenia", "Paris, France"),
        ("Madrid, Spain", "Copenhagen, Denmark"),
        ("Budapest, Hungary", "Paris, France"),
        ("Madrid, Spain", "Freiburg, Germany"),
        ("Oslo, Norway", "Barcelona, Spain"),
        ("Stockholm, Sweden", "Lyon, France"),
    ]

    run_and_save_to_json(input_list)
