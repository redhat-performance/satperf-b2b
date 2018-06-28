"""Graphite operations helper.

File: graphite.py
Description: Implementes the helpers for dealing with graphite api
             to abstract the underlying Graphite API and provide custom
             functionality on top of it.
Date: 27/06/2018
Author: Saurabh Badhwar
"""
import requests
import json

class Graphite(object):
    """Graphite API abstraction layer.

    Graphite class builds a graphite API abstraction layer
    to provide custom functionalities based on top of the
    graphite API.
    """

    def __init__(self, hostname, port, group):
        """Graphite abstraction initializer.

        Keyword arguments:
        hostname -- The hostname of the host on which graphite is running
        port -- The port on which graphite can be accessed
        group -- Inside which group the queries should be made
        """
        self.graphite_hostname = hostname
        self.graphite_port = port
        self.query_url = "{}:{}".format(self.graphite_hostname, 
                                        self.graphite_port)
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
