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

def get_split_arg(argName):
    result = request.args.get(argName, None)
    if result == None:
        return None
    return result.split(',')

@app.route("/network")
def networking():
    # This is currently setup to allow only one value for each (e.g.
    # Location = "Toronto, ON"). If extended, it would allow multiple
    # (e.g. Location = ["Toronto, ON", "Montreal, QC"])
    curr_user_id = int(request.args.get('curr_user_id'))
    connection_dists = [int(i) for i in request.args.get('connection_dist', '1').split(',')]
    professions = get_split_arg('profession')
    locations = get_split_arg('location')
    genders = get_split_arg('gender')
    age = request.args.get('age', None)  # string still needs to be parsed, e.g. "30-50"
    skills = get_split_arg('skills')
    languages = get_split_arg('languages')
    union_statuses = get_split_arg('union_status')  # id of status needs to be parsed e.g. "Union"
    filter = Network_Filter(curr_user_id, professions=professions, connection_dists=connection_dists,
                            locations=locations, genders=genders, age=age, skills=skills,
                            union_statuses=union_statuses, languages=languages)
    connections = get_network_connections(app, filter)
    return json.dumps({'connections': [c.__dict__ for c in connections]})


@app.route("/network/filters")
def get_network_filters():
    return json.dumps(network_filters)

@app.route("/user/<user_id>")
def get_user_from_id(user_id):
    user = get_user_by_id(app, user_id)
    user.connections = get_num_connections(app, user_id)
    user.socials = get_socials(app, user_id)
    user.demo_reels = get_demo_reels(app, user_id)
    user.education = [e.__dict__ for e in get_education(app, user_id)]
    user.skills = get_skills(app, user_id)
    user.ethnicities = get_ethnicities(app, user_id)
    user.media = get_user_media(app, user_id)
    user.appearance = [
     { 'title': 'Height', 'value': user.height },
     { 'title': 'Eye Color', 'value': user.eye_colour },
     { 'title': 'Weight', 'value': user.weight },
     { 'title': 'Hair Color', 'value': user.hair_colour },
     { 'title': 'Age Range', 'value': str(user.age_range_start) + '-' + str(user.age_range_end) },
    ]
    return json.dumps({ 'data': user.__dict__ })

@app.route("/credits/<user_id>")
def get_user_credits(user_id):
    credits = get_credits(app, user_id)
    return json.dumps({ 'data': [c.__dict__ for c in credits] })


@app.route("/posts/<post_id>")
def get_post_by_id(post_id):
    post = get_posts(app, [post_id])
    return json.dumps({'post': [p.__dict__ for p in post]}, default=str)


@app.route("/posts/user/<user_id>")
def get_post_by_user_id(user_id):
    post = get_users_posts(app, [user_id])
    return json.dumps({'post': [p.__dict__ for p in post]}, default=str)


@app.route("/posts/comments/<post_id>")
def get_comments_by_post_id(post_id):
    comments = get_post_comments(app, [post_id])
    return json.dumps({'comments': [c.__dict__ for c in comments]}, default=str)


@app.route("/comments/<comment_id>")
def get_comments_by_id(comment_id):
    comment = get_comments(app, [comment_id])
    return json.dumps({'comment': [c.__dict__ for c in comment]}, default=str)


if __name__ == "__main__":
    app.run()
