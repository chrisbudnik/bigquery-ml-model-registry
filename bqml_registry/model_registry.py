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
            "trial_info": self._process_trial_info(model, schema)
        }

        # Insert model metadata into the registry table
        self.connector.client.insert_rows_json(self.full_table_id, [model_insert_dict])

    def fetch_schema(self) -> List[bigquery.SchemaField]:
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

    def _process_trial_info(self, model: ModelData, schema: List[bigquery.SchemaField]) -> Dict[str, float]:
        """Process trial info."""

        # Check schema for trial info columns
        check_if_trial_column = (field.name == 'tunning' for field in schema)


        if model.tuning and check_if_trial_column:
            return model.fetch_trial_info()
        pass

    def _process_feature_importance(self, model: ModelData, schema: List[bigquery.SchemaField]):
        """Process feature importance."""

        # Check schema for feature importance columns
        check_if_importance_column = any(field.name == 'features.importance' for field in schema)

        # Cech if model is tree-based
        check_if_tree_model = model.model_type in ModelNames.TREE_MODELS

        # Logic to determine if feature importance can be calculated, else return feature names
        if check_if_importance_column and check_if_tree_model:
            return model.fetch_feature_importance()
        
        # this is a temporary solution, can cause problems with schema
        return model.fetch_feature_names()
        