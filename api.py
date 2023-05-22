import sys
import json
from model import GraphBase
from controllers import Controllers
from flask import Flask, request

# Load database
routes_db = GraphBase()
if not routes_db.conn():
    print("Database is not accessible, please, verify configuration.")
    sys.exit(0)

if not routes_db.conn():
    print("Database error.")
    sys.exit(0)

# Define flask server
app = Flask(__name__)
root = '/api/v1'


@app.route(root + '/check/<string:path>', methods=['GET'])
def query_bestroute(path):
    # Check the best route
    query = Controllers(routes_db)
    # Return a json with result
    response = query.querybestroute(path)
    return response


@app.route(root + '/add', methods=['POST'])
def add_route():
    # Create new route
    new_route = json.loads(request.data)
    command = Controllers(routes_db)
    # Return if route was added or not
    response = command.createroute(new_route)
    if response[1] == 201:
        routes_db.reload()
    return response


@app.route(root + '/update', methods=['PUT'])
def update_route():
    # Update route
    new_route = json.loads(request.data)
    command = Controllers(routes_db)
    # Return a response if route was added or not
    response = command.updateroute(new_route)
    if response[1] == 200:
        routes_db.reload()
    return response


@app.route(root + '/remove/<string:route>', methods=['DELETE'])
def delete_route(route):
    # Remove route
    query = Controllers(routes_db)
    # Return a json with result
    response = query.removeroute(route)
    if response[1] == 200:
        routes_db.reload()
    return response


# Main method
if __name__ == '__main__':
    print("Server: 0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=True)
