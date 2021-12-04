from flask import Flask, request
from flask_cors import CORS
from mysql_setup import setup_database
from mysql_insertion import *
from constants import *
import json
from imdb_add import create_user_from_imdb

app = Flask(__name__)
CORS(app)

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
    user.headshots = get_headshots(app, user_id)
    user.appearance = [
     { 'title': 'Height', 'value': user.height },
     { 'title': 'Eye Color', 'value': user.eye_colour },
     { 'title': 'Weight', 'value': user.weight },
     { 'title': 'Hair Color', 'value': user.hair_colour },
     { 'title': 'Age Range', 'value': str(user.age_range_start) + '-' + str(user.age_range_end) },
    ]
    return json.dumps({ 'data': user.__dict__ })

@app.route('/updateHeadshot', methods=["POST"])
def update_headshot():
    request_data = json.loads(request.data)
    user_id = request_data.get('user_id', None)
    headshot = request_data.get('type', None)
    priority = request_data.get('priority', None)
    update_headshot(app, user_id, headshot, priority)
    return json.dumps({'success': True})

@app.route("/credits/<user_id>")
def get_user_credits(user_id):
    credits = get_credits(app, user_id)
    return json.dumps({ 'data': [c.__dict__ for c in credits] })

@app.route("/feed/<user_id>")
def get_feed_for_user(user_id):
    feed = get_user_feed(app, user_id)
    return json.dumps(feed)

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

@app.route("/connection/request/<user_id>/<user_requested>")
def connection_request(user_id, user_requested):
    connection_added = add_connection_request(app, user_id, user_requested)
    return json.dumps(connection_added)

@app.route("/connection/confirm/<user_id1>/<user_id2>")
def confirm_connection(user_id1, user_id2):
    result = add_connection(app, user_id1, user_id2)
    return json.dumps(result)

@app.route('/post/create', methods=["POST"])
def create_post():
    request_data = json.loads(request.data)
    user_id = request_data.get('user_id', None)
    type = request_data.get('type', None)
    title = request_data.get('title', None)
    content = request_data.get('content', None)
    print("data before:", user_id, type, title, content)
    if (not type.isnumeric()):
        if (type.lower() == 'text'):
            type = 1
        elif (type.lower() == 'video'):
            type = 2
        elif (type.lower() == 'image'):
            type = 3
        elif (type.lower() == 'audio'):
            type = 4
        elif (type.lower() == 'file'):
            type = 5
    else:
        type = int(type)

    new_post = Post(post_id=None, user_id=user_id, post_type_id=type, posted_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                 caption=title, likes=0, media_url=content)
    new_post_id = add_post(app, new_post)
    return json.dumps({'post_id': new_post_id })

@app.route('/addimdbuser/<imdbUserId>/<title>/<pronoun_id>')
def addImdbUser(imdbUserId, title, pronoun_id):
    success = create_user_from_imdb(app, imdbUserId, pronoun_id, title)
    # success = create_user_from_imdb(app, '3014031', 2, "Actor, Producer, and Executive")
    # success = create_user_from_imdb(app, '4141252', 2, "Actor and Singer")
    # success = create_user_from_imdb(app, '1602660', 3, "English Actor and Singer")
    # success = create_user_from_imdb(app, '3069650', 2, "British Actor, Producer, and Extra")
    # success = create_user_from_imdb(app, '1275259', 2, "American Actor/Actress and Singer")
    # success = create_user_from_imdb(app, '5896355', 2, "British-American Actor/Actress")
    # success = create_user_from_imdb(app, '2088803', 2, "Actor/Actress and Extra")
    # success = create_user_from_imdb(app, '1869101', 2, "Actor from Cuba")
    # success = create_user_from_imdb(app, '6073955', 2, "Producer and Actor/Actress")
    # success = create_user_from_imdb(app, '2074546', 3, "Actor and Producer")
    # success = create_user_from_imdb(app, '0647634', 2, "American Actor/Actress")
    return json.dumps({'added': success})

@app.route('/message', methods=["POST"])
def addMessage():
    request_data = json.loads(request.data)
    user_from = request_data.get('user_from', None)
    user_to = request_data.get('user_to', None)
    msg = request_data.get('msg', '')
    if (user_from == None or user_to == None or msg == 0):
        return json.dumps({'added': False})
    success = send_message(app, user_from, user_to, msg) != None
    return json.dumps({'added': success})


@app.route('/getMessages')
def getMessages():
    user_id = int(request.args.get('user_id'))
    user_to = request.args.get('user_to', None)
    # chats = []
    chats = get_messages(app, user_id, user_to)
    
    users = {}
    for chat in chats:
        other_user = chat['messages'][0]['user_to'] if chat['messages'][0]['user_to'] != user_id else chat['messages'][0]['user_from']
        if (other_user not in users):
            users[other_user] = get_user_by_id(app, other_user)
        chat['user'] = users[other_user].__dict__
        # TODO: get unreadMsgs
    if (user_to != None):
        get_user_by_id(app, user_to)
    return json.dumps(chats)

if __name__ == "__main__":
    app.run()
