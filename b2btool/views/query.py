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
        self.create_new_query(query_name, query_string)

        # We are done, time to exit
        response["status"] = "Success"
        return jsonify(response), 200

    def create_new_query(self, name, query_text):
        """Create a new custom query in the database.

        Keyword arguments:
        name -- The name to refer to the custom query
        query_text -- The custom query to be done
        """

        q = Query(name=name, query_text=query_text)
        db.session.add(q)
        db.session.commit()
        


class GetQuery(View):
    """GetQuery view returns the custom queries applicable to a given hostname.

    The GetQuery view implements mechanism for retrieving the queries that are
    applicable to a given hostname.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Request dispatcher."""

        hostname = request.args.get("hostname")
        print(hostname)


class GenericQuery(View):
    """GenericQuery view provides methods to manipulate a particular query.

    The GenericQuery view is responsible for providing a common endpoint for
    managing the individual custom queries, providing operations like, view,
    update and delete.
    """

    methods = ["GET", "POST", "DELETE"]

    def get(self):
        """Get request handler."""
        response = {}
        query_name = request.args.get("name")
        query_obj = self.get_object(query_name)
        if query_obj is not None:
            response[query_obj.name] = query_obj.query_text
        return jsonify(response), 200

    def post(self):
        """Post request handler."""
        response = {}
        request_data = request.get_json()
        query_name = request_data['name']
        query_string = request_data['query']
        query_obj = self.get_object(query_name)
        if query_obj is not None:
            query_obj.query_text = query_string
            db.session.commit()
            return jsonify(response), 202
        return jsonify(response), 304

    def delete(self):
        """Delete request handler."""
        response = {}
        query_name = request.args.get('name')
        query_obj = self.get_object(query_name)
        if query_obj is not None:
            db.session.delete(query_obj)
            db.session.commit()
            return jsonify(response), 202
        return jsonify(response), 304

    def get_object(self, name):
        """Retrieve a query object.

        Keyword arguments:
        name -- The name with which to retrieve the object

        Returns:
            sqlalchemy.BaseQuery
        """
        return Query.query.filter_by(name=name).first()