import dagfactory

config_file = "/opt/airflow/dags/airflow_template_with_yaml/medium_demo_bigquery.yaml"
dag_factory = dagfactory.DagFactory(config_file)

# Create task dependencies
dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())
