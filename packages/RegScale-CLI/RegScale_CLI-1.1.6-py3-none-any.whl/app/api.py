#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard imports """

import requests
from requests.adapters import HTTPAdapter, Retry

from app.application import Application


class Api:
    """Wrapper for interacting with the RegScale API"""

    def __init__(self, app: Application):
        """_summary_

        Args:
            api_key (_type_): _description_
        """
        self.app = app
        r_session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        r_session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session = r_session
        config = app.config
        self.config = config
        self.accept = "application/json"
        self.content_type = "application/json"

    def get(self, url: str, headers: dict = None) -> requests.models.Response:
        """Get Request from RegScale endpoint.

        Returns:
            requests.models.Response: Requests reponse
        """
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "accept": self.accept,
                "Content-Type": self.content_type,
            }
        response = self.session.get(url=url, headers=headers)
        return response

    def delete(self, url: str, headers: dict = None) -> requests.models.Response:
        """Delete data from RegScale

        Args:
            url (str): _description_
            headers (dict): _description_

        Returns:
            requests.models.Response: _description_
        """
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
                "accept": self.accept,
            }
        return self.session.delete(url=url, headers=headers)

    def post(
        self, url: str, headers: dict = None, json: dict = None
    ) -> requests.models.Response:
        """Post data to RegScale.
        Args:
            endpoint (str): RegScale Endpoint
            headers (dict, optional): _description_. Defaults to None.
            json (dict, optional): json data to post. Defaults to {}.

        Returns:
            requests.models.Response: Requests reponse
        """
        if headers is None:
            response = self.session.post(url=url, headers=headers, json=json)
        else:
            response = self.session.post(url=url, headers=headers, json=json)
        return response

    def put(
        self, url: str, headers: dict = None, json: dict = None
    ) -> requests.models.Response:
        """Update data for a given RegScale endpoint.
        Args:
            url (str): RegScale Endpoint
            headers (dict, optional): _description_. Defaults to None.
            json (dict, optional): json data to post. Defaults to {}.

        Returns:
            requests.models.Response: Requests reponse
        """
        response = self.session.put(url=url, headers=headers, json=json)
        return response
