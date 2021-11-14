from flask_mysqldb import MySQL
from mysql_table_creation_constants import *

mysql = None

table_setup = [  # Be careful of order, some databases rely on others
    {'name': 'pronouns', 'setup': pronouns_table_command},
    {'name': 'union_statuses', 'setup': union_status_table_command},
    {'name': 'users', 'setup': users_table_command},
    {'name': 'production_types', 'setup': production_type_table_command},
    {'name': 'credits', 'setup': credits_table_command},
    {'name': 'ethnicities', 'setup': ethnicities_table_command},
    {'name': 'user_ethnicities', 'setup': user_ethnicities_table_command},
    {'name': 'connections', 'setup': connections_table_command},
    {'name': 'post_types', 'setup': post_types_table_command},
    {'name': 'posts', 'setup': posts_table_command},
    {'name': 'comments', 'setup': comments_table_command},
    {'name': 'socials', 'setup': socials_table_command},
    {'name': 'user_socials', 'setup': user_socials_table_command},
    {'name': 'demo_reels', 'setup': demo_reels_table_command},
    {'name': 'education', 'setup': education_table_command},
    {'name': 'skills', 'setup': skills_table_command}
]


def setup_database(app):
    global mysql
    # MySQL configuration
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'sigma_db'

    mysql = MySQL(app)

    # Uncomment next line to remove all data and re-initialize
    reset_data(app, mysql)
    # create_tables(app, mysql)
    # initialize_tables(app, mysql)


def create_tables(app, mysql):
    with app.app_context():
        cursor = mysql.connection.cursor()
        for database in table_setup:
            cursor.execute(database['setup'])
        mysql.connection.commit()
        cursor.close()


def initialize_tables(app, mysql):
    # ONLY for data that should always be initizalized
    # see insert_sample_data() for other purposes
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(pronouns_insert_command)
        cursor.execute(union_insert_command)
        cursor.execute(production_type_insert_command)
        cursor.execute(ethnicities_insert_command)
        cursor.execute(post_types_insert_command)
        cursor.execute(socials_insert_command)
        mysql.connection.commit()
        cursor.close()


def reset_data(app, mysql):
    with app.app_context():
        cursor = mysql.connection.cursor()
        for database in reversed(table_setup):
            cursor.execute("DROP TABLE IF EXISTS " + database["name"] + ";")
        mysql.connection.commit()
        cursor.close()
    create_tables(app, mysql)
    initialize_tables(app, mysql)


def execute_mysql_commands(app, commands: list):
    results = []
    with app.app_context():
        cursor = mysql.connection.cursor()
        for command in commands:
            cursor.execute(command)
            results.append(cursor.fetchall())
        mysql.connection.commit()
        cursor.close()
    return results

def execute_prepared_mysql_commands(app, commands: list, parameters: list):
    results = []
    with app.app_context():
        cursor = mysql.connection.cursor()
        for index in range(len(commands)):
            cursor.execute(commands[index], parameters)
            results.append(cursor.fetchall())
        mysql.connection.commit()
        cursor.close()
    return results
