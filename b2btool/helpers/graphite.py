"""Graphite operations helper.

File: graphite.py
Description: Implementes the helpers for dealing with graphite api
             to abstract the underlying Graphite API and provide custom
             functionality on top of it.
Date: 27/06/2018
Author: Saurabh Badhwar
"""
import requests


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
        self.query_url = "{}:{}".format(self.graphite_hostname,self.graphite_port)
        if self.__validate_group(group):
            self.lookup_group = group
        else:
            raise Exception("Unable to find the required data group in graphite")

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
