from dagster import job

from c3d3.assets.wallet_balances.erc20.assets import get_overviews
from c3d3.ops.wallet_balances.erc20.ops import get_cfgs, load
from c3d3.resources.d3vault.resource import d3vault
from c3d3.resources.logger.resource import logger
from c3d3.resources.dwh.resource import dwh


@job(
    name='wallet_balances_erc20',
    resource_defs={
        'd3vault': d3vault,
        'dwh': dwh,
        'logger': logger
    }
)
def dag():
    load(get_overviews=get_overviews(get_cfgs=get_cfgs()))
