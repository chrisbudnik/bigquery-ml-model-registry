from typing import List, Dict, Union, Optional
from google.cloud import bigquery
from config import Config
from model_data import ModelData



class ModelRegistry(Config):
    """Provides an interface for interacting with the model registry table."""
    
    def __init__(self, path_to_keys: str, project_id: str, dataset_id: str, table_id: str):
        self.client = bigquery.Client.from_service_account_json(path_to_keys)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    
    def init_table(self):
        """Initialize or validate the registry table."""
        # ... table initialization logic

    def add_model(self, model_data: ModelData):
        """Adds a model to the registry."""
        
        rows_to_insert = [{
            "model_name": model_data.model_id,
            "features": model_data.fetch_feature_importance(),
            "hyperparams": model_data.fetch_hyperparams(),
            "eval": model_data.fetch_eval_metrics(),
            "training": model_data.fetch_training_info()
            # ... other fields
        }]
        
        errors = self.client.insert_rows_json(self.full_table_id, rows_to_insert)
        if errors:
            print(f"Failed to insert rows: {errors}")
        else:
            print(f"Successfully added model: {model_data.model_id} to the registry.")
