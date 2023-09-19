## `bqml_registry` File Structure

Below is a brief outline of the module's file architecture:

- `model_data.py`: The backbone of the module, housing the `ModelData` class responsible for extracting model metadata.
- `model_registry.py`: Contains the `ModelRegistry` class, used for managing the model registry, including adding and updating models.
- `model_names.py`: A storage class for handling model names and model groupings (e.g., "tree models").
- `schemas.py`: Features the `RegistrySchema` class to specify the schema of the model registry.
- `config.py`: A config class that manages BigQuery connections, querying tables, and permission checks.

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

### model_registry.py

Class is critical for registry management. It hosts the `ModelRegistry` class, which provides functionalities for updating the registry, such as adding or removing models.

| Method                  | Description                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------|
| `create_registry`       | Creates a new registry table in Google BigQuery to store model information.                      |
| `add_model`             | Automatically adds a new model to the existing registry table along with all its associated metadata and evaluation metrics. |

These tables offer a concise reference to the available methods and their functionalities for both `ModelData` and `ModelRegistry`.
#### Features:

- Create a new model registry.
- Add new models to an existing registry.

### model_names.py

This file operates as a storage class for model names and their respective groups. For example, models can be categorized by their type like "tree models."

#### Features:

- Add new model names to the storage.
- Classify models into various predefined or custom groups.
- Retrieve a list of model names or groups.

### schemas.py

The `schemas.py` file includes the `RegistrySchema` class. This class allows users to define the schema of the registry, which can be tailored depending on the intended use-case and the types of models being used.

#### Features:

- Define customizable fields for the registry schema.
- Validate the data of the models against the schema during registry operations.

### config.py

The `config.py` file contains a configuration class that facilitates BigQuery connection management, enables SQL queries on BigQuery tables, and checks for the required permissions.

