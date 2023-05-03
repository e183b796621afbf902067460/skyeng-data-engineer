from dagster import resource

import os
from urllib.parse import quote_plus

from skyeng.resources.pg.resource import PgResource


class ChResource(PgResource):
    DB_ADDRESS = os.getenv('CH_HOST', '')
    DB_PORT = os.getenv('CH_PORT', '')
    DB_USER = os.getenv('CH_USER', '')
    DB_PASSWORD = quote_plus(os.getenv('CH_PASSWORD', ''))
    DB_NAME = os.getenv('CH_DB', '')

    DB_URL = f'clickhouse://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'


@resource
def ch(init_context) -> ChResource:
    return ChResource()
