## `bqml_registry` File Structure

Below is a brief outline of the module's file architecture:

- `model_data.py`: The backbone of the module, housing the `ModelData` class responsible for extracting model metadata.
- `model_registry.py`: Contains the `ModelRegistry` class, used for managing the model registry, including adding and updating models.
- `model_names.py`: A storage class for handling model names and model groupings (e.g., "tree models").
- `schemas.py`: Features the `RegistrySchema` class to specify the schema of the model registry.
- `config.py`: A config class that manages BigQuery connections, querying tables, and permission checks.

### model_data.py (Backbone)

Serving as the backbone of the module, `model_data.py` contains the `ModelData` class, which is essential for fetching and handling model metadata.

#### Features:

- Extract various types of metadata for individual models.
- Support for batch metadata extraction for multiple models.

### model_registry.py

Although not the backbone, this file is critical for registry management. It hosts the `ModelRegistry` class, which provides functionalities for updating the registry, such as adding or removing models.

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

#### Features:

- Initialize BigQuery connection settings.
- Execute SQL queries on tables.
- Check and validate read/write permissions for BigQuery tables.

## Usage

For installation and setup procedures, please refer to the primary README documentation.

## Contributions

Contributions to this project are always welcome. Feel free to raise issues or submit pull requests.

## License

This project is licensed under the MIT License. For more details, refer to the [LICENSE.md](LICENSE.md) file.