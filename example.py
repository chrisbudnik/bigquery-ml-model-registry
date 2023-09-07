from model_registry import ModelRegistry
from model_data import ModelData

# Example usage
if __name__ == "__main__":
    project_id = "your_project_id"
    dataset_id = "dataset_id"
    table_id = "model_registry"

    # Create model registry table
    registry = ModelRegistry(project_id, dataset_id, table_id)
    registry.init_table()
    
    # Add a model to the registry
    model_id = "model_name_1"
    model = ModelData(project_id, dataset_id, model_id)

    # Inspect metadata
    print(model.metadata)

    # Fetch hyperparameters
    hyperparams = model.fetch_hyperparams()
    print(hyperparams)

    # Fetch feature importance - only tree models
    importances = model.fetch_feature_importance()
    print(importances)

    # Adding model to registry (all metadata)
    registry.add_model(model_id)

    