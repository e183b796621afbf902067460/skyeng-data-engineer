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
        'fernet',
        'df_serializer',
        'w3sleep'
    },
    description='get_overview() for hedge_to_supplies'
)
def get_overview(context, configs: dict) -> List[list]:
    def _formatting(samples: List[dict], cfg: dict) -> pd.DataFrame:
        for sample in samples: sample.update(
            {
                'wallet_address': cfg['wallet_address'],
                'label_name': cfg['label_name'],
                'protocol_name': cfg['protocol_name'],
                'token_address': cfg['token_address'],
                'network_name': cfg['network_name']
            }
        )
        context.resources.logger.info(f"Current overview: {samples}")
        df = pd.DataFrame(samples)
        df.rename(
            columns={
                'wallet_address': 'h_wallet_address',
                'label_name': 'h_label_name',
                'protocol_name': 'h_protocol_name',
                'token_address': 'h_token_address',
                'network_name': 'h_network_name',
                'symbol': 'pit_symbol',
                'price': 'pit_price',
                'qty': 'pit_qty'
            },
            inplace=True
        )
        return df
    while True:
        try:
            provider = HTTPProvider(uri=context.resources.fernet.decrypt(configs['network_rpc_node'].encode()).decode())
            class_ = D3BridgeConfigurator(
                abstract=d3Abstract,
                fabric_name='hedge_to_supplies',
                handler_name=configs['protocol_name']
            ).produce_handler()
            handler = class_(
                address=configs['token_address'],
                provider=provider,
                chain=configs['network_name'],
                trader=rootTrad3r
            )
            overview: List[dict] = handler.get_overview(address=configs['wallet_address'])
        except ValueError:
            context.resources.w3sleep.sleep()
        else:
            break
    df = _formatting(samples=overview, cfg=configs)
    return context.resources.df_serializer.df_to_list(df)

