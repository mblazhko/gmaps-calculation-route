from pprint import pprint

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
        json_path = "google_results.json"
        with open(json_path, "a") as json_file:
            json.dump(local_results, json_file, indent=2)

        results.extend(local_results)

    return run_and_save


def test_route_calculation(run_and_save_to_json):
    input_list = [
        ("Kotka, Finland", "Torino, Italy"),
        ("Dijon, France", "Plovdiv, Bulgaria"),
        ("Freiburg, Germany", "Torino, Italy"),
        ("Singen, Germany", "Torino, Italy"),
        ("Singen, Germany", "Annecy, France"),
        ("Novara, Italy", "Besancon, France"),
        ("Chamber, France", "Innsbruck, Austria"),
        ("Sarajevo,  Bosnia and Herzegovina", "Besancon, France"),
        ("Munich,  Germany", "Marseille, France"),
        ("Tallinn,  Estonia", "Lisbon, Portugal"),
        ("Amsterdam,  Netherlands", "Milano, Italy"),
        ("Malaga,  Spain", "Saariselka, Finland"),
    ]

    run_and_save_to_json(input_list)
