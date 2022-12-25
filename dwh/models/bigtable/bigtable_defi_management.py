from sqlalchemy import Column, Text, Float, text
from sqlalchemy.sql import func
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types.common import Nullable, DateTime, UUID

from dwh.base.main import Base
from dwh.cfg.engine import DWHSettings


class BigTableDeFiManagement(Base):

    __tablename__ = 'bigtable_defi_management'
    __table_args__ = (
        engines.MergeTree(order_by=['bigtable_defi_management_uuid']),
        {'schema': DWHSettings.DB_NAME}
    )

    bigtable_defi_management_uuid = Column(UUID, primary_key=True, server_default=text("generateUUIDv4()"))

    h_pool_address = Column(Text)
    h_wallet_address = Column(Text)
    h_network_name = Column(Text)
    h_protocol_name = Column(Text)
    h_pool_name = Column(Text)
    h_label_name = Column(Text)
    h_protocol_category = Column(Text)

    pit_token_symbol = Column(Nullable(Text))
    pit_token_qty = Column(Nullable(Float))
    pit_token_price = Column(Nullable(Float))

    pit_health_factor = Column(Nullable(Float))
    pit_token_reserve_size = Column(Nullable(Float))
    pit_token_borrow_size = Column(Nullable(Float))

    pit_token_deposit_apy = Column(Nullable(Float))
    pit_token_borrow_apy = Column(Nullable(Float))

    s_overview_type = Column(Text)

    bigtable_defi_management_load_ts = Column(DateTime, server_default=func.now())
