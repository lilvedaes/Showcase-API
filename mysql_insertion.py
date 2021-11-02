from typing import List

from mysql_setup import execute_mysql_commands
import time
from objects import *

remove_from_tuple = lambda lst, ignore_elems: [i for i in lst if i not in ignore_elems]


# I'm sorry this isn't pretty, but it adds 3 users and 2 connections!

def add_connection(app, user_id1, user_id2):
    connection_date = time.strftime('%Y-%m-%d %H:%M:%S')
    command = ("INSERT INTO connections (user_id1, user_id2, connection_date) VALUES (" + str(user_id1) + ", " + str(
        user_id2) + ", '" + connection_date + "');")
    return execute_mysql_commands(app, [command])


def create_user(app, user: User):
    user_data = user.get_values()[1:]  # get all data except user_id
    insert_command = (
                'INSERT INTO users (first_name, last_name, profile_image_url, location, title, pronoun_id, gender, union_status_id, height, weight, eye_colour, hair_colour, age_range_start, age_range_end, about_info) VALUES ("%s", "%s", "%s", "%s", "%s", %d, "%s", %d, %d, %d, "%s", "%s", %d, %d, "%s")' % user_data)
    check_command = (
                'SELECT user_id FROM users WHERE first_name = "' + user.first_name + '" AND last_name = "' + user.last_name + '";')
    execute_mysql_commands(app, [insert_command])
    result = execute_mysql_commands(app, [check_command])[0][0]
    user.user_id = result[0]  # Now the user has an id, set it in the object


def add_sample_data(app):
    user1 = User(user_id=None, first_name="Nyah", last_name="Way", profile_image_url="profile_url",
                 location="Toronto, ON", title="Student", pronoun_id=2, gender="Female", union_status_id=3, height=10,
                 weight=20, eye_colour='brown', hair_colour='brown', age_range_start=17, age_range_end=25,
                 about_info="Nyah's about info")
    user2 = User(user_id=None, first_name="Daniela", last_name="Venturo Esaine", profile_image_url="profile_url2",
                 location="Toronto, ON", title="Student", pronoun_id=2, gender="Female", union_status_id=2, height=12,
                 weight=22, eye_colour='brown', hair_colour='white', age_range_start=18, age_range_end=26,
                 about_info="Daniela's about info")
    user3 = User(user_id=None, first_name="Jackson", last_name="Han", profile_image_url="profile_url3",
                 location="Toronto, ON", title="Student", pronoun_id=3, gender="Male", union_status_id=3, height=9,
                 weight=25, eye_colour='dark brown', hair_colour='black', age_range_start=18, age_range_end=25,
                 about_info="Jackson's about info")
    create_user(app, user1)
    create_user(app, user2)
    create_user(app, user3)
    add_connection(app, user1.user_id, user2.user_id)
    add_connection(app, user2.user_id, user3.user_id)


def get_network_connections(app, filter: Network_Filter):
    prev_ids = [filter.user_id]
    next_ids = []
    curr_index = 0
    users = [get_user_by_id(app, filter.user_id)]
    users[0].connection_dist = 0

    for connection_dist in range(1, filter.connection_dist + 1):
        while (curr_index < len(prev_ids)):
            command = "SELECT * FROM connections WHERE user_id1 = " + str(
                prev_ids[curr_index]) + " OR user_id2 = " + str(prev_ids[curr_index]) + ";"
            results = execute_mysql_commands(app, [command])[0]
            for connection in results:
                ids = remove_from_tuple(connection[:2],
                                        prev_ids)  # Get a list of ids in connection we haven't seen before
                if len(ids) == 0:  # ids should only ever contain 0 or 1 elements now
                    continue
                user = get_user_by_id(app, ids[0])
                add_user_based_on_filter(users, user, connection_dist, filter)
                next_ids.append(user.user_id)
            curr_index += 1
        prev_ids.extend(next_ids)
        next_ids = []
    return users


def add_user_based_on_filter(lst: list, user: User, connection_dist: int, filter: Network_Filter):
    if filter.user_applicable(user, connection_dist):
        lst.append(user)
        lst[-1].connection_dist = connection_dist


def get_user_by_id(app, user_id):
    command = "SELECT * FROM users WHERE user_id = " + str(user_id) + ";"
    user = execute_mysql_commands(app, [command])[0][0]
    return User(*user)


def add_post(app, post: Post):
    command = ("INSERT INTO posts (user_id, post_type_id, posted_date, caption, likes, media_url) "
               "VALUES (" + str(post.user_id) + ", " + str(post.post_type_id) +
               ", '" + post.posted_date + "', ''" + post.caption + "', " + str(post.likes) + ", '" + post.media_url +
               "');")
    execute_mysql_commands(app, [command])

    check_command = ("SELECT post_id FROM posts WHERE user_id = " + str(post.user_id) + "AND post_type_id = " +
                     str(post.post_type_id) + "AND posted_date = '" + post.posted_date + "'" + "AND caption = '" +
                     post.caption + "';")

    result = execute_mysql_commands(app, [check_command])[0][0]
    post.post_id = result[0]  # Now the post has an id, set it in the object

    return execute_mysql_commands(app, [command])


def delete_post(app, post_id: int):
    command = ("DELETE FROM posts WHERE post_id = " + str(post_id) + ";")
    return execute_mysql_commands(app, [command])


def get_posts(app, post_ids_lst: List[int]):
    raw_results = []
    for post_id in post_ids_lst:
        command = ("SELECT * FROM posts WHERE post_id = " + str(post_id) + ";")
        raw_results.extend(execute_mysql_commands(app, [command]))

    results = []
    for i in range(len(raw_results)):
        post = Post(post_id=raw_results[0][i][0][0], user_id=raw_results[0][i][0][1], post_type_id=raw_results[0][i][0][2],
                    posted_date=raw_results[0][i][0][3], caption=raw_results[0][i][0][4], likes=raw_results[0][i][0][5],
                    media_url=raw_results[0][i][0][6])
        results.append(post)

    return results


def add_comment(app, comment: Comment):
    command = ("INSERT INTO comments (user_id, post_id, comment_date, comment, likes) "
               "VALUES (" + str(comment.user_id) + ", " + str(comment.post_id) +
               ", '" + comment.comment_date + "', ''" + comment.comment +
               "');")
    execute_mysql_commands(app, [command])

    check_command = ("SELECT comment_id FROM comments WHERE user_id = " + str(comment.user_id) + "AND post_id = " +
                     str(comment.post_id) + "AND comment_date = '" + comment.comment_date + "'" + "AND comment = '" +
                     comment.comment + "';")

    result = execute_mysql_commands(app, [check_command])[0][0]
    comment.comment_id = result[0]  # Now the comment has an id, set it in the object

    return execute_mysql_commands(app, [command])


def delete_comment(app, comment_id: int):
    command = ("DELETE FROM comments WHERE comment_id = " + str(comment_id) + ";")
    return execute_mysql_commands(app, [command])


def get_comments(app, comment_ids_lst: List[int]):
    raw_results = []
    for comment_id in comment_ids_lst:
        command = ("SELECT * FROM comments WHERE comment_id = " + str(comment_id) + ";")
        raw_results.extend(execute_mysql_commands(app, [command]))

    results = []
    for i in range(len(raw_results)):
        comment = Comment(comment_id=raw_results[0][i][0][0], user_id=raw_results[0][i][0][1], post_id=raw_results[0][i][0][2],
                    comment_date=raw_results[0][i][0][3], comment=raw_results[0][i][0][4], likes=raw_results[0][i][0][5])
        results.append(comment)

    return results
