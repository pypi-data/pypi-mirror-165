import unittest

import mock
import json
import requests_mock
from certbot_dns_metaname.dns_metaname import Authenticator

from certbot import errors
from certbot.compat import os
from certbot.plugins import dns_test_common

from certbot.plugins.dns_test_common import DOMAIN

from certbot.tests import util as test_util

FAKE_USER = "remoteuser"
FAKE_PW = "password"
FAKE_ENDPOINT = "mock://endpoint"


class AuthenticatorTest(
    test_util.TempDirTestCase, dns_test_common.BaseAuthenticatorTest
):
    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        # from certbot_dns_ispconfig.dns_ispconfig import Authenticator

        path = os.path.join(self.tempdir, "file.ini")
        dns_test_common.write(
            {
                "ispconfig_username": FAKE_USER,
                "ispconfig_password": FAKE_PW,
                "ispconfig_endpoint": FAKE_ENDPOINT,
            },
            path,
        )

        super(AuthenticatorTest, self).setUp()
        self.config = mock.MagicMock(
            metaname_endpoint="http://metaname.test",
            metaname_account_reference="example.com",
            metaname_api_key="12039sdjkhf19203",
            metaname_propagation_seconds=0,
        )  # don't wait during tests

        self.auth = Authenticator(self.config, "metaname")

        self.mock_client = mock.MagicMock()
        # _get_ispconfig_client | pylint: disable=protected-access
        self.auth._get_ispconfig_client = mock.MagicMock(return_value=self.mock_client)

    def test_perform(self):
        self.auth.perform([self.achall])
        expected = [
            mock.call.add_txt_record(
                DOMAIN, "_acme-challenge." + DOMAIN, mock.ANY, mock.ANY
            )
        ]
        self.assertEqual(expected, self.mock_client.mock_calls)

    def test_cleanup(self):
        self.auth._attempt_cleanup = True
        self.auth.cleanup([self.achall])

        expected = [
            mock.call.del_txt_record(
                DOMAIN, "_acme-challenge." + DOMAIN, mock.ANY, mock.ANY
            )
        ]
        self.assertEqual(expected, self.mock_client.mock_calls)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
