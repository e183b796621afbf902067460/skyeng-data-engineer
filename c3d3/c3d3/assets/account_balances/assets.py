from typing import List
import requests
from dagster import asset
import pandas as pd

from c3tl.abstract.fabric import c3Abstract
from c3tl.bridge.configurator import C3BridgeConfigurator
from trad3r.root.composite.trader import rootTrad3r


@asset(
    name='df',
    required_resource_keys={
        'logger',
        'fernet',
        'df_serializer',
        'w3sleep'
    },
    description='get_overview() for account_balances'
)
def get_overview(context, configs: dict) -> List[list]:
    def _formatting(samples: List[dict], cfg: dict) -> pd.DataFrame:
        for sample in samples: sample.update(
            {
                'label_name': cfg['label_name'],
                'exchange_name': cfg['exchange_name'],
                'symbol_name': cfg['symbol_name'],

            }
        )
        context.resources.logger.info(f"Current overview: {samples}")
        df = pd.DataFrame(samples)
        df.rename(
            columns={
                'label_name': 'h_label_name',
                'exchange_name': 'h_exchange_name',
                'symbol_name': 'h_symbol_name',
                'qty': 'pit_qty',
                'current_price': 'pit_current_price'
            },
            inplace=True
        )
        return df
    while True:
        try:
            class_ = C3BridgeConfigurator(
                abstract=c3Abstract,
                fabric_name='account_balances',
                handler_name=configs['exchange_name']
            ).produce_handler()
            handler = class_(
                api=context.resources.fernet.decrypt(configs['label_api_key'].encode()).decode(),
                secret=context.resources.fernet.decrypt(configs['label_secret_key'].encode()).decode(),
                trader=rootTrad3r
            )
            overview: List[dict] = handler.get_overview(ticker=configs['symbol_name'])
        except requests.exceptions.ConnectionError:
            context.resources.w3sleep.sleep()
        except requests.exceptions.HTTPError:
            context.resources.w3sleep.sleep()
        else:
            break
    df = _formatting(samples=overview, cfg=configs)
    return context.resources.df_serializer.df_to_list(df)

