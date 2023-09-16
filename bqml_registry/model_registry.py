from typing import List, Dict, Union, Optional, Literal
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from .config import Config
from .model_data import ModelData
from .schemas import RegistrySchema


class ModelRegistry(Config):
    """Provides an interface for interacting with the model registry table."""
    
    def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    
    def init_table(self, schema: RegistrySchema) -> None:
        """Initialize or validate the registry table."""

        if self._check_if_table_exists():
            print(f"Table: {self.full_table_id} already exists!")

        else:
            table_definition = bigquery.Table(self.full_table_id, schema=schema.value)
            self.client.create_table(table_definition)
            print(f"Table: {self.full_table_id} successfully created.")

    def add_model(self, model: ModelData) -> None:
        """Adds a model to the registry."""

        # Fetching schema to automatially collect required metrics
        schema = self.fetch_schema()

        # Create a dict with all model metadata
        model_insert_dict = {
            "model_name": model.model_id,
            "created": model.created,
            "type": model.model_type,
            "target": model.fetch_target(),
            "is_tunning": model.is_tunning
        }

        if any(field.name == 'features' for field in schema):
            model_insert_dict["feature"] = model.fetch_feature_importance()
        else:
            model_insert_dict["feature"] = model.fetch_feature_names()

        if any(field.name == 'eval' for field in schema):
            model_insert_dict["hyperparams"] = model.fetch_eval_metrics()

        if any(field.name == 'training_info' for field in schema):
            model_insert_dict["training_info"] = model.fetch_training_info()      
        
        if any(field.name == 'hyperparams' for field in schema):
            model_insert_dict["hyperparams"] = model.fetch_hyperparameters()

        if any(field.name == 'tunning' for field in schema):
            model_insert_dict["tunning"] = model.fetch_trial_info()

        self.client.insert_rows_json(self.full_table_id, [model_insert_dict])

    def fetch_schema(self):
        """Fetch model registry schema."""
        table = self.client.get_table(self.full_table_id)
        return table.schema
    
    def _check_if_table_exists(self) -> bool:
        """Check if model registry exists."""
        
        try:
            self.client.get_table(self.full_table_id)
            return True
        
        except NotFound:
            return False