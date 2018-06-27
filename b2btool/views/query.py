"""Query related views.

File: query.py
Description: The file implements views related to custom query mechanism
             which is used for creating custom queries for the datasource.
Date: 27/06/2018
Author: Saurabh Badhwar
"""
from b2btool.models import Query
from b2btool import db
from flask.views import View
from flask import render_template, request, jsonify


class NewQuery(View):
    """NewQuery view for adding new data queries.

    The NewQuery view provides a REST endpoint for adding a new custom
    data query to the query database. These queries are then used to
    pull data from the data providing service.
    """

    methods = ['POST']

    def dispatch_request(self):
        """Request dispatcher."""
        response = {}

        query_data = request.get_json()
        query_name = query_data['name']
        query_string = query_data['query']

        # Build a model out of the data we got
        q = Query(name=query_name, query_text=query_string)
        db.session.add(q)
        db.session.commit()

        # We are done, time to exit
        response["status"] = "Success"
        return jsonify(response), 200

class GetQuery(View):
    """GetQuery view returns the custom queries applicable to a given hostname.

    The GetQuery view implements mechanism for retrieving the queries that are
    applicable to a given hostname.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Request dispatcher."""

        raise NotImplementedError("The method is not yet implemented.")

