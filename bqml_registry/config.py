import os
import pandas as pd
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
    
    def query(self, sql: str) -> pd.DataFrame:
        """Query BigQuery tables with sql and save results into DataFrame."""
        return self.client.query(sql).to_dataframe()
    
    def execute_trial_info_sql(self) -> pd.DataFrame:
            """Executes ML.TRIAL_INFO() function and saves results in a DataFrame."""

            trial_info_sql = f"""
                SELECT 
                    trial_id, hyperparameters.*, hparam_tuning_evaluation_metrics.*, 
                    training_loss, eval_loss, status, error_message, is_optimal
                FROM ML.TRIAL_INFO(MODEL `{self.project_id}.{self.dataset_id}.{self.model_id}`)
            """
            return self.query(trial_info_sql)

    def execute_feature_importance_sql(self) -> pd.DataFrame:
        """Executes ML.FEATURE_IMPORTANCE() function and saves results in a DataFrame."""
    
        feature_importance_sql = f"""
            SELECT *
            FROM ML.FEATURE_IMPORTANCE(MODEL `{self.project_id}.{self.dataset_id}.{self.model_id}`)
        """
        return self.query(feature_importance_sql)

    def execute_information_schema_sql(self, region: str = "us") -> pd.DataFrame:
        """Executes and fetches results from INFORMATION_SCHEMA.JOBS_BY_PROJECT view."""

        information_schema_sql = f"""
            SELECT * 
            FROM `chris-sandbox-2023.region-{region}.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
            WHERE project_id = "{self.project_id}"
        """
        return self.query(information_schema_sql)

    def execute_search_model_sql(self, region: str = "us") -> pd.DataFrame:
        """Executes query on INFORMATION_SCHEMA and searches for model creation statement."""

        search_model_sql = f"""
            SELECT *
            FROM `chris-sandbox-2023.region-{region}.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
            WHERE project_id = "{self.project_id}"
                AND statement_type = "CREATE_MODEL"
                AND state = "DONE"
                AND destination_table.table_id = "{self.model_id}"
            
            ORDER BY creation_time DESC
            LIMIT 1
        """
        return self.query(search_model_sql)