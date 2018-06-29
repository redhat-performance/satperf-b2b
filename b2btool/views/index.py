"""Index view renderer.

File: index.py
Description: Index view renderer.
Date: 29/06/2018
Author: Saurabh Badhwar
"""
from flask import render_template
from flask.views import View

class Index(View):
    """Index view renderer.

    The view provides a method to render the index page template.
    """

    def dispatch_request(self):
        """Request dispatch handler."""
        return render_template('index.html')