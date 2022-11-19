from typing import List, Dict, Any
from airflow.decorators import task
import re


@task()
def loadOverviews(
        overviews: Dict[int, List[Dict[str, Any]]],
        protocolCategory: str,
        overviewType: str,
        fabricKey: str
) -> None:
    import jinja2
    from src.conf.clients import writer
    from src.queries.inserts.conf import conf

    j: jinja2.Environment = jinja2.Environment()

    table: str = f'pit_{re.sub("-", "_", fabricKey)}'

    for i, overview in overviews.items():
        for aOverview in overview:
            if overviewType in ['incentive', 'allocation']:
                params: dict = {
                    'table': table,
                    'l_address_protocol_category_label_chain_id': int(i),
                    'pit_token_symbol': aOverview['symbol'],
                    'pit_token_amount': aOverview['amount'],
                    'pit_token_price': aOverview['price']
                }
            elif overviewType in ['pool'] and protocolCategory in ['DEX', 'Farming', 'Staking']:
                params: dict = {
                    'table': table,
                    'l_address_protocol_category_chain_id': int(i),
                    'pit_token_symbol': aOverview['symbol'],
                    'pit_token_reserve': aOverview['reserve'],
                    'pit_token_price': aOverview['price']
                }
            elif overviewType in ['pool'] and protocolCategory in ['Lending']:
                params: dict = {
                    'table': table,
                    'l_address_protocol_category_chain_id': int(i),
                    'pit_token_symbol': aOverview['symbol'],
                    'pit_token_reserve_size': aOverview['reserve'],
                    'pit_token_borrow_size': aOverview['borrow'],
                    'pit_token_price': aOverview['price'],
                    'pit_token_deposit_apy': aOverview['depositAPY'],
                    'pit_token_borrow_apy': aOverview['borrowAPY']
                }
            elif overviewType in ['borrow']:
                params: dict = {
                    'table': table,
                    'l_address_protocol_category_label_chain_id': int(i),
                    'pit_token_symbol': aOverview['symbol'],
                    'pit_token_amount': aOverview['amount'],
                    'pit_token_price': aOverview['price'],
                    'pit_health_factor': aOverview['healthFactor']
                }
            else:
                params: dict = dict()

            q: str = conf[protocolCategory]['types'][overviewType]['query']
            template = j.from_string(q)
            query = template.render(params)

            writer.execute(query=query)
