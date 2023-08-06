"""
Ometria API
http://docs.ometria.com/apis/data_api_v2/
- the env vars for the authentication are stored on the kubernetes cluster
under 'ometria-access-credentials'
- functionality:
    set api credentials
    send custom events
    send contact
"""
import logging
import os
import requests
import datetime
import time

class OmetriaExecutor:
    """
    Ometria API handler.
    Args:
        env: switch between environments in Ometria,
            'staging' - for testing
            'prod_marketing' - for marketing emails
            'prod_service' - for service emails
    Attributes:
        api_endpoint: the base API endpoint
        api_key: required for authentication
        api_headers: header to be included in the request
        payload: the formatted payload to be sent
        response: the response from the API call
        queue_safety_limit: limit at which backoff begins
        contact_payload_limit: maximum number of contact records in a single call
        contact_required_fields: required fields for a contact type call
    Returns:
        OmetriaExecutor object
    """

    def __init__(self, env: str):
        """
        Initiate and collect API credentials.
        """
        self.env = env
        self.api_endpoint = "https://api.ometria.com/v2"
        self.api_key = None
        self.api_headers = None
        self.payload = None
        self.response = None
        self.set_api_credentials()
        self.queue_safety_limit = 10000
        self.contact_payload_limit = 100
        self.contact_required_fields = ('id', '@type', 'email')

    def set_api_credentials(self):
        """
        Collect API credentials depending on the environment.
        """
        # api key
        if self.env == "staging":
            api_key_env_var = "OMETRIA_STAGING_API_KEY"
        elif self.env == "prod_marketing":
            api_key_env_var = "OMETRIA_MARKETING_API_KEY"
        elif self.env == "prod_service":
            api_key_env_var = "OMETRIA_SERVICE_API_KEY"
        else:
            raise KeyError(f"Unknown env - {self.env}")

        if api_key_env_var in os.environ:
            self.api_key = os.getenv(api_key_env_var)
            logging.info("API credentials set")
        else:
            raise KeyError(f"Env var {api_key_env_var} does not exist")

        # headers
        self.api_headers = {
            "X-Ometria-Auth": self.api_key,
            "Content-Type": "application/json"
        }

    def send_custom_events(self):
        """
        Send custom_event type of payload to Ometria, save the API response.
        """
        if self.payload:
            # check if payload length is valid - 100 items per send
            payload_len = len(self.payload)
            if payload_len <= 100:
                # request - not adding retry for POST request
                self.response = requests.post(
                    json=self.payload,
                    url=f"{self.api_endpoint}/push",
                    headers=self.api_headers
                )
                logging.info(f"Sent {payload_len} 'custom_events' items")
                self.payload = None

            else:
                raise ValueError(
                    f"Payload too big - {payload_len}, max 100 items"
                )
        else:
            logging.info("No send - empty payload")

    def send_contact(self, payload: list) -> tuple:
        """
        Send a single contact payload to Ometria, backs off when the remaining queue size hits a safety limit

        Args:
            session: the client session
            payload: list of json records to be uploaded

        Returns:
            Tuple of 3 items: a timestamp of when the payload was sent, a list of the uids in the payload, the response json
        """
        self.validate_contact_payload(payload)
        timestamp = datetime.datetime.now()
        uids = [record['id'] for record in payload]
        response = requests.post(f"{self.api_endpoint}/push", json=payload, headers=self.api_headers)
        
        if response.status_code != 202:
            raise ValueError(f"Server responded with {response.status_code} - {response.reason}")
        
        queue_remaining = int(response.headers['X-QueueSize-Remaining'])
        self.backoff(queue_remaining)
        return timestamp, uids, response.json()

    def backoff(self, queue_remaining: int):
        """
        Slow down the rate at which contact calls are made to Ometria to prevent hitting the queue limit

        Args:
            queue_remaining: the number of free slots remaining in the queue
        """
        breach = self.queue_safety_limit - queue_remaining
        if breach > 0:
            delay_time = int((1000 + breach)/1000) * 10
            logging.info(f"Passed queue safety limit of {self.queue_safety_limit}, remaining queue is {queue_remaining}, waiting {delay_time} seconds")
            time.sleep(delay_time)
            logging.info(f"{delay_time} seconds elapsed, resuming...")

    def validate_contact_payload(self, payload: list) -> list:
        """
        Validates contact payloads before uploading, checks that no chunk is > 100 and the individual json records contain the required fields

        Args:
            payloads: a chunked list (max 100 per chunk) of contact records to be uploaded
        """
        if len(payload) > self.contact_payload_limit:
            raise ValueError(f"Payload chunk has size > {self.contact_payload_limit}")
        for record_idx, record in enumerate(payload):
            try:
                [record[field] for field in self.contact_required_fields]
            except KeyError as e:
                logging.error(f"Contact record {record_idx} is missing a required field: {e}")
                raise
