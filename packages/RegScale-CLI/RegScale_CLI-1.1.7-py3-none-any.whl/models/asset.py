#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from dataclasses import dataclass


@dataclass
class Asset:
    """Asset Model"""

    name: str
    other_tracking_number: str
    is_public: bool = True
    uuid: str = None
    serial_number: str = None
    ip_address: str = None
    mac_address: str = None
    manufacturer: str = None
    model: str = None
    asset_owner: str = None
    asset_owner_id: str = None
    operating_system: str = None
    os_version: str = None
    asset_type: str = None
    cpu: int = None
    ram: int = None
    disk_storage: int = None
    description: str = None
    status: str = None
    parent_id: int = None
    parent_module: str = None

    def __getitem__(self, key):
        """getter

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        return getattr(self, key)

    def __setitem__(self, key, value):
        """setter

        Args:
            key (_type_): _description_
            value (_type_): _description_

        Returns:
            _type_: _description_
        """
        return setattr(self, key, value)
