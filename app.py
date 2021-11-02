from flask import Flask, request
from mysql_setup import setup_database
from mysql_insertion import *
from constants import *
import json

app = Flask(__name__)

# MySQL configuration
setup_database(app)
add_sample_data(app)
add_sample_posts_with_comments(app)


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
    union_status = request.args.get('union_status', None)  # id of status needs to be parsed e.g. "Union"
    filter = Network_Filter(curr_user_id, profession=profession, connection_dist=connection_dist,
                            location=location, gender=gender, age=age, skills=skills,
                            union_status=union_status, languages=languages)
    connections = get_network_connections(app, filter)
    return json.dumps({'connections': [c.__dict__ for c in connections]})


@app.route("/network/filters")
def get_network_filters():
    return json.dumps(network_filters)


@app.route("/posts/<post_id>")
def get_post_by_id(post_id):
    post = get_posts(app, [post_id])
    return json.dumps({'post': [p.__dict__ for p in post]}, default=str)


@app.route("/posts/user/<user_id>")
def get_post_by_user_id(user_id):
    post = get_users_posts(app, [user_id])
    return json.dumps({'post': [p.__dict__ for p in post]}, default=str)


@app.route("/posts/<post_id>/comments")
def get_comments_by_post_id(post_id):
    comments = get_post_comments(app, [post_id])
    return json.dumps({'comments': [c.__dict__ for c in comments]}, default=str)


@app.route("/comments/<comment_id>")
def get_comments_by_id(comment_id):
    comment = get_comments(app, [comment_id])
    return json.dumps({'comment': [c.__dict__ for c in comment]}, default=str)


if __name__ == "__main__":
    app.run()
