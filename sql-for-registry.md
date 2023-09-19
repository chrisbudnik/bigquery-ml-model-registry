# SQL Explanation for Pivoting Hyperparameters

The given SQL script is designed to restructure data related to machine learning models' hyperparameters. It pivots hyperparameters into their respective columns for easier usage and model filtering. The script is divided into several parts:

## `hparams_float` (CTE)

This CTE focuses on hyperparameters that have floating-point values.

```sql
WITH hparams_float as (
  SELECT *
  FROM (
    SELECT  model_name, hparams,
    FROM `project_id.dataset_id.table_id`, UNNEST(hyperparams) hparams
  )
  PIVOT(
    MAX(hparams.value_float) FOR hparams.name 
    IN ("l1Regularization","l2Regularization", "maxTreeDepth", "numParallelTree", "subsample", 
    "minRelativeProgress", "earlyStop", "colsampleBytree", "colsampleBylevel", "colsampleBynode")
  )
)
```

- It first unnests the `hyperparams` array from the main table (`project_id.dataset_id.table_id`).
- Then, the `PIVOT` operation pivots these unrolled records into separate columns based on hyperparameter names like "l1Regularization", "l2Regularization", etc.
- `MAX(hparams.value_float)` function is used to get the maximum value, if there are duplicates.

## `hparams_string` (CTE)

This CTE focuses on hyperparameters that have string values.

```sql
hparams_string as (
  SELECT *
  FROM (
    SELECT  model_name, hparams,
    FROM `project_id.dataset_id.table_id`, UNNEST(hyperparams) hparams
  )
  PIVOT(
    MAX(hparams.value_string) FOR hparams.name IN ("treeMethod","dataSplitMethod", "categoryEncodingMethod")
  )
)
```

- Similar to `hparams_float`, it unnests and then pivots based on hyperparameter names like "treeMethod", "dataSplitMethod", etc.
- `MAX(hparams.value_string)` function is used to handle duplicates.
- `hparams_float` and `hparams_string` are separate becouse BigQuery does not support `COALESCE` function within `PIVOT` statement.

## Final Query

The final query joins the main table (`project_id.dataset_id.table_id`) with both `hparams_float` and `hparams_string` CTEs using `model_name`.

```sql
SELECT hparams_float.*, hparams_string.*
FROM `project_id.dataset_id.table_id` 
LEFT JOIN hparams_string USING(model_name)
LEFT JOIN hparams_float USING(model_name)
```

By running this query, you will have a single table that includes all the pivoted columns from both the `hparams_float` and `hparams_string` CTEs, joined on the `model_name`.

This structure makes it significantly easier to filter, sort, and analyze models based on their hyperparameters.