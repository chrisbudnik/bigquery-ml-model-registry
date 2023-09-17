-- BigQuery SQL: 
-- converting hyperparameters stored in an array into columns
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
),
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
SELECT hparams_float.*, hparams_string.*
FROM `project_id.dataset_id.table_id` 
LEFT JOIN hparams_string USING(model_name)
LEFT JOIN hparams_float USING(model_name)