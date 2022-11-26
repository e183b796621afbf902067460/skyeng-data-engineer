from head.db.reader.client import DBReaderClient
from head.db.writer.client import DBWriterClient

from src.conf.engine import db_engine


reader = DBReaderClient().setEngine(engine=db_engine)
writer = DBWriterClient().setEngine(engine=db_engine)
