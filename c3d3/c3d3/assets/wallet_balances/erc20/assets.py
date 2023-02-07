from typing import List
from dagster import asset
import pandas as pd

from raffaelo.providers.http.provider import HTTPProvider
from d3tl.abstract.fabric import d3Abstract
from d3tl.bridge.configurator import D3BridgeConfigurator
from trad3r.root.composite.trader import rootTrad3r


@asset(
    name='df',
    required_resource_keys={
        'logger',
        'fernet'
    },
    description='get_overview() for wallet_balances_erc20'
)
def get_overview(context, configs: dict) -> List[list]:
    df = pd.DataFrame()

    provider = HTTPProvider(uri=context.resources.fernet.decrypt(configs['network_rpc_node'].encode()).decode())

    class_ = D3BridgeConfigurator(
        abstract=d3Abstract,
        fabric_name='wallet_balances',
        handler_name='erc20'
    ).produce_handler()

    handler = class_(
        address=configs['token_address'],
        provider=provider,
        trader=rootTrad3r
    )
    overview: List[dict] = handler.get_overview(address=configs['wallet_address'])
    for sample in overview: sample.update(
            {
                'wallet_address': configs['wallet_address'],
                'label_name': configs['label_name'],
                'token_address': configs['token_address'],
                'network_name': configs['network_name']
            }
        )

    context.resources.logger.info(f"Current overview: {overview}")
    df = df.append(pd.DataFrame(overview), ignore_index=True)
    df.rename(
        columns={
            'wallet_address': 'h_wallet_address',
            'label_name': 'h_label_name',
            'token_address': 'h_token_address',
            'network_name': 'h_network_name',
            'symbol': 'pit_symbol',
            'qty': 'pit_qty',
            'price': 'pit_price'
        },
        inplace=True
    )
    return [df.columns.values.tolist()] + df.values.tolist()

