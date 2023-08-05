import json
import logging

import pandas as pd
import requests
from dns.dns_types import record_types

logger = logging.getLogger(__name__)


def update(
    record_name: str, record_type: str, record_content: str, api_config: dict
) -> None:
    """
    Update a DNS record.

    This function updates one DNS record using porkbun API and a secrets dictionary
    with API key and secret.

    Parameters
    ----------
    record_name: str
        name of the DNS record to be inserted.

    record_type: str
        type of the record to be inserted. It has to be one of the following list:
        - A
        - MX
        - CNAME
        - ALIAS
        - TXT
        - NS
        - AAAA
        - SRV
        - TLSA
        - CAA

    record_content: str
        the value of the record.

    api_config: dict
        dictionary containing the API endpoint, apikey, secretapikey and the
        values above, to be sent as payload to the API request.

    """

    if record_type not in record_types:
        logger.error(f"Wrong record type. Must be one of the following: {record_types}")
        raise requests.exceptions.ConnectionError
    try:
        api_config["name"] = record_name
        api_config["type"] = record_type
        api_config["content"] = record_content

        requests.post(
            api_config["endpoint"],
            data=json.dumps(api_config),
        )
        logger.info(
            f"Record updated: {record_name} \t {record_type} \t {record_content}"
        )

    except requests.exceptions.ConnectionError as e:
        logger.error(e, record_name, record_type, record_content)


def bulk_update(domain_db: str, secrets: str) -> None:
    """
    Update DNS records in bulk.

    This function updates the DNS records from a domain database file,
    in CSV format.

    Parameters
    ----------
    domain_db_filename: str
        The path of the domain database file.

    secrets: str
        The path of the file with the API secrets.

    """
    df = pd.read_csv(domain_db)
    domains = df[["host", "type", "answer"]].to_dict("records")

    with open(secrets, "r") as f:
        api_config = json.load(f)

    for entry in domains:
        update(entry["host"], entry["type"], entry["answer"], api_config)
