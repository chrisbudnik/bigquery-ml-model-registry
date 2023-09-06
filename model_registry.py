from google.cloud import bigquery


class ModelRegistry:
    def __init__(self, path_to_keys: str, project_id: str, dataset_id: str, table_id: str):
        self.client = bigquery.Client.from_service_account_json(path_to_keys)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    
    def init_table(self):
        schema = [
            bigquery.SchemaField("model_name", "STRING"),
            bigquery.SchemaField("created", "DATE"),
            bigquery.SchemaField("type", "STRING"),
            # ... (other fields)
        ]
        try:
            self.client.get_table(self.full_table_id)
            print(f"Table: {self.full_table_id} already exists!")
        except:
            self.client.create_table(bigquery.Table(self.full_table_id, schema=schema))
            print(f"Table: {self.full_table_id} successfully created.")
    
    def add_model(self, model_id: str):
        full_table_id = self.full_table_id
        feature_importance_sql = f"""
            SELECT *
            FROM ML.FEATURE_IMPORTANCE(MODEL `{self.project_id}.{self.dataset_id}.{model_id}`)
        """
        feature_importance_query = self.client.query(feature_importance_sql)
        feature_importance_results = feature_importance_query.result()

        # Store the feature importance in a list of dicts
        features = []
        for row in feature_importance_results:
            features.append({
                "name": row.feature,
                "importance_weight": row.importance_weight,
                "importance_gain": row.importance_gain,
                "importance_cover": row.importance_cover
                })
        
        # Use model reference to access it
        model_ref = bigquery.Model(f"{self.project_id}.{self.dataset_id}.{model_id}")
        model = self.client.get_model(model_ref)

        # Fetch model training data which includes hyperparams, eval and more
        metadata = model.training_runs[0]

        # Helper function for string and float value differentiation
        def value_string_classifier(value):
            return isinstance(value, str) or isinstance(value, list)

        # extract hyperparameters into dict
        hyperparams = metadata["trainingOptions"]
        hyperparams_data = [{"name": key,
                            "value_string": str(value) if value_string_classifier(value)  else None,
                            "value_float": float(value) if not value_string_classifier(value) else None}
                            for key, value in hyperparams.items()]
        hyperparams_insert = [item for item in hyperparams_data if item['name'] != 'inputLabelColumns']

        # extract evaluation metrics into dict
        eval_metrics = metadata["evaluationMetrics"]['regressionMetrics']
        eval_metrics_insert = [{"name": key, "value": float(value)} for key, value in eval_metrics.items()]

        # extract trianing info into dict
        training_info = metadata["results"][0]
        training_info_insert = [{"name": key, "value": float(value)} for key, value in training_info.items()]
        
        rows_to_insert = [{
            "model_name": model.model_id,
            "created": model.created.strftime('%Y-%m-%d'),
            "type": model.model_type,
            "features": features,
            "eval": eval_metrics_insert,
            "training": training_info_insert,
            "hyperparams": hyperparams_insert
        }]
        
        errors = self.client.insert_rows_json(full_table_id, rows_to_insert)
        if errors:
            print(f"Failed to insert rows: {errors}")
        else:
            print(f"Successfully added model: {model_id} to the registry.")



