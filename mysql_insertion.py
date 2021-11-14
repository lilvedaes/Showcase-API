from typing import List

from mysql_setup import execute_mysql_commands, execute_prepared_mysql_commands
import time
from objects import *

remove_from_tuple = lambda lst, ignore_elems: [i for i in lst if i not in ignore_elems]


# I'm sorry this isn't pretty, but it adds 3 users and 2 connections!

def add_connection(app, user_id1, user_id2):
    connection_date = time.strftime('%Y-%m-%d %H:%M:%S')
    command = ("INSERT INTO connections (user_id1, user_id2, connection_date) VALUES (" + str(user_id1) + ", " + str(
        user_id2) + ", '" + connection_date + "');")
    return execute_mysql_commands(app, [command])

def create_user(app, user: DBUser):
    user_data = user.get_values()[1:] # get all data except user_id
    insert_command = ('''INSERT INTO users (first_name, last_name, profile_image_url, location, title, pronoun_id, gender, union_status_id, height, weight, eye_colour, hair_colour, age_range_start, age_range_end, about_info) VALUES ("%s", "%s", "%s", "%s", "%s", %d, "%s", %d, %d, %d, "%s", "%s", %d, %d, "%s")''' %user_data)
    check_command = ('''SELECT user_id FROM users WHERE first_name = "''' + user.first_name + '''" AND last_name = "''' + user.last_name + '''";''')
    execute_mysql_commands(app, [insert_command])
    result = execute_mysql_commands(app, [check_command])[0][0]
    user.user_id = result[0]  # Now the user has an id, set it in the object

def add_credit(app, credit: Credit):
    credit_data = credit.get_values()
    insert_command = '''INSERT INTO credits (user_id, production_name, role, start_date, end_date, src_type, src_url, production_type, director, producer, production_link, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], credit_data)

def add_social(app, user_id, label, social_link):
    insert_command = '''INSERT INTO user_socials (user_id, label, social_link) VALUES (%s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, label, social_link))

def add_demo_reel(app, user_id, title, src_url):
    insert_command = '''INSERT INTO demo_reels (user_id, title, src_url) VALUES (%s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, title, src_url))

def add_skill(app, user_id, skill):
    insert_command = '''INSERT INTO skills (user_id, skill) VALUES (%s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, skill))

def add_ethnicity(app, user_id, ethnicity):
    find_ethnicity_id = 'SELECT ethnicity_id FROM ethnicities WHERE ethnicity = "' + ethnicity + '";'
    ethnicity_ids = execute_mysql_commands(app, [find_ethnicity_id])[0][0]
    insert_command = '''INSERT INTO user_ethnicities (user_id, ethnicity_id) VALUES (%s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, ethnicity_ids[0]))

def add_credit(app, credit: Credit):
    credit_data = credit.get_values()
    insert_command = '''INSERT INTO credits (user_id, production_name, role, start_date, end_date, src_type, src_url, production_type, director, producer, production_link, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], credit_data)

def add_social(app, user_id, label, social_link):
    insert_command = '''INSERT INTO user_socials (user_id, label, social_link) VALUES (%s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, label, social_link))

def add_demo_reel(app, user_id, title, src_url):
    insert_command = '''INSERT INTO demo_reels (user_id, title, src_url) VALUES (%s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, title, src_url))

def add_skill(app, user_id, skill):
    insert_command = '''INSERT INTO skills (user_id, skill) VALUES (%s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, skill))

def add_ethnicity(app, user_id, ethnicity):
    find_ethnicity_id = 'SELECT ethnicity_id FROM ethnicities WHERE ethnicity = "' + ethnicity + '";'
    ethnicity_ids = execute_mysql_commands(app, [find_ethnicity_id])[0][0]
    insert_command = '''INSERT INTO user_ethnicities (user_id, ethnicity_id) VALUES (%s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], (user_id, ethnicity_ids[0]))

def add_education(app, education: Education):
    education_data = education.get_values()
    insert_command = '''INSERT INTO education (user_id, title, start_date, end_date, institution, institution_logo_url) VALUES (%s, %s, %s, %s, %s, %s)'''
    execute_prepared_mysql_commands(app, [insert_command], education_data)

def add_sample_data(app):
    user1 = DBUser(user_id=None, first_name="Nyah", last_name="Way", profile_image_url="profile_url",
                 location="Toronto, ON", title="Student", pronoun_id=2, gender="Female", union_status_id=3, height=10,
                 weight=20, eye_colour='brown', hair_colour='brown', age_range_start=17, age_range_end=25,
                 about_info="Nyah's about info")
    user2 = DBUser(user_id=None, first_name="Daniela", last_name="Venturo Esaine", profile_image_url="profile_url2",
                 location="Toronto, ON", title="Student", pronoun_id=2, gender="Female", union_status_id=2, height=12,
                 weight=22, eye_colour='brown', hair_colour='white', age_range_start=18, age_range_end=26,
                 about_info="Daniela's about info")
    user3 = DBUser(user_id=None, first_name="Jackson", last_name="Han", profile_image_url="profile_url3",
                 location="Toronto, ON", title="Student", pronoun_id=3, gender="Male", union_status_id=3, height=9,
                 weight=25, eye_colour='dark brown', hair_colour='black', age_range_start=18, age_range_end=25,
                 about_info="Jackson's about info")
    create_user(app, user1)
    create_user(app, user2)
    create_user(app, user3)
    add_connection(app, user1.user_id, user2.user_id)
    add_connection(app, user2.user_id, user3.user_id)
    credit1 = Credit(user_id=user1.user_id, production_name="Dune",            role="Chani",                 start_date="2021", end_date="2021", src_type="image", src_url="https://www.indiewire.com/wp-content/uploads/2021/08/dune-2-e1630306284316.png", production_type="Movie",   director=None, producer=None, production_link=None, description='Starring role in movie "Dune"')
    credit2 = Credit(user_id=user1.user_id, production_name="Euphoria",        role="Rue Bennet",            start_date="2019", end_date="2020", src_type="video", src_url="https://www.youtube.com/embed/hmk1aHU0768",                                      production_type="TV show", director=None, producer=None, production_link=None, description='Lead role in HBO TV series "Euphoria"')
    credit3 = Credit(user_id=user1.user_id, production_name="K.C. Undercover", role="K.C. Cooper / Bernice", start_date="2015", end_date="2018", src_type=None,    src_url=None,                                                                             production_type="TV show", director=None, producer=None, production_link=None, description='Lead role in Disney TB series "K.C. Undercover"')
    add_credit(app, credit1)
    add_credit(app, credit2)
    add_credit(app, credit3)
    add_social(app, user1.user_id, 'IMDb', 'https://www.imdb.com')
    add_social(app, user1.user_id, 'Instagram', 'https://www.instagram.com')
    add_social(app, user1.user_id, 'YouTube', 'https://www.youtube.com')
    add_demo_reel(app, user1.user_id, 'Acting Reel', 'https://www.youtube.com/embed/r_cptjgco2Y')
    add_demo_reel(app, user1.user_id, 'Dancing Reel', 'https://www.youtube.com/embed/2Iw951fviP4')
    education = []
    education.append(Education(user_id=user1.user_id, title="Theatre",                        start_date="2015", end_date="",     institution="Oakland School for the Arts",    institution_logo_url="https://upload.wikimedia.org/wikipedia/commons/4/4e/Oakland_School_for_the_Arts_logo.jpg"))
    education.append(Education(user_id=user1.user_id, title="CalShakes Conservatory Program", start_date="2012", end_date="",     institution="California Shakespeare Theater", institution_logo_url="https://fundforsharedinsight.org/wp-content/uploads/2019/11/cal-shakes-logo.jpg"))
    education.append(Education(user_id=user1.user_id, title="Acting",                         start_date="2011", end_date="2012", institution="American Conservatory Theater",  institution_logo_url="https://s3.amazonaws.com/mobilecause-avatar-production/shared_img/shared_imgs/352099/thumbnail/logo_stamp_square_black-5000x500.png?1586974422"))
    for edu in education:
        add_education(app, edu)
    skills = ['Stage Fighting', 'Kick Boxing', 'Singing', 'Dancing', 'British Accent', 'Spanish Accent', 'Gymnastics', 'Cheerleading', 'Fencing', 'Skiing']
    for skill in skills:
        add_skill(app, user1.user_id, skill)
    ethnicities = ['Black/African American', 'other']
    for ethnicity in ethnicities:
        add_ethnicity(app, user1.user_id, ethnicity)

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
    command = "SELECT user_id, first_name, last_name, profile_image_url, location, title, pronoun_set, gender, union_status, height, weight, eye_colour, hair_colour, age_range_start, age_range_end, about_info FROM (users LEFT JOIN union_statuses ON union_statuses.union_status_id=users.union_status_id LEFT JOIN pronouns ON pronouns.pronoun_id=users.pronoun_id) WHERE user_id = " + str(user_id) + ";"
    user = execute_mysql_commands(app, [command])[0][0]
    return User(*user)

def add_post(app, post: Post):
    command = ("INSERT INTO posts (user_id, post_type_id, posted_date, caption, likes, media_url) "
               "VALUES (" + str(post.user_id) + ", " + str(post.post_type_id) +
               ", '" + post.posted_date + "', '" + post.caption + "', " + str(post.likes) + ", '" + post.media_url +
               "');")
    check_command = ("SELECT LAST_INSERT_ID();")

    result = execute_mysql_commands(app, [command, check_command])
    post.post_id = result[1][0][0]  # Now the post has an id, set it in the object

    return post.post_id


def delete_post(app, post_id: int):
    command = ("DELETE FROM posts WHERE post_id = " + str(post_id) + ";")
    return execute_mysql_commands(app, [command])


def get_posts(app, post_ids_lst: List[int]):
    raw_results = []
    for post_id in post_ids_lst:
        command = ("SELECT * FROM posts WHERE post_id = " + str(post_id) + ";")
        raw_results.extend(execute_mysql_commands(app, [command]))

    results = []
    for i in range(len(raw_results[0])):
        post = Post(post_id=raw_results[0][i][0], user_id=raw_results[0][i][1], post_type_id=raw_results[0][i][2],
                    posted_date=raw_results[0][i][3], caption=raw_results[0][i][4], likes=raw_results[0][i][5],
                    media_url=raw_results[0][i][6])
        results.append(post)

    return results

def get_users_posts(app, user_ids_lst: List[int]):
    raw_results = []
    for user_id in user_ids_lst:
        command = ("SELECT * FROM posts WHERE user_id = " + str(user_id) + ";")
        raw_results.extend(execute_mysql_commands(app, [command]))

    results = []
    for i in range(len(raw_results[0])):
        post = Post(post_id=raw_results[0][i][0], user_id=raw_results[0][i][1], post_type_id=raw_results[0][i][2],
                    posted_date=raw_results[0][i][3], caption=raw_results[0][i][4], likes=raw_results[0][i][5],
                    media_url=raw_results[0][i][6])
        results.append(post)

    return results

def get_user_media(app, user_id):
    command = ("SELECT post_type, media_url FROM posts LEFT JOIN post_types ON posts.post_type_id=post_types.post_type_id WHERE user_id = " + str(user_id) + " AND posts.post_type_id != 1;")
    results = execute_mysql_commands(app, [command])[0]
    media = [{ 'src_type': result[0], 'media_url': result[1] } for result in results]
    return media


def add_comment(app, comment: Comment):
    command = ("INSERT INTO comments (user_id, post_id, comment_date, comment, likes) "
               "VALUES (" + str(comment.user_id) + ", " + str(comment.post_id) +
               ", '" + comment.comment_date + "', '" + comment.comment + "', " + str(comment.likes) +
               ");")

    check_command = ("SELECT LAST_INSERT_ID();")

    result = execute_mysql_commands(app, [command, check_command])
    comment.comment_id = result[1][0][0]  # Now the comment has an id, set it in the object

    return comment.comment_id


def delete_comment(app, comment_id: int):
    command = ("DELETE FROM comments WHERE comment_id = " + str(comment_id) + ";")
    return execute_mysql_commands(app, [command])


def get_comments(app, comment_ids_lst: List[int]):
    raw_results = []
    for comment_id in comment_ids_lst:
        command = ("SELECT * FROM comments WHERE comment_id = " + str(comment_id) + ";")
        raw_results.extend(execute_mysql_commands(app, [command]))

    results = []
    for i in range(len(raw_results[0])):
        comment = Comment(comment_id=raw_results[0][i][0], user_id=raw_results[0][i][1], post_id=raw_results[0][i][2],
                    comment_date=raw_results[0][i][3], comment=raw_results[0][i][4], likes=raw_results[0][i][5])
        results.append(comment)

    return results


def get_post_comments(app, post_ids_lst: List[int]):
    raw_results = []
    for post_id in post_ids_lst:
        command = ("SELECT * FROM comments WHERE post_id = " + str(post_id) + ";")
        raw_results.extend(execute_mysql_commands(app, [command]))

    results = []
    for i in range(len(raw_results[0])):
        comment = Comment(comment_id=raw_results[0][i][0], user_id=raw_results[0][i][1], post_id=raw_results[0][i][2],
                    comment_date=raw_results[0][i][3], comment=raw_results[0][i][4], likes=raw_results[0][i][5])
        results.append(comment)

    return results


def add_sample_posts_with_comments(app):
    post1 = Post(post_id=None, user_id=1, post_type_id=1, posted_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                 caption="In the beach!", likes=0, media_url="")
    post2 = Post(post_id=None, user_id=1, post_type_id=3, posted_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                 caption="Another caption!", likes=0, media_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Zendaya_-_2019_by_Glenn_Francis.jpg/1200px-Zendaya_-_2019_by_Glenn_Francis.jpg")
    post3 = Post(post_id=None, user_id=1, post_type_id=2, posted_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                 caption="In the sand!", likes=0, media_url="https://www.youtube.com/embed/QuCUA1HskqQ")
    post1_id = add_post(app, post1)
    post2_id = add_post(app, post2)
    post3_id = add_post(app, post3)

    comment1 = Comment(comment_id=None, user_id=1, post_id=post1_id, comment_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                       comment="Looks awesome!", likes=0)
    comment2 = Comment(comment_id=None, user_id=1, post_id=post1_id, comment_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                       comment="Looks great!", likes=0)
    comment3 = Comment(comment_id=None, user_id=2, post_id=post3_id, comment_date=time.strftime('%Y-%m-%d %H:%M:%S'),
                       comment="Looks amazing!", likes=0)

    add_comment(app, comment1)
    add_comment(app, comment2)
    add_comment(app, comment3)


def get_credits(app, user_id):
    command = "SELECT * FROM credits WHERE user_id = " + str(user_id) + ";"
    results = execute_mysql_commands(app, [command])[0]
    credits = [Credit(*(result)) for result in results]
    return credits

def get_num_connections(app, user_id):
    command = "SELECT COUNT(*) AS connection_count FROM connections WHERE user_id1 = " + str(user_id) + " OR user_id2 = " + str(user_id) + ";"
    count = execute_mysql_commands(app, [command])[0][0]
    return count[0]

def get_socials(app, user_id):
    command = "SELECT user_socials.label, social_link, icon FROM user_socials LEFT JOIN socials ON user_socials.label=socials.label WHERE user_id = " + str(user_id) + ";"
    results = execute_mysql_commands(app, [command])[0]
    socials = [{ 'label': result[0], 'social_link': result[1], 'icon': result[2] } for result in results]
    return socials

def get_demo_reels(app, user_id):
    command = "SELECT title, src_url FROM demo_reels WHERE user_id = " + str(user_id) + ";"
    results = execute_mysql_commands(app, [command])[0]
    reels = [{ 'title': result[0], 'src_url': result[1] } for result in results]
    return reels

def get_skills(app, user_id):
    command = "SELECT skill FROM skills WHERE user_id = " + str(user_id) + ";"
    results = execute_mysql_commands(app, [command])[0]
    skills = [result[0] for result in results]
    return list(skills)

def get_education(app, user_id):
    command = "SELECT * FROM education WHERE user_id = " + str(user_id) + ";"
    results = execute_mysql_commands(app, [command])[0]
    education = [Education(*result) for result in results]
    return education

def get_ethnicities(app, user_id):
    command = "SELECT ethnicity FROM user_ethnicities LEFT JOIN ethnicities ON user_ethnicities.ethnicity_id=ethnicities.ethnicity_id WHERE user_id = " + str(user_id) + ";"
    results = execute_mysql_commands(app, [command])[0]
    ethnicities = [result[0] for result in results]
    return ethnicities

