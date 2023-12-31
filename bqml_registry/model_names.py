from enum import Enum

class ModelNames():
    # Classification Models
    LOGISTIC_REG = "LOGISTIC_REG"
    AUTOML_CLASSIFIER = "AUTOML_CLASSIFIER"
    BOOSTED_TREE_CLASSIFIER = "BOOSTED_TREE_CLASSIFIER"
    RANDOM_FOREST_CLASSIFIER = "RANDOM_FOREST_CLASSIFIER"
    DNN_CLASSIFIER = "DNN_CLASSIFIER"
    DNN_LINEAR_COMBINED_CLASSIFIER = "DNN_LINEAR_COMBINED_CLASSIFIER"

    # Regression Models
    LINEAR_REG = "LINEAR_REG"
    AUTOML_REGRESSOR = "AUTOML_REGRESSOR"
    BOOSTED_TREE_REGRESSOR = "BOOSTED_TREE_REGRESSOR"
    RANDOM_FOREST_REGRESSOR = "RANDOM_FOREST_REGRESSOR"
    DNN_REGRESSOR = "DNN_REGRESSOR"
    DNN_LINEAR_COMBINED_REGRESSOR = "DNN_LINEAR_COMBINED_REGRESSOR"
    ARIMA_PLUS = "ARIMA_PLUS"
    ARIMA_PLUS_XREG = "ARIMA_PLUS_XREG"

    # Clustering Models
    KMEANS = "KMEANS"

    # Dimensionality Reduction Models
    MATRIX_FACTORIZATION = "MATRIX_FACTORIZATION"
    PCA = "PCA"

    # AutoEncoder
    AUTOENCODER = "AUTOENCODER"

    # Deep Neural Networks (DNN) Models
    DNN_MODELS = {
        "DNN_CLASSIFIER",
        "DNN_REGRESSOR",
        "DNN_LINEAR_COMBINED_CLASSIFIER",
        "DNN_LINEAR_COMBINED_REGRESSOR"
    }

    # Tree-based Models
    TREE_MODELS = {
        "BOOSTED_TREE_CLASSIFIER",
        "BOOSTED_TREE_REGRESSOR",
        "RANDOM_FOREST_CLASSIFIER",
        "RANDOM_FOREST_REGRESSOR"
    }

    # Classification Models
    CLASSIFICATION_MODELS = {
        "LOGISTIC_REG",
        "AUTOML_CLASSIFIER",
        "BOOSTED_TREE_CLASSIFIER",
        "RANDOM_FOREST_CLASSIFIER",
        "DNN_CLASSIFIER",
        "DNN_LINEAR_COMBINED_CLASSIFIER"
    }

    # Regression Models
    REGRESSION_MODELS = {
        "LINEAR_REG",
        "AUTOML_REGRESSOR",
        "BOOSTED_TREE_REGRESSOR",
        "RANDOM_FOREST_REGRESSOR",
        "DNN_REGRESSOR",
        "DNN_LINEAR_COMBINED_REGRESSOR",
        "ARIMA_PLUS",
        "ARIMA_PLUS_XREG"
    }

    SUPPORTED_MODELS = {
        "LINEAR_REGRESSION",
        "AUTOML_REGRESSOR",
        "BOOSTED_TREE_REGRESSOR",
        "RANDOM_FOREST_REGRESSOR",
        "DNN_REGRESSOR",
        "DNN_LINEAR_COMBINED_REGRESSOR",
        "LOGISTIC_REGRESSION",
        "AUTOML_CLASSIFIER",
        "BOOSTED_TREE_CLASSIFIER",
        "RANDOM_FOREST_CLASSIFIER",
        "DNN_CLASSIFIER",
        "DNN_LINEAR_COMBINED_CLASSIFIER"
    }

