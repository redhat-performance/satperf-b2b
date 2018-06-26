"""Application entrypoint file.

File: __init__.py
Description: Marks the place for application entrypoint.
Date: 26/06/2018
Author: Saurabh Badhwar
"""
from b2btool.app import application, db
from b2btool.models import Query, Build

db.create_all()