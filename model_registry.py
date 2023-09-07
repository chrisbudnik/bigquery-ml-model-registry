from typing import List, Dict, Union, Optional
from google.cloud import bigquery
from config import Config
from model_data import ModelData


class ModelRegistry(Config):
    """Provides an interface for interacting with the model registry table."""
    
    def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    
    def init_table(self):
        """Initialize or validate the registry table."""

        schema = [
            bigquery.SchemaField("model_name", "STRING"),
            bigquery.SchemaField("created", "DATE"),
            bigquery.SchemaField("type", "STRING"),

            bigquery.SchemaField("features", "RECORD", mode="REPEATED", fields=(
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("importance_weight", "FLOAT64"),
                bigquery.SchemaField("importance_gain", "FLOAT64"),
                bigquery.SchemaField("importance_cover", "FLOAT64")
                )),

            bigquery.SchemaField("eval", "RECORD", mode="REPEATED", fields=(
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("value", "FLOAT64"),
            )),

            bigquery.SchemaField("training", "RECORD", mode="REPEATED", fields=(
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("value", "FLOAT64"),
            )),

            bigquery.SchemaField("hyperparams", "RECORD", mode="REPEATED", fields=(
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("value_string", "STRING"),
                bigquery.SchemaField("value_float", "FLOAT64")
            ))
        ]
        
        # Create table if it does not exist
        try:
            self.client.get_table(self.full_table_id)
            print(f"Table: {self.full_table_id} already exists!")
        except:
            self.client.create_table(bigquery.Table(self.full_table_id, schema=schema))
            print(f"Table: {self.full_table_id} successfully created.")

    def add_model(self, model_data: ModelData) -> None:
        """Adds a model to the registry."""
        
        rows_to_insert = [{
            "model_name": model_data.model_id,
            "created": model_data.created.strftime('%Y-%m-%d'),
            "type": model_data.model_type,
            "features": model_data.fetch_feature_importance(),
            "eval": model_data.fetch_eval_metrics(),
            "training": model_data.fetch_training_info(),
            "hyperparams": model_data.fetch_hyperparams(),
        }]
        
        self.client.insert_rows_json(self.full_table_id, rows_to_insert)

