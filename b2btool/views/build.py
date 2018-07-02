"""Build data recorder views.

File: build.py
Description: The file contains information about the views related to
             handling of the build data.
Date: 28/06/2018
Author: Saurabh Badhwar
"""
from b2btool.models import Build
from b2btool import db, graphite
from flask import render_template, jsonify, request
from flask.views import View
from datetime import datetime


class NewBuild(View):
    """NewBuild view for taking in the data about the new build.

    The view is responsible for taking in the data about the new builds
    which needs to be visualized.
    """

    methods = ["POST"]

    def dispatch_request(self):
        """Request disptach handler."""
        response = {}
        request_data = request.get_json()
        benchmark_name = request_data['benchmark_name']
        hostname = request_data['hostname'].replace('.', '_')
        tag = request_data['build_tag']
        start_time = datetime.strptime(request_data['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(request_data['end_time'], '%Y-%m-%d %H:%M:%S')
        self.create_build_record(benchmark_name, hostname, tag, start_time,
                                 end_time)
        return jsonify(response), 201

    def create_build_record(self, benchmark_name, hostname, tag, start_time,
                            end_time):
        """Create a new build comparison record in the database.

        Keyword arguments:
        benchmark_name -- The name of the benchmark to store the record for
        hostname -- The hostname of the host from which the data was collected
        tag -- The build tag to which the record belongs
        start_time -- The time at which the benchmark started
        end_time -- The time at which the benchmark ended
        """
        build = Build(benchmark_name=benchmark_name, hostname=hostname, tag=tag, start_time=start_time, end_time=end_time)
        db.session.add(build)
        db.session.commit()


class BuildTags(View):
    """BuildTag view for querying build tags.

    The BuildTag view exposes a mechanism for querying the build tags
    that are present in the Build records.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Request dispatch handler."""
        response = {}
        build_objects = self.get_objects()
        response["tags"] = []
        for obj in build_objects:
            response["tags"].append(obj.tag)
        return jsonify(response), 200

    def get_objects(self):
        """Get all the objects.

        Returns:
            sqlalchemy.BaseQuery

        """
        return db.session.query(Build.tag).distinct().all()


class BuildBenchmarks(View):
    """BuildBenchmarks view for querying available benchmarks in a build.

    The BuildBenchmarks view provides a mechanism for querying the available
    benchmarks available in a particular build tag.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Dispatch request handler."""
        response = {}
        build_tag = request.args.get('build_tag')
        hostname = request.args.get('hostname')
        build_objects = self.get_objects(build_tag, hostname)
        response['benchmarks'] = []
        for obj in build_objects:
            response['benchmarks'].append(obj.benchmark_name)
        return jsonify(response), 200

    def get_objects(self, tag, hostname):
        """Get Build data objects.

        Keyword arguments:
        tag -- The build tag with which to retrieve the objects
        hostname -- The hostname for which the benchmarks should be returned
        Returns:
            List
        
        """
        return Build.query.filter_by(tag=tag).filter_by(hostname=hostname).all()


class BuildHosts(View):
    """BuildHosts view for retrieving host associated information.

    The view is responsible for returning all the hostnames in a
    specified build tag.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Request dispatch handler."""
        response = {}
        build_tag = request.args.get('build_tag')
        build_objects = self.get_objects(build_tag)
        response['hosts'] = []
        for obj in build_objects:
            response['hosts'].append(obj.hostname)
        return jsonify(response), 200

    def get_objects(self, tag):
        """Get build object data.

        Keyword arguments:
        tag -- The build tag to filter the hosts with

        Returns:
            List
        
        """
        return Build.query.filter_by(tag=tag)


class BuildMetrics(View):
    """BuildMetrics view for retrieving the build metrics.

    The BuildMetrics view implement functionality for retrieving the metrics
    available for a particular host in a given build tag. The view returns the
    available metrics if a fully qualified query_path parameter is provided.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Request dispatch handler."""
        response = {}
        build_tag = request.args.get('build_tag')
        benchmark_name = request.args.get('benchmark')
        hostname = request.args.get('hostname')

        try:
            query_path = request.args.get('query_path')
            build_obj = self.get_object(build_tag, benchmark_name, hostname)
            metric_data = graphite.get_metric_data(query_path, build_obj.start_time, build_obj.end_time)
            response['dataset'] = metric_data
            return jsonify(response), 200
        except:
            metrics = graphite.get_metrics(hostname)
            response['metrics'] = metrics
            return jsonify(response), 200

    def get_object(self, tag, benchmark, hostname):
        """Retrieve the build data object from database

        Keyword arguments:
        tag -- The build tag
        benchmark -- The name of the benchmark
        hostname -- The hostname for which record needs to be retrieved
        """
        return Build.query.filter_by(tag=tag, benchmark_name=benchmark, hostname=hostname).first()


class BuildLeafMetrics(View):
    """BuildLeafMetrics view for retrieving leaf node metrics.

    The view provides methods for handling the retrieval of metric
    paths which can be visualized.
    """

    methods = ["GET"]

    def dispatch_request(self):
        """Request dispatch handler."""
        response = {}
        query_path = request.args.get('query_path')
        measurable_metrics = graphite.get_measurable_metrics(path=query_path)
        response['metric_paths'] = measurable_metrics
        return jsonify(response), 200