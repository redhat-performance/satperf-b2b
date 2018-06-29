"""Views entrypoint file.

File: __init__.py
Description: The files marks the entrypoint for the views inside the B2BTool.
Date: 27/06/2018
Author: Saurabh Badhwar
"""
from .query import NewQuery
from .build import NewBuild, BuildTags, BuildBenchmarks, BuildHosts, BuildMetrics, BuildLeafMetrics
from .index import Index