# :bar_chart: BigQuery ML Model Registry 

## :pencil2: Description

The `bigquery-ml-model-registry` project leverages Google's BigQuery API in Python to create a robust and versatile machine learning model registry. Our model registry aims to make model management straightforward and systematic by including comprehensive information for each registered model.

## :star2: Features

### `ModelData` Class

- **Fetching Model Metadata**: Retrieves all essential metadata associated with a BigQuery ML model, such as hyperparameters, feature names, and their importances.
- **Evaluation Metrics**: Fetches various metrics like accuracy, precision, recall, etc., which help in the evaluation and comparison of different models.

### `ModelRegistry` Class

- **Registry Creation**: Provides methods for creating a new registry table within BigQuery to store model information.
- **Automated Model Addition**: Includes functionalities to automatically add new models to the registry table with all their associated metadata and evaluation metrics.

### `RegistryTemplate` Class

- **Flexible Schema Definition**: Allows users to define the schema of the registry table based on their specific needs.
- **Three Recommended Options for Schema**:
    1. **Include All Columns**: A robust option that includes all possible columns for maximum information.
    2. **Include Feature Importance**: Tailored for scenarios where tree-based models are used, storing only feature importance data.
    3. **Focus on Tuning**: Ideal for hyperparameter tuning scenarios, includes general stats and tuning-specific information like trial performance.

## :file_folder: Repo Structure

- `bqml_registry/` - This is the main code base for the BQML Model Registry module. It contains all the necessary classes and functionalities.
- `example.py` - An example script that demonstrates how to use the various functionalities provided by the BQML Model Registry module.
- `sql-for-registry.md` - A markdown file that provides example SQL queries for handling special use-cases like pivoting hyperparameters or managing array records in the registry table.

## :gear: Prerequisites

Before diving into the functionalities, make sure you have:

- Google Cloud SDK and BigQuery Python SDK installed
- An active Google Cloud project with billing enabled
- A BigQuery dataset with saved BigQuery ML model

You can check detailed set-up guide here: `set-up-guide.md`

## :hammer_and_wrench: Setup

First, import the necessary modules.

```python
from bqml_registry import ModelRegistry, ModelData, RegistrySchema
```

## ModelData Instance Creation

To interact with a specific model, you create a `ModelData` instance. 

You can create a `ModelData` instance as follows:

```python
project_id = "project_id"
dataset_id = "dataset_id"
model_id = "model_id"

model = ModelData(project_id, dataset_id, model_id)
```

## Fetching Feature Importance

Once the `ModelData` instance is created, you can fetch feature importance to understand the impact of each feature in model predictions. 
> **Note**: Feature importance can only be calculated for models based on decision tree algorithms, such as boosted trees or random forests. If you're using other types of models, this functionality will not be applicable.


```python
# Fetch feature importance
feature_importance = model.fetch_feature_importance()
```

## Fetching Hyperparameters

You can also use the `ModelData` instance to fetch the hyperparameters that were used to train the model. This is useful for auditing, understanding the model's behavior, or planning retraining.

```python
# Fetch hyperparameters
hyperparameters = model.fetch_hyperparameters()
```

## Generating Model SQL 

To generate SQL code that was used for model creation, take advantage of the `generate_model_sql` method. 
It is one of the easiest ways to check implemented data transformations and retrive the code in general. 
Under the hood, method searches project INFORMATION_SCHEMA.JOBS. 

```python
# Generate SQL code
sql_code = model.generate_model_sql()
```

## Initializing Model Registry Table

To store metadata about multiple models, you can initialize a Model Registry table. This table is created in a BigQuery dataset.

Here's how to initialize the Model Registry table:

```python
# Create model registry instance
registry = ModelRegistry(project_id, dataset_id, "model_registry")

# Define schema details
schema = RegistrySchema(feature_importance=True)

# Initialize model registry table
registry.create_registry(schema)
```

## Registering a Model to the Model Registry

After the Model Registry table is initialized, you can register models to this table. Doing so will store metadata like hyperparameters and feature importance for easy future retrieval.

Here's how to register a model:

```python
# Add model to the registry table
registry.add_model(model)
```

By following these steps, you can effectively manage your BigQuery ML models using the `bqml_registry` Python module. Feel free to explore these functionalities to improve your machine learning workflow.