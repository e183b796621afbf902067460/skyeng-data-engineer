from typing import List
from dagster import asset

from raffaelo.providers.http.provider import HTTPProvider
from d3tl.abstract.fabric import d3Abstract
from d3tl.bridge.configurator import D3BridgeConfigurator
from trad3r.root.composite.trader import rootTrad3r


@asset(
    required_resource_keys={
        'logger'
    }
)
def get_overviews(context, get_cfgs: List[dict]) -> List[List[dict]]:
    overviews = list()
    for cfg in get_cfgs:
        provider = HTTPProvider(uri=cfg['h_network_rpc_node'])

        class_ = D3BridgeConfigurator(
            abstract=d3Abstract,
            fabric_name='wallet_balances',
            handler_name='erc20'
        ).produce_handler()

        handler = class_(
            address=cfg['h_erc20_token_address'],
            provider=provider,
            trader=rootTrad3r
        )
        overview = handler.get_overview(address=cfg['h_wallet_address'])
        context.resources.logger.info(f"Current overview for wallet ({cfg['h_wallet_address']}) and token ({cfg['h_erc20_token_address']}): {overview} — {cfg['h_network_name']}")
        overviews.append(overview)
    return overviews

