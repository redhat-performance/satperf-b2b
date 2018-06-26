"""Query Model.

File: query.py
Description: The query models defines the database model for storing the custom
             queries based on the input provided.
Date: 26/06/2018
Author: Saurabh Badhwar
"""
from b2btool import db


class Query(db.Model):
    """Query model definition.

    The model defines a mechanism for storing the queries related to custom fields so as to provide a visualization.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                   comment="Unique ID for the query")
    name = db.Column(db.String(100), nullable=False, comment="Display name \
                     for query")
    query_text = db.Column(db.String(512), nullable=False, 
                           comment="Queryable text to use for querying")

    def __repr__(self):
        """Query model representation."""
        return "Query %r" % self.name