"""Application entrypoint file.

File: __init__.py
Description: Marks the place for application entrypoint.
Date: 26/06/2018
Author: Saurabh Badhwar
"""
from b2btool.app import application, db, graphite
from b2btool.models import Query, Build
from b2btool.views import NewQuery, NewBuild, BuildTags, BuildHosts, BuildBenchmarks, BuildMetrics, BuildLeafMetrics, Index

application.add_url_rule('/newquery', view_func=NewQuery.as_view('new_query'))
application.add_url_rule('/newbuild', view_func=NewBuild.as_view('new_build'))
application.add_url_rule('/tags', view_func=BuildTags.as_view('build_tags'))
application.add_url_rule('/hosts', view_func=BuildHosts.as_view('build_hosts'))
application.add_url_rule('/benchmarks', view_func=BuildBenchmarks.as_view('build_benchmarks'))
application.add_url_rule('/build_metrics', view_func=BuildMetrics.as_view('build_metrics'))
application.add_url_rule('/leaf_metrics', view_func=BuildLeafMetrics.as_view('leaf_metrics'))
application.add_url_rule('/', view_func=Index.as_view('index_view'))
db.create_all()