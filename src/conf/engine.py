import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Uncomment after update
# FUND_MICROSERVICE_URI = PostgresHook(postgres_conn_id='FUND_MICROSERVICE_CONN').get_uri()
# POOL_MICROSERVICE_URI = PostgresHook(postgres_conn_id='POOL_MICROSERVICE_CONN').get_uri()
# ALLOCATION_MICROSERVICE_URI = PostgresHook(postgres_conn_id='ALLOCATION_MICROSERVICE_CONN').get_uri()

db_address = os.getenv('DB_ADDRESS', '')
db_user = os.getenv('DB_USER', '')
db_password = quote_plus(os.getenv('DB_PASSWORD', ''))
db_name = os.getenv('DB_NAME', '')

db_url = f'postgresql://{db_user}:{db_password}@{db_address}/{db_name}'
db_engine = create_engine(db_url)
