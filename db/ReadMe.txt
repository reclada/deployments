Run install.sh [rm_schema]
Use rm_schema optional argument to remove all reclada schemas before DB install.

environment variables:
    DB_URI      - connection string for psql
        format: "postgresql://[user_name]:[password]@[host(server_name)]:[port(default: 5432)]/[db_name]"
    LAMBDA_NAME - s3_create_datasource_in_db lambda name
    CUSTOM_REPO_PATH - 
    ENVIRONMENT_NAME - the name of the environment where is works (K8S or DOMINO)