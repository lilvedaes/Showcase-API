from mysql_setup import execute_mysql_commands
import time
from objects import *

# I'm sorry this isn't pretty, but it adds 3 users and 2 connections!

def add_connection(app, user_id1, user_id2):
    connection_date = time.strftime('%Y-%m-%d %H:%M:%S')
    command = ("INSERT INTO connections (user_id1, user_id2, connection_date) VALUES (" + str(user_id1) + ", " + str(user_id2) + ", '" + connection_date + "');")
    return execute_mysql_commands(app, [command])

def create_user(app, user: User):
    user_data = user.get_values()[1:] # get all data except user_id
    insert_command = ('INSERT INTO users (first_name, last_name, profile_image_url, location, title, pronoun_id, union_status_id, height, weight, eye_colour, hair_colour, age_range_start, age_range_end, about_info) VALUES ("%s", "%s", "%s", "%s", "%s", %d, %d, %d, %d, "%s", "%s", %d, %d, "%s")' %user_data)
    check_command = ('SELECT user_id FROM users WHERE first_name = "' + user.first_name + '" AND last_name = "' + user.last_name + '";')
    execute_mysql_commands(app, [insert_command])
    result = execute_mysql_commands(app, [check_command])
    user.user_id = result[0][0][0] # Now the user has an id, set it in the object


def add_sample_data(app):
    user1 = User(None, "Nyah", "Way", "profile_url", "Toronto", "Student", 2, 3, 10, 20, 'brown', 'brown', 17, 25, "Nyah's about info")
    user2 = User(None, "Daniela", "Venturo Esaine", "profile_url2", "Toronto", "Student", 2, 2, 12, 22, 'brown', 'white', 18, 26, "Daniela's about info")
    user3 = User(None, "Jackson", "Han", "profile_url3", "Toronto", "Student", 3, 3, 9, 25, 'dark brown', 'black', 18, 25, "Jackson's about info")
    create_user(app, user1)
    create_user(app, user2)
    create_user(app, user3)
    add_connection(app, user1.user_id, user2.user_id)
    add_connection(app, user2.user_id, user3.user_id)