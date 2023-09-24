from bqml_registry import ModelRegistry, ModelData, RegistrySchema

# Example usage
if __name__ == "__main__":
    project_id = "chris-sandbox-2023"
    dataset_id = "housing"
    table_id = "model_registry"

    # Initialize Model Registry object
    registry = ModelRegistry(project_id, dataset_id, table_id)

    # Define schema details
    schema = RegistrySchema(feature_importance=True)

    # Create model registry table
    registry.create_registry()

    # List models to add to the registry
    model_ids = ["model_forest_01", "model_forest_02", "model_forest_03"]

    # Iterate over model ids and add them to the registry
    for model in model_ids:
        # Create Model Data instance
        model = ModelData(project_id, dataset_id, model)

        # Add model to registry table 
        registry.add_model(model)
