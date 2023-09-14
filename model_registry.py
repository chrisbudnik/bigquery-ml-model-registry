from typing import List, Dict, Union, Optional, Literal
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from config import Config
from model_data import ModelData
from schemas import RegistrySchema


class ModelRegistry(Config):
    """Provides an interface for interacting with the model registry table."""
    
    def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    def _replace_table(self, schema: RegistrySchema) -> None:
        """Replacee table based on provided schema."""

        self.client.delete_table(self.full_table_id, not_found_ok=True)
        self.client.create_table(bigquery.Table(self.full_table_id, schema=schema.value))
        print(f"Table: {self.full_table_id} replaced.")
    
    def init_table(self, schema: RegistrySchema, replace: bool = False) -> None:
        """Initialize or validate the registry table."""

        try:
            self.client.get_table(self.full_table_id)
            print(f"Table: {self.full_table_id} already exists!")

            if replace: self._replace_table(schema)

        except NotFound:
            self.client.create_table(bigquery.Table(self.full_table_id, schema=schema.value))
            print(f"Table: {self.full_table_id} successfully created.")

    def add_model(self, model_data: ModelData) -> None:
        """Adds a model to the registry."""
        
        rows_to_insert = [{
            "model_name": model_data.model_id,
            "created": model_data.created,
            "type": model_data.model_type,
            "features": model_data.fetch_feature_importance(),
            "eval": model_data.fetch_eval_metrics(),
            "training": model_data.fetch_training_info(),
            "hyperparams": model_data.fetch_hyperparams(),
        }]
        
        self.client.insert_rows_json(self.full_table_id, rows_to_insert)

