from orm.clients.reader.client import DBReaderClient
from orm.clients.writer.client import DBWriterClient

from cfg.engine import db_engine


reader = DBReaderClient().setEngine(engine=db_engine)
writer = DBWriterClient().setEngine(engine=db_engine)
