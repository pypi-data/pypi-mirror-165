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
from ory_client.model.keto_namespaces import KetoNamespaces
from ory_client.model.null_duration import NullDuration
from ory_client.model.project_revision_hooks import ProjectRevisionHooks
from ory_client.model.project_revision_identity_schemas import ProjectRevisionIdentitySchemas
from ory_client.model.project_revision_third_party_login_providers import ProjectRevisionThirdPartyLoginProviders
from ory_client.model.string_slice_json_format import StringSliceJSONFormat
globals()['KetoNamespaces'] = KetoNamespaces
globals()['NullDuration'] = NullDuration
globals()['ProjectRevisionHooks'] = ProjectRevisionHooks
globals()['ProjectRevisionIdentitySchemas'] = ProjectRevisionIdentitySchemas
globals()['ProjectRevisionThirdPartyLoginProviders'] = ProjectRevisionThirdPartyLoginProviders
globals()['StringSliceJSONFormat'] = StringSliceJSONFormat
from ory_client.model.normalized_project_revision import NormalizedProjectRevision


class TestNormalizedProjectRevision(unittest.TestCase):
    """NormalizedProjectRevision unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNormalizedProjectRevision(self):
        """Test NormalizedProjectRevision"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NormalizedProjectRevision()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
