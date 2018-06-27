"""B2B Tool configuration.

File: config.py
Description: Flask configuration file for B2B tool
Date: 27/06/2018
Author: Saurabh Badhwar
"""
DEBUG = False
SECRET_KEY = 'your_application_secret_key'
BCRYPT_LOG_ROUNDS = 5  # Increase this value as required for your application
SQLALCHEMY_DATABASE_URI = "sqlalchemy compatible URI for connecting \
                        to database"
SQLALCHEMY_ECHO = False
STATIC_PATH = 'capacity_planner/static'
TEMPLATES_PATH = 'capacity_planner/templates'
SESSION_TYPE = 'filesystem'
