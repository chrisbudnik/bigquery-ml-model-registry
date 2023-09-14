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

    def add_model(self, model: ModelData) -> None:
        """Adds a model to the registry."""
        schema = self.fetch_schema()

        if any(field.name == 'features' for field in schema):
            features_input = model.fetch_feature_importance()
        else:
            features_input = model.fetch_feature_names()

        rows_to_insert = [{
            "model_name": model.model_id,
            "created": model.created,
            "type": model.model_type,
            "features": features_input,
            "eval": model.fetch_eval_metrics(),
            "training": model.fetch_training_info(),
            "hyperparams": model.fetch_hyperparameters(),
        }]

        # Check if 'is_tunning' exists in schema
        if any(field.name == 'tunning' for field in schema):
            rows_to_insert[0]["tunning_info"] = model.fetch_trial_info()

            self.client.insert_rows_json(self.full_table_id, rows_to_insert)

    def fetch_schema(self):
        table = self.client.get_table(self.full_table_id)
        return table.schema

