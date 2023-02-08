from dagster import Definitions, AssetsDefinition

from c3d3.assets.hedge_to_supplies.assets import get_overview
from c3d3.ops.hedge_to_supplies.ops import extract_from_d3vault, load_to_dwh
from c3d3.jobs.hedge_to_supplies.jobs import dag
from c3d3.schedules.hedge_to_supplies.schedules import every_minute
from c3d3.resources.d3vault.resource import d3vault
from c3d3.resources.logger.resource import logger
from c3d3.resources.dwh.resource import dwh
from c3d3.resources.fernet.resource import fernet
from c3d3.resources.serializers.resource import df_serializer
from c3d3.resources.w3sleep.resource import w3sleep


extract_from_d3vault = AssetsDefinition.from_op(extract_from_d3vault)
load_to_dwh = AssetsDefinition.from_op(load_to_dwh)


hedge_to_supplies = Definitions(
    assets=[extract_from_d3vault, get_overview, load_to_dwh],
    jobs=[dag],
    resources={
        'd3vault': d3vault,
        'dwh': dwh,
        'logger': logger,
        'fernet': fernet,
        'df_serializer': df_serializer,
        'w3sleep': w3sleep
    },
    schedules=[every_minute]
)
