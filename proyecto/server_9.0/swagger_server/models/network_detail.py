# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class NetworkDetail(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, bssid: str=None, essid: str=None, security: str=None, channel: int=None):  # noqa: E501
        """NetworkDetail - a model defined in Swagger

        :param bssid: The bssid of this NetworkDetail.  # noqa: E501
        :type bssid: str
        :param essid: The essid of this NetworkDetail.  # noqa: E501
        :type essid: str
        :param security: The security of this NetworkDetail.  # noqa: E501
        :type security: str
        :param channel: The channel of this NetworkDetail.  # noqa: E501
        :type channel: int
        """
        self.swagger_types = {
            'bssid': str,
            'essid': str,
            'security': str,
            'channel': int
        }

        self.attribute_map = {
            'bssid': 'BSSID',
            'essid': 'ESSID',
            'security': 'Security',
            'channel': 'Channel'
        }
        self._bssid = bssid
        self._essid = essid
        self._security = security
        self._channel = channel

    @classmethod
    def from_dict(cls, dikt) -> 'NetworkDetail':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NetworkDetail of this NetworkDetail.  # noqa: E501
        :rtype: NetworkDetail
        """
        return util.deserialize_model(dikt, cls)

    @property
    def bssid(self) -> str:
        """Gets the bssid of this NetworkDetail.

        La dirección MAC del punto de acceso.  # noqa: E501

        :return: The bssid of this NetworkDetail.
        :rtype: str
        """
        return self._bssid

    @bssid.setter
    def bssid(self, bssid: str):
        """Sets the bssid of this NetworkDetail.

        La dirección MAC del punto de acceso.  # noqa: E501

        :param bssid: The bssid of this NetworkDetail.
        :type bssid: str
        """
        if bssid is None:
            raise ValueError("Invalid value for `bssid`, must not be `None`")  # noqa: E501

        self._bssid = bssid

    @property
    def essid(self) -> str:
        """Gets the essid of this NetworkDetail.

        El nombre de la red expuesto (SSID).  # noqa: E501

        :return: The essid of this NetworkDetail.
        :rtype: str
        """
        return self._essid

    @essid.setter
    def essid(self, essid: str):
        """Sets the essid of this NetworkDetail.

        El nombre de la red expuesto (SSID).  # noqa: E501

        :param essid: The essid of this NetworkDetail.
        :type essid: str
        """

        self._essid = essid

    @property
    def security(self) -> str:
        """Gets the security of this NetworkDetail.

        Tipo de seguridad de la red, como WPA, WPA2.  # noqa: E501

        :return: The security of this NetworkDetail.
        :rtype: str
        """
        return self._security

    @security.setter
    def security(self, security: str):
        """Sets the security of this NetworkDetail.

        Tipo de seguridad de la red, como WPA, WPA2.  # noqa: E501

        :param security: The security of this NetworkDetail.
        :type security: str
        """

        self._security = security

    @property
    def channel(self) -> int:
        """Gets the channel of this NetworkDetail.

        El canal en el que opera la red.  # noqa: E501

        :return: The channel of this NetworkDetail.
        :rtype: int
        """
        return self._channel

    @channel.setter
    def channel(self, channel: int):
        """Sets the channel of this NetworkDetail.

        El canal en el que opera la red.  # noqa: E501

        :param channel: The channel of this NetworkDetail.
        :type channel: int
        """

        self._channel = channel
