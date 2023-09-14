
from google.cloud import bigquery


class RegistrySchema():

    # Registry components
    general_fields = [
            bigquery.SchemaField("model_name", "STRING"),
            bigquery.SchemaField("created", "DATE"),
            bigquery.SchemaField("type", "STRING"),
            bigquery.SchemaField("target", "STRING"),
            bigquery.SchemaField("is_tunning", "STRING"),
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

    def __init__(self, 
                 general_fields: bool = True,
                 feature_importance: bool = False,
                 evaluation: bool = True,
                 training_info: bool = True,
                 hyperparameters: bool = True,
                 tunning_info: bool = True,
                 ) -> None:
        
        self.general_fields = general_fields
        self.feature_importance = feature_importance
        self.evaluation = evaluation
        self.training_info = training_info
        self.hyperparameters = hyperparameters
        self.tunning_info = tunning_info

    def build_schema(self) -> list:
        schema = []
        
        if self.general_fields:
            schema.extend(self.general_fields)
        
        if self.feature_importance:
            schema.extend(self.feature_importance_fields)
            
        if self.evaluation:
            schema.extend(self.eval_fields)
        
        if self.training_info:
            schema.extend(self.training_info_fields)
        
        if self.hyperparameters:
            schema.extend(self.hyperparam_fields)
        
        return schema
        
