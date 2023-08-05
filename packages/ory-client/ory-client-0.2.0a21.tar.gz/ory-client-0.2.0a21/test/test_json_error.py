"""
    Ory APIs

    Documentation for all public and administrative Ory APIs. Administrative APIs can only be accessed with a valid Personal Access Token. Public APIs are mostly used in browsers.   # noqa: E501

    The version of the OpenAPI document: v0.2.0-alpha.21
    Contact: support@ory.sh
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ory_client
from ory_client.model.generic_error import GenericError
globals()['GenericError'] = GenericError
from ory_client.model.json_error import JsonError


class TestJsonError(unittest.TestCase):
    """JsonError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testJsonError(self):
        """Test JsonError"""
        # FIXME: construct object with mandatory attributes with example values
        # model = JsonError()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
