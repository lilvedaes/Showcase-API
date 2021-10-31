from flask import Flask, request
from mysql_setup import setup_database
from mysql_insertion import *
from constants import *
import json

app = Flask(__name__)

# MySQL configuration
setup_database(app)
add_sample_data(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/network")
def networking():
    curr_user_id = int(request.args.get('curr_user_id'))
    connection_dist = int(request.args.get('connection_dist'))
    connections = get_network_connections(app, curr_user_id, connection_dist)
    return json.dumps({ 'connections': [c.__dict__ for c in connections]})

@app.route("/network/filters")
def get_network_filters():
    return json.dumps(network_filters)


if __name__ == "__main__":
    app.run()
