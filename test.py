import requests
from model import GraphBase

inputfile = "data/input-routes-test.csv"
inputinvalidfile = "data/input-routes-test-invalid.csv"


class TestBestRoute:

    def test_cli_validroute(self):
        """
        Test a valid route
        """
        correct_result = {'Path': ['GRU', 'BRC', 'SCL', 'ORL', 'CDG'], 'Cost': 40}
        route_db = GraphBase(inputfile)
        result = route_db.shortest_route("GRU", "CDG")
        assert result == correct_result

    def test_cli_invalidroute(self):
        """
        Test an invalid route
        """
        correct_result = {}
        route_db = GraphBase(inputfile)
        result = route_db.shortest_route('XXX', 'YYY')
        assert result == correct_result

    def test_rest_validroute(self):
        """
        Test a rest request with a valid route
        """
        correct_result = {'Path': ['GRU', 'BRC', 'SCL', 'ORL', 'CDG'], 'Cost': 40}
        url = "http://localhost:3000/api/v1/check/GRU-CDG"
        response = requests.get(url)
        result = response.json()
        assert result == correct_result

    def test_rest_invalidroute(self):
        """
        Test a rest request with an invalid route
        """
        correct_result = {}
        url = "http://localhost:3000/api/v1/check/OOO-DDD"
        response = requests.get(url)
        result = response.json()
        assert result == correct_result

    def test_rest_addroute(self):
        """
        Test a rest request to add a route
        """
        correct_result = 201
        add_json = {'start': 'LLL', 'finish': 'MMM', 'cost': 14}
        add_url = "http://localhost:3000/api/v1/add"
        response = requests.post(url=add_url, json=add_json)
        result = response.status_code
        assert result == correct_result

    def test_rest_updateroute(self):
        """
        Test a rest request to update a route
        """
        correct_result = 200
        update_json = {'start': 'LLL', 'finish': 'MMM', 'cost': 15}
        update_url = "http://localhost:3000/api/v1/update"
        response = requests.put(url=update_url, json=update_json)
        result = response.status_code
        assert result == correct_result

    def test_rest_deleteroute(self):
        """
        Test a rest request to delete a route
        """
        correct_result = 200
        delete_url = "http://localhost:3000/api/v1/remove/LLL-MMM"
        response = requests.delete(delete_url)
        result = response.status_code
        assert result == correct_result
