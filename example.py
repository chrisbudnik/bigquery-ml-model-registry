from bqml_registry import ModelRegistry, ModelData

from pprint import pprint

# Example usage
if __name__ == "__main__":
    project_id = "chris-sandbox-2023"
    dataset_id = "housing"
    table_id = "model_registry"

    # Create model registry table
    registry = ModelRegistry(project_id, dataset_id, table_id)
    registry.create_registry()
    
    # Add a model to the registry
    model_id = "model_forest_03"
    model = ModelData(project_id, dataset_id, model_id)

    # Inspect metadata
    pprint(model.metadata)

    # Fetch hyperparameters
    hyperparams = model.fetch_hyperparameters()
    pprint(hyperparams)

    # Fetch feature importance - only tree models
    importances = model.fetch_feature_importance()
    pprint(importances)

    # Adding model to registry (all metadata)
    #registry.add_model(model)

    