<h1 align="center">Team Sigma</h1>

## About the project
Team Sigma aims to help young artists who are just starting out in the industry.

## Project setup
Follow these instructions to run the project after cloning locally:
1. Install [MySQL installer](https://dev.mysql.com/downloads/installer/) and install MySQL Server
    1. Set the MySQL root password as empty (no password)
2. At root, create a virtual environment with these commands on your terminal, alternatively, your IDE can create a venv for you:
    1. Run `python -m venv venv`
    2. If your os is OS X or Linux run `source venv/bin/activate`, if your os is Windows run `venv\Scripts\activate`
    3. Run `pip3 install -r requirements.txt`
4. Run `mysql -u root`.
    1. Run `CREATE DATABASE sigma_db CHARACTER SET utf8;` to create the local database.
    2. Run `exit`.
4. Run `python app.py` and go to the link provided in the terminal to view the webapp. (the same can be achieved by step 7)