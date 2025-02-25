# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class URL(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, url: str=None):  # noqa: E501
        """URL - a model defined in Swagger

        :param url: The url of this URL.  # noqa: E501
        :type url: str
        """
        self.swagger_types = {
            'url': str
        }

        self.attribute_map = {
            'url': 'URL'
        }
        self._url = url

    @classmethod
    def from_db(cls, job_db):

        return cls(
            url = job_db.URL

        )

    @classmethod
    def from_dict(cls, dikt) -> 'URL':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The URL of this URL.  # noqa: E501
        :rtype: URL
        """
        return util.deserialize_model(dikt, cls)

    @property
    def url(self) -> str:
        """Gets the url of this URL.


        :return: The url of this URL.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this URL.


        :param url: The url of this URL.
        :type url: str
        """

        self._url = url
