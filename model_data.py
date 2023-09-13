from typing import List, Dict, Union, Optional
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from config import Config


class ModelData(Config):
    """Responsible for fetching and storing model-related metadata."""
    
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

    @property
    def metadata(self) -> Dict:
        """Access model metadata, training info, features and eval metrics"""
        
        training_runs = self.model.training_runs[0]
        if training_runs.get("trainingOptions", {}).get("numTrials", 0):
            raise NotImplementedError("Hyperparameter tunning models are not currently supported.")
        return training_runs
    
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

        TREE_MODELS = ("BOOSTED_TREE_REGRESSOR", "BOOSTED_TREE_CLASSIFIER", 
                       "RANDOM_FOREST_REGRESSOR", "RANDOM_FOREST_CLASSIFIER")
        
        if self.model_type not in TREE_MODELS:
            raise NotImplementedError(f"Fetching feature importance is not supported for {self.model_type} model type.")

        feature_importance_sql = f"""
            SELECT *
            FROM ML.FEATURE_IMPORTANCE(MODEL `{self.project_id}.{self.dataset_id}.{self.model_id}`)
        """
        feature_importance_results = self.client.query(feature_importance_sql).result()
    
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

        def value_type_classifier(value) -> bool:
            """Helper function that allows distinction between hyperparameter value types."""
            STRING_HYPERPARAMS = ["dataSplitMethod", "treeMethod", "categoryEncodingMethod"]
            return value in STRING_HYPERPARAMS

        hyperparams = self.metadata["trainingOptions"]
        hyperparams_data = [{"name": key,
                            "value_string": str(value) if value_type_classifier(key)  else None,
                            "value_float": float(value) if not value_type_classifier(key) else None}
                            for key, value in hyperparams.items()]
        
        return [item for item in hyperparams_data if item['name'] != 'inputLabelColumns']


    def fetch_eval_metrics(self) -> List[Dict[str, float]]:
        """Fetches and returns evaluation metrics."""
        model_class = self.model_type.split("_")[-1]

        if model_class not in ("REGRESSOR", "CLASSIFIER"):
            raise NotImplementedError("Evaluation metrics are only supported for REGRESSOR and CLASSIFIER models")
        
        if model_class == "REGRESSOR":
            eval_metrics = self.metadata["evaluationMetrics"]['regressionMetrics']
        else:
            eval_metrics = self.metadata["evaluationMetrics"]['classificationMetrics']
            
        return [{"name": key, "value": float(value)} for key, value in eval_metrics.items()]
        

    def fetch_training_info(self) -> List[Dict[str, float]]:
        """Fetches and returns training info."""
        
        training_info = self.metadata["results"][0]
        return [{"name": key, "value": float(value)} for key, value in training_info.items()]
