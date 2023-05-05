import os
from urllib.parse import quote_plus

from resources.datasource import PgDataSourceResource


class ChDataWarehouseResource(PgDataSourceResource):

    DB_ADDRESS = os.getenv('CH_DATAMART_HOST', None)
    DB_PORT = os.getenv('CH_DATAMART_PORT', None)
    DB_USER = os.getenv('CH_DATAMART_USER', None)
    DB_PASSWORD = quote_plus(os.getenv('CH_DATAMART_PASSWORD', None))
    DB_NAME = os.getenv('CH_DATAMART_DB', None)

    DB_URL = f'clickhouse://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'
