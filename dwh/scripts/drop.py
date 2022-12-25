from dwh.cfg.engine import DWHSettings

from sqlalchemy_utils import database_exists, drop_database
from clickhouse_sqlalchemy.exceptions import DatabaseException


if __name__ == '__main__':
    ENGINE = DWHSettings.get_engine()
    URI = DWHSettings.get_uri()

    try:
        if database_exists(URI):
            drop_database(URI)
    except DatabaseException:
        ...