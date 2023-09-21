import os
import pandas as pd
from google.cloud import bigquery
from googleapiclient import discovery
from google.oauth2 import service_account

class Config:
    """Base class to handle configuration and authentication."""
    _client = None
    _credentials = None

    @property
    def credentials(self):
        if Config._credentials is None:
            path_to_keys = os.environ.get("SERVICE_ACCOUNT_CREDENTIALS")
            if path_to_keys is None:
                raise EnvironmentError("The SERVICE_ACCOUNT_CREDENTIALS environment variable is not set.")
            
            Config._credentials = service_account.Credentials.from_service_account_file(
                path_to_keys,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        return Config._credentials

    @property
    def client(self):
        if Config._client is None:
            Config._client = bigquery.Client(credentials=self.credentials)
        return Config._client

    def check_permissions(self, permissions: list) -> bool:
        """Check if the service account has the required permissions."""
        service = discovery.build('cloudresourcemanager', 'v1', credentials=self.credentials)
        body = {
            'permissions': permissions
        }
        resource = f"{self.client.project}"
        request = service.projects().testIamPermissions(resource=resource, body=body)
        response = request.execute()

        # Check if all required permissions are granted
        return set(permissions).issubset(set(response.get('permissions', [])))
    
    def query(self, sql: str) -> pd.DataFrame:
        """Query BigQuery tables with sql and save results into DataFrame."""
        return self.client.query(sql).to_dataframe()


