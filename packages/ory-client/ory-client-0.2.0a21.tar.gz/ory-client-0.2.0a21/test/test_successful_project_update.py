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
from ory_client.model.project import Project
from ory_client.model.warning import Warning
globals()['Project'] = Project
globals()['Warning'] = Warning
from ory_client.model.successful_project_update import SuccessfulProjectUpdate


class TestSuccessfulProjectUpdate(unittest.TestCase):
    """SuccessfulProjectUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSuccessfulProjectUpdate(self):
        """Test SuccessfulProjectUpdate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SuccessfulProjectUpdate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
