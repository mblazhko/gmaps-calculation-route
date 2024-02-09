from pprint import pprint

from app import GetBestRouteHelper, get_route
import json
import pytest


@pytest.fixture
def run_and_save_to_json(request):
    results = []

    def run_and_save(inputs):
        local_results = []

        for input_data in inputs:
            result = get_route(input_data[0], input_data[1])
            local_results.append(result)

        json_path = "here_results.json"
        with open(json_path, "a") as json_file:
            json.dump(local_results, json_file, indent=2)

        results.extend(local_results)

    return run_and_save


def test_route_calculation(run_and_save_to_json):
    input_list = [
        ("60.4377703,26.7743319", "45.0735804,7.5932061"),
        ("47.3319205,4.9910196", "42.1442187,24.6584737"),
        ("47.9873966,7.7140197", "45.0735804,7.5932061"),
        ("47.7569579,8.7851771", "45.0735804,7.5932061"),
        ("47.7569579,8.7851771", "45.8899323,6.0873036"),
        ("45.4538818,8.5745815", "47.2602913,5.9298595"),
        ("47.2546749,4.6932274", "47.285542,11.2963896"),
        ("43.8836819,18.322742", "47.2602913,5.9298595"),
        ("48.155022,11.3770295", "43.280477,5.2158411"),
        ("59.4717596,24.5734352", "38.7441392,-9.2009354"),
        ("52.3547418,4.8215603", "45.4628246,9.0953318"),
        ("36.7649935,-4.5889975", "68.4253146,27.4113023"),
    ]

    run_and_save_to_json(input_list)
