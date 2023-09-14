from typing import List, Dict, Union, Optional
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from config import Config
from model_names import ModelNames
import pandas as pd


class ModelData(Config):
    """Responsible for fetching and storing model-related metadata."""

    STRING_HYPERPARAMS = ["dataSplitMethod", "treeMethod", "categoryEncodingMethod"]
    
    def __init__(self, project_id: str, dataset_id: str, model_id: str) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.model_id = model_id

        try:
            model_ref = bigquery.Model(f"{self.project_id}.{self.dataset_id}.{model_id}")
            model = self.client.get_model(model_ref)
        except NotFound:
            raise NameError(f"Model: {self.model_id} was not found in {self.dataset_id} dataset.")
        
        self.model = model
        self.created = self.model.created.strftime('%Y-%m-%d')
        self.model_type = model.model_type

        if self.model_type not in ModelNames.SUPPORTED_MODELS:
            raise NotImplementedError(f"Model type: {self.model_type} is not supported.")

    @property
    def metadata(self) -> Dict:
        """Access model metadata, training info, features and eval metrics"""
        training_runs = self.model.training_runs[0]
        return training_runs
    
    @property
    def is_tunning(self):
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

        feature_importance_sql = f"""
            SELECT *
            FROM ML.FEATURE_IMPORTANCE(MODEL `{self.project_id}.{self.dataset_id}.{self.model_id}`)
        """
        df = self.query(feature_importance_sql)
        df.rename(columns={'feature': 'name'}, inplace=True)
        return  df.to_dict('records')
        
    def fetch_hyperparams(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns hyperparameters."""

        hyperparams = self.metadata["trainingOptions"]
        hyperparams_data = [{"name": key,
                            "value_string": str(value) if key in self.STRING_HYPERPARAMS  else None,
                            "value_float": float(value) if key not in self.STRING_HYPERPARAMS else None}
                            for key, value in hyperparams.items()]
        
        return [item for item in hyperparams_data if item['name'] != 'inputLabelColumns']


    def fetch_eval_metrics(self) -> List[Dict[str, float]]:
        """Fetches and returns evaluation metrics."""

        if self.is_tunning:
            raise ValueError("""BigQuery does not provide evaluation metrics for hyperparameter-tunning models. 
                             They are accessed in fetch_trial_info() method""")

        if self.model_type not in ModelNames.REGRESSION_MODELS | ModelNames.CLASSIFICATION_MODELS:
            raise NotImplementedError("Evaluation metrics are only supported for REGRESSOR and CLASSIFIER models")
        
        if self.model_type in ModelNames.REGRESSION_MODELS:
            eval_metrics = self.metadata["evaluationMetrics"]['regressionMetrics']
        else:
            eval_metrics = self.metadata["evaluationMetrics"]['classificationMetrics']
            
        return [{"name": key, "value": float(value)} for key, value in eval_metrics.items()]
        

    def fetch_training_info(self) -> List[Dict[str, float]]:
        """Fetches and returns training info."""
        
        training_info = self.metadata["results"][0]
        return [{"name": key, "value": float(value)} for key, value in training_info.items()]
    
    def fetch_trial_info(self) -> List[Dict[str, float]]:
        
        if not self.is_tunning:
            raise ValueError(f"Fetching trial info is not supported for non hyperparameter-tunning models.")

        trial_info_sql = f"""
            SELECT 
                trial_id, hyperparameters.*, hparam_tuning_evaluation_metrics.*, 
                training_loss, eval_loss, status, error_message, is_optimal
            FROM ML.TRIAL_INFO(MODEL `{self.project_id}.{self.dataset_id}.{self.model_id}`)
        """
        df = self.query(trial_info_sql)
        cols_to_melt = [col for col in df.columns if col != 'trial_id']

        df_melted = pd.melt(df, id_vars=['trial_id'], value_vars=cols_to_melt, 
                            var_name='name', value_name='value')
        
        # string and float columns must be in separate columns for BigQuery export
        df_melted["value_string"] = df_melted.value if isinstance(df_melted.value, str) else None
        df_melted['value_float'] = df_melted['value'].apply(lambda x: float(x) if x is not None and not isinstance(x, str) else None)

        df_melted.drop('value', axis=1, inplace=True)
        return  df_melted.to_dict('records')


