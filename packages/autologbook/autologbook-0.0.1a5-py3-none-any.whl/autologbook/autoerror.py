# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 08:13:29 2022

@author: elog-admin
"""


class AutologError(Exception):
    """Base class for autologbook exception."""

    pass


class MissingProtocolInformation(AutologError):
    """
    Missing protocol information.

    Raised when attempting to build a protocol without providing all
    needed information.
    """

    pass


class MissingWorkerParameter(AutologError):
    """
    Missing worker parameter.

    Raised when attempting to update a worker parameters without providing
    a needed parameter.
    """

    pass
