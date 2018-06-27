"""Application entrypoint file.

File: __init__.py
Description: Marks the place for application entrypoint.
Date: 26/06/2018
Author: Saurabh Badhwar
"""
from b2btool.app import application, db
from b2btool.models import Query, Build
from b2btool.views import NewQuery

application.add_url_rule('/newquery', view_func=NewQuery.as_view('new_query'))
db.create_all()