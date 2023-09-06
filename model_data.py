from typing import List, Dict, Union, Optional
from google.cloud import bigquery
from config import Config


class ModelData(Config):
    """Responsible for fetching and storing model-related metadata."""
    
    def __init__(self, project_id: str, dataset_id: str, model_id: str):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.model_id = model_id

        try:
            model_ref = bigquery.Model(f"{self.project_id}.{self.dataset_id}.{model_id}")
            model = self.client.get_model(model_ref)

        except Exception:
            raise NameError(f"Model: {self.model_id} was not found in {self.dataset} dataset.")
        
        self.model = model
        
    def fetch_feature_importance(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns feature importance data."""

        feature_importance_sql = f"""
            SELECT *
            FROM ML.FEATURE_IMPORTANCE(MODEL `{self.project_id}.{self.dataset_id}.{self.model_id}`)
        """
        feature_importance_results = self.client.query(feature_importance_sql).result()

        # Store the feature importance in a list of dictionaries
        features = []
        for row in feature_importance_results:
            features.append({
                "name": row.feature,
                "importance_weight": row.importance_weight,
                "importance_gain": row.importance_gain,
                "importance_cover": row.importance_cover
                })
        return features
        
    def fetch_hyperparams(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns hyperparameters."""
        # ... logic for fetching hyperparameters
        return []

    def fetch_eval_metrics(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns evaluation metrics."""
        # ... logic for fetching evaluation metrics
        return []

    def fetch_training_info(self) -> List[Dict[str, Union[str, float]]]:
        """Fetches and returns training info."""
        # ... logic for fetching training information
        return []

