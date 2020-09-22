import heapq
import logging
import os
import re
import sys

logging.basicConfig(filename="log/bestroute.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class GraphBase:

    def __init__(self, filedb=None):
        db_location = filedb
        if filedb is not None:
            db_location = filedb
        else:
            try:
                with open('database.ini') as f:
                    content = f.readlines()[0].rstrip('\n')
                    if len(content) > 0:
                        db_location = content
                        if not os.path.isfile(db_location):
                            db_location = None

                f.close()
            except Exception as e:
                print("Database config not accessible." + e)
                logging.error("Database config not accessible." + e)

        self.filedb = db_location
        self.vertices = self.loadallvertices()
        self.spa_result = dict()

    def conn(self):
        """
        Verify if file is valid with mask: OOO,DDD,999
        """
        if self.filedb is None:
            return False
        line_pattern = r"[A-Z]{3},[A-Z]{3},[\d]+$"
        with open(self.filedb) as f:
            try:
                for line in f:
                    line = line.rstrip('\n\r').upper()
                    if not bool(re.match(line_pattern, line)):
                        logging.error("Database error. Line: " + line)
                        return False
                return True
            except Exception as e:
                logging.error('Database is not accessible.' + e)
                return False

    def commandroute(self, operation, lines, updatedline=None):
        """
        Insert, update and delete routes
        """
        if operation == 'Insert':
            fileoperation = "a"
        else:
            fileoperation = "w"
        try:
            with open(self.filedb, fileoperation) as f:
                if operation == 'Insert':
                    f.write("\r")
                    f.write(updatedline)
                    code = 201
                else:
                    for line in lines:
                        if line != "":
                            f.write(line)
                            f.write("\r")
                    if updatedline is not None and operation != 'Delete':
                        f.write(updatedline)
                    code = 200
                message = operation + ' ok: ' + updatedline
                logging.info(message)
                f.close()
                return False, message, code
        except Exception as e:
            logging.error('Database is not accessible.' + e)
            return True, 'Database is not accessible', 503

    def selectroute(self, route_key):
        """
        Verify if route exists
        """
        with open(self.filedb, 'r') as f:
            try:
                lines = list()
                routeexists = False
                code = 200
                message = 'Route does not exists'
                for line in f:
                    line = line.rstrip('\n\r').upper()
                    if line[0:7] == route_key:
                        routeexists = True
                        message = 'Route exists.'
                        code = 400
                    else:
                        if lines != "":
                            lines.append(line)
            except Exception as e:
                logging.error('Database is not accessible.' + e)
                return True, False, 'Database is not accessible.', 503, []

        return False, routeexists, message, code, lines

    def reload(self):
        """
        Verify if file is valid with mask: OOO,DDD,999
        """
        self.vertices = self.loadallvertices()

    def hasvertices(self):
        """
        Return number of vertices in database
        """
        if len(self.vertices) > 0:
            return True
        else:
            return False

    def getallvertices(self):
        return self.vertices

    def loadallvertices(self):
        """
        Create the vertices to shortest path algorithm
        """
        if self.filedb is None:
            return
        vertices = dict()
        line_pattern = r"[A-Z]{3},[A-Z]{3},[\d]+$"
        try:
            with open(self.filedb) as f:
                for line in f:
                    # Recover origin, destiny and cost
                    if bool(re.match(line_pattern, line)):
                        start, finish, cost = line.rstrip('\n\r').split(",")
                        # Create route entry
                        route = {finish: int(cost)}
                        origin_dict = vertices.get(start)
                        if origin_dict is not None:
                            origin_dict.update(route)
                            vertices[start] = origin_dict
                        else:
                            vertices[start] = route

            with open(self.filedb) as f:
                for line2 in f:
                    if bool(re.match(line_pattern, line2)):
                        # Recover origin, destiny and cost
                        start, finish, cost = line2.rstrip('\n\r').split(",")
                        # Finish must be a vertice also
                        if vertices.get(finish) is None:
                            vertices[finish] = {finish: 0}

        except Exception as e:
            logging.error("File open error." + e)
            return None

        return vertices

    def shortest_route(self, start, finish):
        """
        Calculate the shortest path
        """
        distances = dict()
        previous = dict()
        nodes = list()
        result = dict()
        best_price = 0

        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == finish:
                path = []
                while previous[smallest]:
                    path.append(smallest)
                    smallest = previous[smallest]
                if len(path) == 1:
                    result["Cost"] = distances[finish]
                else:
                    result["Cost"] = best_price

                if len(path) > 0:
                    path.append(start)
                    result["Path"] = path[::-1]
                else:
                    result = dict()

                self.spa_result = result
                return result

            if distances[smallest] == sys.maxsize:
                break

            for neighbor in self.vertices[smallest]:
                cost = distances[smallest] + self.vertices[smallest][neighbor]
                if cost < distances[neighbor]:
                    distances[neighbor] = cost
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = cost
                            best_price = cost
                            break
                    heapq.heapify(nodes)

        return result

    def insertroute(self, new_route):
        """
        Create a new route in csv file
        """
        route_key = new_route['start'] + "," + new_route['finish']
        error, exists, message, code, lines = self.selectroute(route_key)
        if error or exists:
            return False, message, code
        else:
            new_route_line = new_route['start'] + "," + new_route['finish'] + "," + str(new_route['cost'])
            error, message, code = self.commandroute('Insert', lines, new_route_line)
            if not error:
                return True, message, 201
            else:
                return False, message, code

    def updateroute(self, new_route):
        """
        Update a route in csv file
        """
        # Check if route already exists
        route_key = new_route['start'] + "," + new_route['finish']
        error, exists, message, code, lines = self.selectroute(route_key)
        if error or not exists:
            return False, message, code
        else:
            update_route_line = new_route['start'] + "," + new_route['finish'] + "," + str(new_route['cost'])
            error, message, code = self.commandroute('Update', lines, update_route_line)
            if not error:
                return True, message, 200
            else:
                return False, message, code

    def deleteroute(self, new_route):
        """
        Delete a route in csv file
        """
        route_key = new_route.replace('-', ',')
        error, exists, message, code, lines = self.selectroute(route_key)
        if error or not exists:
            return False, message, code
        else:
            error, message, code = self.commandroute('Delete', lines, route_key)
            if not error:
                return True, message, 200
            else:
                return False, message, code

    def __str__(self):
        return str(self.vertices)
