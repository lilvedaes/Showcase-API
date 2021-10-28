from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

'''
Example of how to use the mysqldb library:
    cursor = mysql.connection.cursor()
    cursor.execute(\''' INSERT INTO info_table VALUES(%s,%s)\''',(name,age))
    mysql.connection.commit()
    cursor.close()
'''


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
