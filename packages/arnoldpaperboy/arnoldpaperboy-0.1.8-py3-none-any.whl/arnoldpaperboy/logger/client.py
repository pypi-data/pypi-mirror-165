# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.rst.
"""Interfact to google.cloud.logging.Client"""

from google.cloud.logging import Client


def get_stackdriver_client(project):
    """Return the stackdriver logging client for a project.

    Args:
        project (str): the google project id

    Returns:
        Client: the logging client.
    """
    return Client(project=project)
