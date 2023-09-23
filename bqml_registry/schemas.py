
from google.cloud import bigquery


class RegistrySchema():

    # Registry components
    general_fields = [
            bigquery.SchemaField("model_name", "STRING"),
            bigquery.SchemaField("created", "DATE"),
            bigquery.SchemaField("type", "STRING"),
            bigquery.SchemaField("target", "STRING"),
            bigquery.SchemaField("tuning", "STRING"),
    ]
    feature_fields = [
            bigquery.SchemaField("features", "REPEATED")
    ]
    feature_importance_fields = [
            bigquery.SchemaField("features", "RECORD", mode="REPEATED", fields=(
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("importance_weight", "FLOAT64"),
            bigquery.SchemaField("importance_gain", "FLOAT64"),
            bigquery.SchemaField("importance_cover", "FLOAT64")
            ))
    ]
    eval_fields = [
            bigquery.SchemaField("eval", "RECORD", mode="REPEATED", fields=(
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("value", "FLOAT64"),
            ))    
    ]
    training_info_fields = [
            bigquery.SchemaField("training", "RECORD", mode="REPEATED", fields=(
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("value", "FLOAT64"),
            )),
    ]
    hyperparam_fields = [
            bigquery.SchemaField("hyperparams", "RECORD", mode="REPEATED", fields=(
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("value_string", "STRING"),
            bigquery.SchemaField("value_float", "FLOAT64")
            ))
    ]

    tunning_fields = [
            bigquery.SchemaField("tunning", "RECORD", mode="REPEATED", fields=(
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("value_string", "STRING"),
            bigquery.SchemaField("value_float", "FLOAT64")
            ))
    ]

    def __init__(self, 
                 feature_importance: bool = False,
                 tunning_info: bool = True,
                 ) -> None:
        
        self.feature_importance = feature_importance
        self.tunning_info = tunning_info

    def build_schema(self) -> list:
        schema = []
        schema.extend(self.general_fields)
        
        if self.feature_importance:
            schema.extend(self.feature_importance_fields)
        else: 
            schema.extend(self.feature_fields)
            
        schema = schema + self.eval_fields + self.training_info_fields + self.hyperparam_fields
        
        if self.tunning_info:
            schema.extend(self.tunning_info)
        
        return schema
        
