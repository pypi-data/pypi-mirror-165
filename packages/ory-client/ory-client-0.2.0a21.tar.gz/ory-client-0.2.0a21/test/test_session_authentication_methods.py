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
from ory_client.model.session_authentication_method import SessionAuthenticationMethod
globals()['SessionAuthenticationMethod'] = SessionAuthenticationMethod
from ory_client.model.session_authentication_methods import SessionAuthenticationMethods


class TestSessionAuthenticationMethods(unittest.TestCase):
    """SessionAuthenticationMethods unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSessionAuthenticationMethods(self):
        """Test SessionAuthenticationMethods"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SessionAuthenticationMethods()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
