"""Build data model.

File: build.py
Description: The model defines the way how we store the build to build
             data for comparison purpose.
Date: 26/06/2018
Author: Saurabh Badhwar
"""
from b2btool import db


class Build(db.Model):
    """Build model.

    The build model describes the way in which we store the information
    about build to build records. This information is then used to query the
    backend time series database for the purpose of generating visualizations.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                   comment="Build ID")
    benchmark_name = db.Column(db.String(255), nullable=False, 
                               comment="The name of the benchmark")
    hostname = db.Column(db.String(255), nullable=False, 
                         comment="The hostname to pull the data of")
    tag = db.Column(db.String(50), nullable=False, comment="Build \
                    differentiation tag")
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Build model representation."""
        return "Build %r" % self.tag