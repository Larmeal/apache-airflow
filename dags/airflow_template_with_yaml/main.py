import dagfactory

config_file = "/opt/airflow/dags/airflow_template_with_yaml/medium_demo_bigquery.yaml"
test = dagfactory.DagFactory(config_file)

# Create task dependencies
test.clean_dags(globals())
test.generate_dags(globals())
