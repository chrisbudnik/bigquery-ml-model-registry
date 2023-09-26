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
            "is_tunning": model.tuning,
        }
        # if features.importance is in the schema, add feature importance to the dict
        if any(field.name == 'features.importance' for field in schema):
            # Raise an error if model is not tree-based (no support for feature importance)
            if model.model_type not in ModelNames.TREE_MODELS:
                raise ValueError("Feature importance can be only calculated for tree-based models.")
            
            model_insert_dict["features"] = model.fetch_feature_importance()
        else:
            model_insert_dict["features"] = model.fetch_feature_names()

        # Add additional model metadata to the dict
        metadata_dict = {
            "eval": model.fetch_eval_metrics(),
            "trainint_info": model.fetch_training_info(),
            "hyperparams": model.fetch_hyperparameters()
        }
        model_insert_dict = model_insert_dict | metadata_dict

        # Add tunning info if it exists
        if any(field.name == 'tunning' for field in schema):
            model_insert_dict["tunning"] = model.fetch_trial_info()

        # Insert model metadata into the registry table
        self.connector.client.insert_rows_json(self.full_table_id, [model_insert_dict])

    def fetch_schema(self):
        """Fetch model registry schema."""
        table = self.connector.client.get_table(self.full_table_id)
        return table.schema
    
    def _check_if_table_exists(self) -> bool:
        """Check if model registry exists."""

        try:
            self.connector.client.get_table(self.full_table_id)
            return True
        
        except NotFound:
            return False
        
    def _process_eval_metrics(self, eval_metrics: Dict[str, float]) -> Dict[str, float]:
        """Process evaluation metrics."""
        pass

    def _process_trial_info(self, trial_info: Dict[str, float]) -> Dict[str, float]:
        """Process trial info."""
        pass

    def _process_feature_importance(self, feature_importance: Dict[str, float]) -> Dict[str, float]:
        """Process feature importance."""
        pass