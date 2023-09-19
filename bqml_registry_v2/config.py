import os
import pandas as pd
from google.cloud import bigquery  
from google.cloud import iam_v1
from google.cloud.iam_v1.types import TestIamPermissionsRequest

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

    def check_permissions(self, resource: str, permissions: list) -> bool:
        """Check if the service account has the required permissions."""
        iam_client = iam_v1.IAMPolicyClient(client_options={"api_endpoint": "iam.googleapis.com"})
        request = TestIamPermissionsRequest(resource=resource, permissions=permissions)
        response = iam_client.test_iam_permissions(request=request)

        # Check if all required permissions are granted
        return set(permissions).issubset(set(response.permissions))

    def query(self, sql: str) -> pd.DataFrame:
        """Query BigQuery tables with sql and save results into DataFrame."""
        # Check permissions before making the query
        resource = f"projects/{self.client.project}"
        permissions = ["bigquery.tables.getData"]

        if not self.check_permissions(resource, permissions):
            raise PermissionError("Service account does not have the required permissions to perform this query.")
        
        return self.client.query(sql).to_dataframe()

    