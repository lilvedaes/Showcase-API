from flask import Flask
from flask_mysqldb import MySQL
from mysql_setup import setup_database

app = Flask(__name__)

# MySQL configuration
setup_database(app)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
