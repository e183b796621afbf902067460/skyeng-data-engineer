from dagster import Definitions, AssetsDefinition

from c3d3.assets.wallet_balances.gas.assets import get_overview
from c3d3.ops.wallet_balances.gas.ops import extract_from_d3vault, load_to_dwh
from c3d3.jobs.wallet_balances.gas.jobs import dag
from c3d3.schedules.wallet_balances.gas.schedules import every_minute
from c3d3.resources.d3vault.resource import d3vault
from c3d3.resources.logger.resource import logger
from c3d3.resources.dwh.resource import dwh
from c3d3.resources.fernet.resource import fernet
from c3d3.resources.serializers.resource import df_serializer


extract_from_d3vault = AssetsDefinition.from_op(extract_from_d3vault)
load_to_dwh = AssetsDefinition.from_op(load_to_dwh)


wallet_balances_gas = Definitions(
    assets=[extract_from_d3vault, get_overview, load_to_dwh],
    jobs=[dag],
    resources={
        'd3vault': d3vault,
        'dwh': dwh,
        'logger': logger,
        'fernet': fernet,
        'df_serializer': df_serializer
    },
    schedules=[every_minute]
)
