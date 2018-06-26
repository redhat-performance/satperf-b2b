"""Application definition and configuration.

File: app.py
Description: The file contains the main application object and the
             configuration setup for the application.
Date: 26/06/2018
Author: Saurabh Badhwar
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__, instance_relative_config=True)
application.config.from_object('config')
application.config.from_pyfile('config.py')

db = SQLAlchemy(application)

@application.route("/ping", methods=['GET', 'POST'])
def ping():
    """Application ping."""
    return "PONG"
