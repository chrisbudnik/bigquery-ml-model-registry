from enum import Enum
from google.cloud import bigquery


class RegistrySchema(Enum):
    general_registry = [
            bigquery.SchemaField("model_name", "STRING"),
            bigquery.SchemaField("created", "DATE"),
            bigquery.SchemaField("type", "STRING"),
            bigquery.SchemaField("target", "STRING"),

            bigquery.SchemaField("features", "STRING"),

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
    tree_registry = [
            bigquery.SchemaField("model_name", "STRING"),
            bigquery.SchemaField("created", "DATE"),
            bigquery.SchemaField("type", "STRING"),
            bigquery.SchemaField("target", "STRING"),

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