import os
from google.cloud import bigquery

class Config:
    """Base class to handle configuration and authentication."""
    _client = None

    @property
    def client(self):
        if Config._client is None:
            path_to_keys = os.environ.get("SERVICE_ACCOUNT_CREDENTIALS")

            if path_to_keys is None:
                raise EnvironmentError("The SERVICE_ACCOUNT_CREDENTIALS environment variable is not set.")
            Config._client = bigquery.Client.from_service_account_json(path_to_keys)

        return Config._client
