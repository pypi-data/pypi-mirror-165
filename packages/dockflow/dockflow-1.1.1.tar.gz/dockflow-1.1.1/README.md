# Dockflow CLI
This package requires docker to be installed and running on your machine.
## Getting started

1. Install dockflow:  
   `pip install dockflow`

2. Authenticate docker to pull from private GCR repository:  
   2.1. First make sure that your `gcloud` is authenticated.  
   2.2. Ensure you are in the correct project using `gcloud config set project <project name>`  
   2.3. Use `gcloud auth configure-docker` to auth docker to pull from private container repo.  

## Quickstart
1. Ensure that your docker file sharing settings allows access to your development directory.
2. Navigate to the root directory of your ```dags``` folder.
3. Use `dockflow config` and enter your container repo url excluding the version.
    - This will save the url in a config file.
    - Eg. `eu.gcr.io/<project>/<container>`
    - This should only be used if the container repo changes.
4. If the image version tag is not `composer-1.11.2-airflow-1.10.9` specify the tag using `dockflow start -iv <version>`
5. Use `dockflow start` (This will mount the dag folder and start Airflow).
6. Use the UI to add connections.
    - Admin -> Connections -> Create
7. Use `dockflow refresh` to refresh the configs cache or to bundle configs.
8. Remember to use `dockflow stop` to shut down the instance to save local machine resources.
    - The state will be persisted in the same directory as the `dags` folder.
9. To stop and remove the container use `dockflow stop --rm`

## Available composer versions

- composer-1.11.2-airflow-1.10.9 (default)
- composer-1.10.6-airflow-1.10.6 (No longer being updated)

## CloudSQL Proxy

```
docker run -d \
  -v <PATH_TO_KEY_FILE>:/config \
  -p 127.0.0.1:5432:5432 \
  --network='dockflow' \
  --name='cloudsql' \
  gcr.io/cloudsql-docker/gce-proxy:1.17 /cloud_sql_proxy \
  -instances=<INSTANCE_CONNECTION_NAME>=tcp:0.0.0.0:5432 -credential_file=/config
```