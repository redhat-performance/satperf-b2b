"""Graphite operations helper.

File: graphite.py
Description: Implementes the helpers for dealing with graphite api
             to abstract the underlying Graphite API and provide custom
             functionality on top of it.
Date: 27/06/2018
Author: Saurabh Badhwar
"""
from datetime import datetime
import requests
import json

class Graphite(object):
    """Graphite API abstraction layer.

    Graphite class builds a graphite API abstraction layer
    to provide custom functionalities based on top of the
    graphite API.
    """

    def __init__(self, app):
        """Graphite abstraction initializer.

        Keyword arguments:
        app -- The flask application object
        """
        self.graphite_hostname = app.config.get('GRAPHITE_HOSTNAME')
        self.graphite_port = app.config.get('GRAPHITE_PORT')
        self.query_url = "{}:{}".format(self.graphite_hostname, 
                                        self.graphite_port)
        group = app.config.get('GRAPHITE_QUERY_GROUP')
        if self.__validate_group(group):
            self.lookup_group = group
        else:
            raise Exception("Unable to find the required data group in \
                            graphite")

    def get_metrics(self, hostname):
        """Get the metrics from the graphite server.

        The method provides functionality for retrieving the metrics from
        the graphite server which are present under a provided hostname.

        Keyword arguments:
        hostname -- The hostname for which the metrics needs to be retrieved

        Returns:
            List

        """
        self.query_url = "{}:{}/metrics/find?query={}.{}.*".format(self.graphite_hostname, self.graphite_port, self.lookup_group, hostname)
        req = requests.get(self.query_url)
        response_data = json.loads(req.text)
        metrics = []
        for metric in response_data:
            metrics.append(metric['id'])
        return metrics

    def get_measurable_metrics(self, path):
        """Get the measurable metric paths.

        The method provides a mechanism for retrieving the measurable
        metric paths from the provided expandable path.

        Keyword arguments:
        path -- The path from which measurable metrics need to be gathered

        Returns:
            List
        
        """
        self.query_url = "{}:{}/metrics/find?query={}.*".format(self.graphite_hostname, self.graphite_port, path)
        req = requests.get(self.query_url)
        response_data = json.loads(req.text)
        metrics = []
        for metric in response_data:
            if metric['lead'] == 1:
                metrics.append(metric['id'])
            else:
                tmp_metrics = self.get_measurable_metrics(metric['id'])
                for tmp_metric in tmp_metrics:
                    metrics.append(tmp_metric)
        return metrics

    def get_metric_data(self, metric, start_time, end_time):
        """Retrieve the metric data from the server.

        The method provides a mechanism for retrieving the metric data
        from the server provided a lead node metric path.

        Keyword arguments:
        metric -- The leaf node metric path to retrieve the data for
        start_time -- Python datetime format start time for metrics
        end_time -- Python datetime format end time for metrics

        Returns:
            dict
        """
        start_time = start_time.strftime('%H:%M_%Y%m%d')
        end_time = end_time.strftime('%H:%M_%Y%m%d')
        self.query_url = "{}:{}/render?target={}&from={}&until={}&format=json".format(self.graphite_hostname, self.graphite_port,metric,start_time,end_time)
        req = requests.get(self.query_url)
        response_data = json.loads(req.text)
        return response_data

    def __validate_group(self, group):
        """Validate the provided group.
        
        The method is used to validate if the provided group exists or not
        inside the graphite storage.

        Keyword Arguments:
        group -- The name of the group to lookup

        Returns:
            bool

        """
        query = self.query_url + "/metrics/find?query={}.*".format(group)
        resp = requests.get(query)
        if len(resp.content) > 2:
            return True
        return False
