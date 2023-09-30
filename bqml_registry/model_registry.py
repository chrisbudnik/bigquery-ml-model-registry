from typing import List, Dict, Union, Optional, Literal
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from .config import Config
from .model_data import ModelData
from .schemas import RegistrySchema
from .model_names import ModelNames
from .connector import BigQueryConnector


class ModelRegistry():
    """Provides an interface for interacting with the model registry table."""
    
    def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"

        # Initialize BigQueryConnector object
        self.connector = BigQueryConnector()
    
    def create_registry(self, schema: RegistrySchema) -> None:
        """Initialize or validate the registry table."""

        if self._check_if_table_exists():
            print(f"Table: {self.full_table_id} already exists!")

        else:
            table_definition = bigquery.Table(self.full_table_id, schema=schema.build_schema())
            self.connector.client.create_table(table_definition)
            print(f"Table: {self.full_table_id} successfully created.")

    def add_model(self, model: ModelData) -> None:
        """Adds a model to the registry."""

        # Fetching schema to automatially collect required metrics
        schema = self.fetch_schema()

        # Create a dict with general model metadata
        model_insert_dict = {
            "model_name": model.model_id,
            "created": model.created,
            "type": model.model_type,
            "target": model.fetch_target(),
            "tuning": model.tuning,
            "features": self._process_feature_importance(model, schema),
            "eval": model.fetch_eval_metrics(),
            "trainint_info": model.fetch_training_info(),
            "hyperparams": model.fetch_hyperparameters(),
        }

        # Check schema for tunning trials info columns
        if any(field.name == 'tunning' for field in schema):
            model_insert_dict["tunning"] = self._process_trial_info(model, schema)

        # Insert model metadata into the registry table
        self.connector.client.insert_rows_json(self.full_table_id, [model_insert_dict])

    def fetch_schema(self) -> List[bigquery.SchemaField]:
        """Fetch model registry schema."""

        if not self._check_if_table_exists():
            raise NameError(f"Table: {self.full_table_id} does not exist.")

        table = self.connector.client.get_table(self.full_table_id)
        return table.schema
    
    def _check_if_table_exists(self) -> bool:
        """Check if model registry exists."""

        try:
            self.connector.client.get_table(self.full_table_id)
            return True
        
        except NotFound: return False
        
    def _process_eval_metrics(self, eval_metrics: Dict[str, float]) -> Dict[str, float]:
        """Process evaluation metrics to fit BigQuery schema."""
        pass

    def _process_trial_info(self, model: ModelData, schema: List[bigquery.SchemaField]) -> Dict[str, float]:
        """Process trial info to fit BigQuery schema."""

        # Logic to determine if trial info can be calculated
        if model.tuning:
            return model.fetch_trial_info()
        
        # if schema includes hyperparameter tunning columns, but model is not tuned
        return [{"name": None, "value_string": None, 'value_float': None}]

    def _process_feature_importance(self, model: ModelData, schema: List[bigquery.SchemaField]):
        """Process feature importance to fit BigQuery schema."""

        # Check schema for feature importance columns
        check_if_importance_column = any(field.name == 'features.importance' for field in schema)

        # Cech if model is tree-based
        check_if_tree_model = model.model_type in ModelNames.TREE_MODELS

        # Logic to determine if feature importance can be calculated
        if check_if_importance_column and check_if_tree_model:
            return model.fetch_feature_importance()
        
        # if model is not tree-based, but feature importance columns exist
        if check_if_importance_column:
            return self._process_feature_names(model)
        
        # this is a temporary solution, can cause problems with schema
        return model.fetch_feature_names()
        
    
    def _process_feature_names(self, model: ModelData) -> List[Dict[str, str]]:
        """Process feature names to fit BigQuery schema."""
        
        # Create dummy feature importance dict with None values that will convert into null values in BigQuery
        dummy_feature_importance = {"importance_weight": None, "importance_gain": None, "importance_cover": None}

        # Create a list of dicts with feature names and dummy feature importance
        return [item | dummy_feature_importance for item in model.fetch_feature_names()]
        
        