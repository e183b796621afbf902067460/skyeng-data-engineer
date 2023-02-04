from dagster import Definitions, AssetsDefinition

from c3d3.assets.wallet_balances.erc20.assets import get_overviews
from c3d3.ops.wallet_balances.erc20.ops import get_cfgs, load
from c3d3.jobs.wallet_balances.erc20.jobs import dag
from c3d3.schedules.wallet_balances.erc20.schedules import every_10th_minute
from c3d3.resources.d3vault.resource import d3vault
from c3d3.resources.logger.resource import logger
from c3d3.resources.dwh.resource import dwh


get_cfgs = AssetsDefinition.from_op(get_cfgs)
load = AssetsDefinition.from_op(load)


wallet_balances_erc20 = Definitions(
    assets=[get_cfgs, get_overviews, load],
    jobs=[dag],
    resources={
        'd3vault': d3vault,
        'dwh': dwh,
        'logger': logger
    },
    schedules=[every_10th_minute]
)
