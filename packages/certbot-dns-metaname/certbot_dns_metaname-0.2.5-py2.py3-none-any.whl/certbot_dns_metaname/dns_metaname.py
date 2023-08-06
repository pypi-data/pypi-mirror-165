#!/usr/bin/env python

from certbot_dns_metaname.metaname import Client
import json
import logging

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
import zope

import os

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    def more_info(self):
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using the Metaname JSON RPC API."

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )

        add("credentials", help="Credentials file for the Metaname API")

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Remove TXT record from domain
        """
        self.metaname = self._get_metaname_client()
        parent_domain = self.credentials.conf("username")

        records = self.metaname.dns_zone(parent_domain)
        for record in records:
            if record["name"] == validation_name:
                logger.debug(f"Removing {record['name']} ref: {record['reference']}")
                self.metaname.delete_dns_record(parent_domain, record["reference"])

        # return super()._cleanup(domain, validation_name, validation)

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Create TXT record for domain
        """
        self.metaname = self._get_metaname_client()
        parent_domain = self.credentials.conf("username")
        # Add . to end of validation name to make it fully qualified

        response = self.metaname.create_dns_record(
            parent_domain,
            {"name": validation_name + ".", "type": "TXT", "data": validation},
        )
        self.dns_record_reference = response
        # return super()._perform(domain, validation_name, validation)

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "Metaname credentials INI file",
            {
                "endpoint": "URL of the Metaname Remote API.",
                "username": "Username for Metaname Remote API.",
                "api_key": "API key for Metaname Remote API.",
            },
        )

    def _get_metaname_client(self):
        return Client(
            self.credentials.conf("endpoint"),
            self.credentials.conf("username"),
            self.credentials.conf("api_key"),
        )
