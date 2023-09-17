# BigQuery ML Model Registry 

## Description

The `bigquery-ml-model-registry` project leverages Google's BigQuery API in Python to create a robust and versatile machine learning model registry. Our model registry aims to make model management straightforward and systematic by including comprehensive information for each registered model.

## Features

- **Model Name**: Unique identifiers for each model
- **Model Type**: Classification, Regression, Clustering etc.
- **Features**: The features used in the model
- **Feature Importance**: Quantitative measures of the importance of each feature, where applicable
- **Performance Metrics**: Metrics like accuracy, F1-score, and RMSE to quantify the model's performance
- **Detailed Hyperparameter Specification**: Full specification of hyperparameters used in training the model

## Why Use bigquery-ml-model-registry?

1. **Versatility**: Support for a wide range of ML models.
2. **Audit Trail**: Keep a comprehensive record of model evolution for governance and troubleshooting.
3. **Interoperability**: Seamless integration with BigQuery for easy data ingestion and query.
4. **Scalability**: Designed to scale effortlessly as you add more models.
5. **Visibility**: Easy-to-use interface to query and extract model metadata.

# Prerequisites

Before diving into the functionalities, make sure you have:

- Google Cloud SDK and BigQuery Python SDK installed
- An active Google Cloud project with billing enabled
- A BigQuery dataset and model

## Setup

First, import the necessary modules.

```python
from bqml_registry import ModelRegistry, ModelData, RegistrySchema
```

## ModelData Properties & Methods

The `ModelData` class also exposes several properties that provide various types of information about the model. Here's a table describing these properties:

| Property       | Description                                                                                                 |
|----------------|-------------------------------------------------------------------------------------------------------------|
| `model`        | A `bigquery.Model` object that allows interaction with all built-in properties of the BigQuery model.        |
| `created`      | Timestamp indicating when the model was created.                                                            |
| `model_type`   | Specifies the type of the machine learning model (e.g., linear regression, neural network, etc.).            |
| `metadata`     | Contains most of the information about the model in raw format, such as hyperparameters and training data.   |
| `is_tuning`    | Boolean value that is `True` if the model involves hyperparameter tuning, otherwise `False`.                 |

Additionaly, `ModelData` class provides various methods to fetch or generate information about the model. Here are the supported methods:

| Method                  | Description                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------|
| `fetch_target`          | Fetches the target variable for the model.                                                      |
| `fetch_feature_names`   | Retrieves the names of features used in the model.                                               |
| `fetch_feature_importance` | Gets the importance of each feature in the model.                                              |
| `fetch_hyperparameters` | Retrieves the hyperparameters used in training the model.                                        |
| `fetch_eval_metrics`    | Fetches evaluation metrics for the model.                                                       |
| `fetch_training_info`   | Gets information about the training process of the model.                                        |
| `fetch_trial_info`      | Retrieves information about the different trials performed during hyperparameter tuning.         |
| `generate_model_sql`    | Generates model creation statement.                                      |

These properties and methods can be accessed directly from a `ModelData` instance, providing an easy way to obtain key details about your machine learning models in BigQuery.

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
> :Warning: **Note**: Feature importance can only be calculated for models based on decision tree algorithms, such as boosted trees or random forests. If you're using other types of models, this functionality will not be applicable.


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
registry.init_table(schema)
```

## Registering a Model to the Model Registry

After the Model Registry table is initialized, you can register models to this table. Doing so will store metadata like hyperparameters and feature importance for easy future retrieval.

Here's how to register a model:

```python
# Add model to the registry table
registry.add_model(model)
```

By following these steps, you can effectively manage your BigQuery ML models using the `bqml_registry` Python module. Feel free to explore these functionalities to improve your machine learning workflow.
