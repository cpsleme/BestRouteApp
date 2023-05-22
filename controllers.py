import re
import logging
from flask import jsonify

logging.basicConfig(filename="log/bestroute.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class Controllers:
    """
    Execute API requests
    input: An object with routes added from file
    """

    def __init__(self, routes_db):
        self.routes_db = routes_db

    @staticmethod
    def validrouteinput(new_route):
        """
        Check if route is valid
        """
        post_pattern = r"[A-Z]{3},[A-Z]{3},[\d]+$"
        route_valid = new_route['start'] + "," + new_route['finish'] + "," + str(new_route['cost'])
        if not bool(re.match(post_pattern, route_valid)):
            return False
        else:
            return True

    def querybestroute(self, route):
        """
        Return the best route from a get input
        """
        get_pattern = r"[A-Z]{3}-[A-Z]{3}$"
        route_upper = route.upper()
        if not bool(re.match(get_pattern, route_upper)):
            logging.error('Route invalid: ' + route_upper)
            return jsonify({'error': 'Enter a valid route, example: GRU-CDG'}), 400

        start, finish = route_upper.split("-")
        if start == finish:
            logging.error('Origin is equal destiny: ' + route_upper)
            return jsonify({'error': 'Origin is equal destiny, please enter a valid route.'}), 400
        else:
            result = self.routes_db.shortest_route(start, finish)
            if result is None:
                return jsonify({'error': 'Route not founded.'}), 404
            return jsonify(result)

    def createroute(self, new_route):
        """
        Create a new route in routes file
        """
        # Check input data        
        if not self.validrouteinput(new_route):
            logging.error('Origin is equal destiny: ' + new_route)
            return jsonify({'error': 'Enter a valid route, example: {"start":"GRU","finish":"ORL","cost":89}'}), 400

        inserted, message, code = self.routes_db.insertroute(new_route)
        if inserted:
            return jsonify({'success': 'Route added.'}), code
        else:
            return jsonify({'error': message}), code

    def updateroute(self, new_route):
        """
        Create a new route in routes file
        """
        # Check input data
        if not self.validrouteinput(new_route):
            logging.error('Origin is equal destiny: ' + new_route['start'] + "-" + new_route['finish'])
            return jsonify({'error': 'Enter a valid route, example: {"start":"GRU","finish":"ORL","cost":89}'}), 400

        updated, message, code = self.routes_db.updateroute(new_route)
        if updated:
            return jsonify({'success': 'Route updated.'}), code
        else:
            return jsonify({'error': message}), code

    def removeroute(self, route):
        """
        Create a new route in routes file
        """
        get_pattern = r"[A-Z]{3}-[A-Z]{3}$"
        route_upper = route.upper()
        if not bool(re.match(get_pattern, route_upper)):
            logging.error('Route invalid: ' + route_upper)
            return jsonify({'error': 'Enter a valid route, example: GRU-CDG'}), 400

        deleted, message, code = self.routes_db.deleteroute(route_upper)
        if deleted:
            return jsonify({'success': 'Route deleted.'}), code
        else:
            return jsonify({'error': message}), code
