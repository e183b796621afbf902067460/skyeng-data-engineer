from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

import os
from urllib.parse import quote_plus


class PgDataSourceResource:

    DB_ADDRESS = os.getenv('PG_DATASOURCE_HOST', None)
    DB_PORT = os.getenv('PG_DATASOURCE_PORT', None)
    DB_USER = os.getenv('PG_DATASOURCE_USER', None)
    DB_PASSWORD = quote_plus(os.getenv('PG_DATASOURCE_PASSWORD', None))
    DB_NAME = os.getenv('PG_DATASOURCE_DB', None)

    DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'

    def _db_uri(self) -> str:
        return self.DB_URL

    def get_engine(self) -> Engine:
        return create_engine(self._db_uri())


def pg_datasource():
    return PgDataSourceResource()
