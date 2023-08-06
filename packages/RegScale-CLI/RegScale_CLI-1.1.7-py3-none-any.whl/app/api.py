#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard imports """

import concurrent.futures

import requests
from requests.adapters import HTTPAdapter, Retry
from rich.progress import Progress

from app.application import Application
from app.logz import create_logger


class Api:
    """Wrapper for interacting with the RegScale API"""

    def __init__(self, app: Application):
        """_summary_

        Args:
            api_key (_type_): _description_
        """
        self.app = app
        logger = create_logger()
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
        self.logger = logger

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
            headers = {
                "Authorization": self.config["token"],
            }

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
        if headers is None:
            headers = {
                "Authorization": self.config["token"],
            }
        response = self.session.put(url=url, headers=headers, json=json)
        return response

    def update_server(
        self,
        url: str,
        headers: dict = None,
        json_list=None,
        method="post",
        config=None,
        message="Working",
    ):
        """Concurrent Post or Put of multiple objects

        Args:
            url (str): _description_
            headers (dict): _description_
            dict_list (list): _description_

        Returns:
            _type_: _description_
        """
        if headers is None and config:
            headers = {"Accept": "application/json", "Authorization": config["token"]}
        if json_list and len(json_list) > 0:
            with Progress(transient=False) as progress:
                task = progress.add_task(message, total=len(json_list))
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    if method == "post":
                        result_futures = list(
                            map(
                                lambda x: executor.submit(self.post, url, headers, x),
                                json_list,
                            )
                        )
                    for future in concurrent.futures.as_completed(result_futures):
                        try:
                            self.logger.debug(
                                "result is %s", future.result().status_code
                            )
                            progress.update(task, advance=1)
                        except Exception as ex:
                            self.logger.error("e is %s, type: %s", ex, type(ex))
