import pandas as pd
from google.cloud import bigquery
from google.cloud.bigquery import ScalarQueryParameter, QueryJobConfig

from .config import Config
from .permissions import RequiredPermissions
from .exceptions import BigQueryPermissionError, SQLNotFoundError


class BigQueryConnector(Config):
    def __init__(self) -> None:
        if not self.check_permissions(RequiredPermissions.ALL.value):
            raise BigQueryPermissionError("Service account does not meet all permission requirements.")
        
    def query(self, sql: str) -> pd.DataFrame:
        """Query BigQuery tables with sql and save results into DataFrame."""
        return self.client.query(sql).to_dataframe()

    def parameterized_query(self, sql: str, params: dict[str: str]) -> pd.DataFrame:
        """Query BigQuery tables with sql and save results into DataFrame."""
        query_params = [ScalarQueryParameter(key, "STRING", value) for key, value in params.items()]
        
        job_config = QueryJobConfig()
        job_config.query_parameters = query_params
        
        return self.client.query(sql, job_config=job_config).to_dataframe()

    def execute_trial_info_sql(self, full_model_id: str) -> pd.DataFrame:
        """Executes ML.TRIAL_INFO() function and saves results in a DataFrame."""

        trial_info_sql = f"""
            SELECT 
                trial_id, hyperparameters.*, hparam_tuning_evaluation_metrics.*, 
                training_loss, eval_loss, status, error_message, is_optimal
            FROM ML.TRIAL_INFO(MODEL `{full_model_id}`)
        """
        return self.query(trial_info_sql)

    def execute_feature_importance_sql(self, full_model_id: str) -> pd.DataFrame:
        """Executes ML.FEATURE_IMPORTANCE() function and saves results in a DataFrame."""
    
        feature_importance_sql = f"""
            SELECT *
            FROM ML.FEATURE_IMPORTANCE(MODEL `{full_model_id}`)
        """
        return self.query(feature_importance_sql)

    def execute_search_model_sql(self, project_id: str, model_id: str, region: str = "us") -> pd.DataFrame:
        """Executes query on INFORMATION_SCHEMA and searches for model creation statement."""

        search_model_sql = f"""
            SELECT *
            FROM `{project_id}.region-{region}.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
            WHERE project_id = "{project_id}"
                AND statement_type = "CREATE_MODEL"
                AND state = "DONE"
                AND destination_table.table_id = "{model_id}"
            
            ORDER BY creation_time DESC
            LIMIT 1
        """
        try:  
            query_result = self.query(search_model_sql)
            
        except ValueError:
            raise SQLNotFoundError(("No results found for search_model_sql query. " 
                                   "Model create statement was most likely executed on a different project."))

        return query_result