from typing import Union
import datetime
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

    def parameterized_query(self, sql: str, params: list[dict[str, str]]) -> pd.DataFrame:
        """
        Query BigQuery tables with sql and save results into DataFrame.
        Params should be a list of dicts, where each dict contains the following keys:
        name: name of the parameter, value: value of the parameter, type: type of the parameter
        """
        query_params = [ScalarQueryParameter(param["name"], param["type"], param["value"]) for param in params]
        
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

    def execute_search_model_sql(self, 
                                 project_id: str, 
                                 model_id: str, 
                                 limit_date: Union[str, datetime.datetime] = None,
                                 region: str = "us") -> pd.DataFrame:
        """Executes query on INFORMATION_SCHEMA and searches for model creation statement."""

        search_model_sql = f"""
            SELECT *
            FROM `{project_id}.region-{region}.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
            WHERE project_id = @project_id
                AND statement_type = "CREATE_MODEL"
                AND state = "DONE"
                AND destination_table.table_id = @model_id
                AND DATE(creation_time) = @limit_date
            
            ORDER BY creation_time DESC
            LIMIT 1
        """
        # Define parameters for parameterized query
        params = [
            {"name": "project_id", "type": "STRING", "value": project_id},
            {"name": "model_id", "type": "STRING", "value": model_id},
            {"name": "limit_date", "type": "DATE", "value": limit_date}
        ]

        # Execute parameterized query, raise error if no results are found
        try:  
            query_result = self.parameterized_query(search_model_sql, params)
            
        except ValueError:
            raise SQLNotFoundError(("No results found for search_model_sql query. " 
                                   "Model create statement was most likely executed on a different project."))

        return query_result