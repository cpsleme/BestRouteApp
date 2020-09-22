import sys
import re
from model import GraphBase


def output_bestroute(origin, result_input):
    """
    Print origin and best route result
    input: origin, result
    output: formatted best route
    """
    if len(result_input) == 0:
        return "No routes founded."

    separator = " - "
    result_print = ""
    for item in result_input["Path"]:
        if result_print == "":
            result_print = item
        else:
            result_print = result_print + separator + item

    result_print = result_print + " > $" + str(result_input["Cost"])

    return result_print


if __name__ == '__main__':

    parameters = sys.argv
    if len(parameters) < 2:
        print(f"Please, type: python cli.py <file.csv>")
        sys.exit(0)

    if parameters[1] in ['help', '-h', '--help']:
        print(f"Please, type: python cli.py <file.csv>")
        sys.exit(0)

    # Test and load files
    filecsv = parameters[1]
    #filecsv = 'routesdb.csv'
    route_db = GraphBase(filecsv)

    if not route_db.conn() or not route_db.hasvertices():
        print(f"Please, type a valid csv file.")
        sys.exit(0)
    else:

        print(f"Initial routes added from file {filecsv}.")
        input_pattern = r"[A-Z]{3}-[A-Z]{3}$"

        # Infinite looping for input routes
        while 1:

            input_route = input("please enter the route (bye to exit): ")

            if input_route.lower() == "bye":
                sys.exit()

            input_route = input_route.upper()
            if bool (re.match(input_pattern, input_route)):
                start, finish = input_route.split("-")
                if start == finish:
                    print ("Origin is equal destiny, please enter a valid route.")
                else:
                    result = route_db.shortest_route(start, finish)
                    print (output_bestroute(finish, result))

            else:
                print("")
                print("please enter a route, example: GRU-CDG")


