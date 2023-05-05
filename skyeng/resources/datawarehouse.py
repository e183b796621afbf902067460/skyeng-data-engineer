import os
from urllib.parse import quote_plus

from resources.datasource import PgDataSourceResource


class PgDataWarehouseResource(PgDataSourceResource):

    DB_ADDRESS = os.getenv('PG_DATAWAREHOUSE_HOST', None)
    DB_PORT = os.getenv('PG_DATAWAREHOUSE_PORT', None)
    DB_USER = os.getenv('PG_DATAWAREHOUSE_USER', None)
    DB_PASSWORD = quote_plus(os.getenv('PG_DATAWAREHOUSE_PASSWORD', None))
    DB_NAME = os.getenv('PG_DATAWAREHOUSE_DB', None)
