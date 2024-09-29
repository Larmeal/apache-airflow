SELECT
    *
FROM `{{ params.project_id }}.dataset.table`
WHERE
    date = @start_interval