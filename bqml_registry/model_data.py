from typing import List, Dict, Union, Optional, Any
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd
from .config import Config
from .model_names import ModelNames
from .connector import BigQueryConnector


class ModelData():
    """Responsible for fetching and storing model-related metadata."""
    
    def __init__(self, project_id: str, dataset_id: str, model_id: str) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.model_id = model_id
        self.fully_model_id = f"{self.project_id}.{self.dataset_id}.{self.model_id}"

        # Initialize BigQueryConnector object
        self.connector = BigQueryConnector()

        try:
            # Fetch model metadata (raw), else raise error
            model_ref = bigquery.Model(f"{self.fully_model_id}")
            model = self.connector.client.get_model(model_ref)

        except NotFound:
            raise NameError(f"Model: {self.model_id} was not found in {self.dataset_id} dataset.")
        
        self.model = model
        self.created = self.model.created.strftime('%Y-%m-%d')
        self.model_type = model.model_type
        
        # Check if model type is supported
        if self.model_type not in ModelNames.SUPPORTED_MODELS:
            raise NotImplementedError(f"Model type: {self.model_type} is not supported.")

    @property
    def metadata(self) -> Dict[str, Any]:
        """Access model metadata, training info, features and eval metrics."""

        training_runs = self.model.training_runs[0]
        return training_runs
    
    @property
    def tuning(self):
        """Provide information if hyperparameter-tunning was included."""
        return int(self.metadata.get("trainingOptions", {}).get("numTrials", 0)) > 0
    
    def fetch_target(self) -> str:
        """Fetches and returns model target variable"""
        
        target = self.metadata["trainingOptions"]["inputLabelColumns"]
        if len(target) > 1:
            raise NotImplementedError("Multiple target variables are not supported.")
        
        return target[0]
    
    def fetch_feature_names(self):
        """Fetches and returns feature names."""
        return [{"name": feature.name} for feature in self.model.feature_columns]
    
    def fetch_feature_importance(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns feature importance data."""
        
        if self.model_type not in ModelNames.TREE_MODELS:
            raise ValueError(f"Fetching feature importance is not supported for {self.model_type} model type.")

        df: pd.DataFrame = self.connector.execute_feature_importance_sql(self.fully_model_id)

        # Rename column 'feature' into name to match BigQuery schema
        df.rename(columns={'feature': 'name'}, inplace=True)

        return  df.to_dict('records')
    
    @staticmethod
    def _assign_string_type(value: Any) -> str:
        """Assign type to the value."""

        if isinstance(value, str):
            return value
        
        if isinstance(value, list):
            return "-".join(value)
        return None
    
    @staticmethod
    def _assign_float_type(value: Any) -> float:
        """Assign type to the value."""

        if not isinstance(value, str | list | None):
            return float(value)
        return None
    
    def fetch_hyperparameters(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns hyperparameters."""

        hyperparams: Dict[str, Any] = self.metadata["trainingOptions"]

        hyperparams_data = []
        for key, value in hyperparams.items():
            # Exclude target label(s) from hyperparams
            if key == 'inputLabelColumns':
                continue

            hyperparam_dict = {}
            hyperparam_dict["name"] = key

            # Determine the type of the value for proper BigQuery export
            hyperparam_dict["value_string"] = self._assign_string_type(value)
            hyperparam_dict["value_float"] = self._assign_float_type(value)
        
            hyperparams_data.append(hyperparam_dict)

        return hyperparams_data

    def fetch_eval_metrics(self) -> List[Dict[str, float]]:
        """Fetches and returns evaluation metrics."""

        if self.tuning:
            raise ValueError("""BigQuery does not provide evaluation metrics for hyperparameter-tunning models. 
                             They can be accessed with fetch_trial_info() method""")

        if self.model_type not in ModelNames.REGRESSION_MODELS | ModelNames.CLASSIFICATION_MODELS:
            raise NotImplementedError("Evaluation metrics are only supported for REGRESSOR and CLASSIFIER models")
        
        # Fetch evaluation metrics, hypertunning models have them empty
        eval_metrics: dict = self.metadata.get("evaluationMetrics", {})  

        if self.model_type in ModelNames.REGRESSION_MODELS:
            model_metrics: dict = eval_metrics.get('regressionMetrics', {})
        else:
            model_metrics: dict = eval_metrics.get('classificationMetrics', {})
            
        return [{"name": key, "value": float(value)} for key, value in model_metrics.items()]

    def fetch_training_info(self) -> List[Dict[str, float]]:
        """Fetches and returns training info."""
        
        training_info: dict = self.metadata.get("results", [])[0]
        if not training_info:
            raise ValueError("Training info is not available for this model.")
        
        return [{"name": key, "value": float(value)} for key, value in training_info.items()]
    
    def fetch_trial_info(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns trial info based on ML.TRIAL_INFO() function."""

        if not self.tuning:
            raise ValueError(f"Fetching trial info is not supported for non hyperparameter-tunning models.")

        df: pd.DataFrame = self.connector.execute_trial_info_sql(self.fully_model_id)

        # Melt Dataframe, trial_id remains as column - others are unpivoted
        cols_to_melt = [col for col in df.columns if col != 'trial_id']
        
        df_melted = pd.melt(df, id_vars=['trial_id'], value_vars=cols_to_melt, 
                            var_name='name', value_name='value')
        
        # Determine the type of the value for proper BigQuery export
        df_melted["value_string"] = df_melted['value'].apply(lambda x: self._assign_string_type(x))
        df_melted['value_float'] = df_melted['value'].apply(lambda x: self._assign_float_type(x))

        # Drop unnecessary 'value' column, save results into a dict
        df_melted.drop('value', axis=1, inplace=True)
        return df_melted.to_dict('records')
     
    def generate_model_sql(self, region: str = "us") -> str:
        """Retrive model create statement sql from information schema."""
        
        model_info: pd.DataFrame = self.connector.execute_search_model_sql(self.project_id, self.model_id, self.created, region)

        # Concatenate all rows into a single string
        return "".join(model_info["query"].to_list())
