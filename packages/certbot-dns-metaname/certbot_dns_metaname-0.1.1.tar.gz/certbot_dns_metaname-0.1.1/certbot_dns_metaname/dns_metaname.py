#!/usr/bin/env python

from certbot_dns_metaname.metaname import Client
import json
import logging

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

import os

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)

        self.metaname_endpoint = self.config.metaname_endpoint
        self.metaname_account_reference = self.config.metaname_account_reference
        self.metaname_api_key = self.config.metaname_api_key

    def more_info(self):
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using the Metaname JSON RPC API."

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )

        add("metaname_endpoint", "metaname endpoint")
        add("metaname_account_reference", "metaname account reference")
        add("metaname_api_key", "metaname api key")

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Remove TXT record from domain
        """
        self.metaname = Client(
            self.metaname_endpoint,
            self.metaname_account_reference,
            self.metaname_api_key,
        )
        records = self.metaname.dns_zone(domain)
        for record in records:
            if record["name"] == validation_name:
                logger.debug(f"Removing {record['name']} ref: {record['reference']}")
                self.metaname.delete_dns_record(domain, record["reference"])

        # return super()._cleanup(domain, validation_name, validation)

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Create TXT record for domain
        """
        response = self.metaname.create_dns_record(
            domain, {"name": validation_name, "type": "TXT", "data": validation}
        )
        self.dns_record_reference = response
        # return super()._perform(domain, validation_name, validation)

    def _setup_credentials(self) -> None:
        self.metaname = Client(
            self.metaname_endpoint,
            self.metaname_account_reference,
            self.metaname_api_key,
        )


if __name__ == "__main__":
    print(os.getenv("CERTBOT_DOMAIN"))
