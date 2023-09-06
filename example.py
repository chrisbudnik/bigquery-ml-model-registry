from model_registry import ModelRegistry

# Example usage
if __name__ == "__main__":
    path_to_keys = "path/to/service-account-key.json"
    project_id = "your_project_id"
    dataset_id = "dataset_id"
    table_id = "model_registry"

    registry = ModelRegistry(path_to_keys, project_id, dataset_id, table_id)
    
    # Add a model to the registry
    model_id = "model_name_1"
    registry.add_model(model_id)