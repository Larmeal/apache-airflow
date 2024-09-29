# Apache Airflow with YAML File
The repository was created to experiment with hosting Airflow on your own using Docker. This repository is used for explanations on [Medium - สร้าง Airflow Pipeline ง่าย ๆ ผ่าน YAML ไฟล์ด้วย DAG Factory](https://medium.com/cj-express-tech-tildi/%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%87-airflow-pipeline-%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2-%E0%B9%86-%E0%B8%9C%E0%B9%88%E0%B8%B2%E0%B8%99-yaml-%E0%B9%84%E0%B8%9F%E0%B8%A5%E0%B9%8C%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-dag-factory-33dddefd67c4).

Before getting started, you need to install [Git](https://git-scm.com/downloads), [Docker](https://www.docker.com/), and [Docker Compose](https://docs.docker.com/compose/install/). You can check out this [Medium](https://medium.com/@chutdanai.tho/%E0%B9%80%E0%B8%A3%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%95%E0%B9%89%E0%B8%99%E0%B9%83%E0%B8%8A%E0%B9%89%E0%B8%87%E0%B8%B2%E0%B8%99-mongodb-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-pymongo-%E0%B9%81%E0%B8%9A%E0%B8%9A-step-by-step-d70f4d7c1b6e) post for the installation.

After you have completed all the installations, do the following:

1. Clone the git repository to your folder.
```shell
git init
git clone https://github.com/Larmeal/apache-airflow.git
```

2. Run the docker compose inside the repository
```shell
docker-compose up
```
or
```shell
docker compose up
```
3. After that, you can use Airflow as usual. If you want to make any adjustments, you can do so in the docker-compose YAML file. You can see an example at [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).