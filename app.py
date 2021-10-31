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
    # This is currently setup to allow only one value for each (e.g.
    # Location = "Toronto, ON"). If extended, it would allow multiple
    # (e.g. Location = ["Toronto, ON", "Montreal, QC"])
    curr_user_id = int(request.args.get('curr_user_id'))
    connection_dist = int(request.args.get('connection_dist', 1))
    profession = request.args.get('profession', None)
    location = request.args.get('location', None)
    gender = request.args.get('gender', None)
    age = request.args.get('age', None)  # string still needs to be parsed, e.g. "30-50"
    skills = request.args.get('skills', None)
    languages = request.args.get('languages', None)
    union_status = request.args.get('union_status', None) # id of status needs to be parsed e.g. "Union"
    filter = Network_Filter(curr_user_id, profession=profession, connection_dist=connection_dist,
                            location=location,gender=gender, age=age, skills=skills,
                            union_status=union_status, languages=languages)
    connections = get_network_connections(app, filter)
    return json.dumps({ 'connections': [c.__dict__ for c in connections]})

@app.route("/network/filters")
def get_network_filters():
    return json.dumps(network_filters)


if __name__ == "__main__":
    app.run()
