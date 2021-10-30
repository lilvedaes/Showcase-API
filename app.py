from flask import Flask
from mysql_setup import setup_database
from mysql_insertion import *

app = Flask(__name__)

# MySQL configuration
setup_database(app)
add_sample_data(app)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
