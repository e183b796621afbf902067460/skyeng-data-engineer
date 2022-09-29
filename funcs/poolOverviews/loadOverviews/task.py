from typing import List, Dict, Any
from airflow.decorators import task


@task()
def loadOverviews(overviews: Dict[int, List[Dict[str, Any]]], overviewType: str) -> None:
    from cfg.clients import writer

    queries: dict = {
        'liquidity-pool-overview': {
            'query': '''
                INSERT INTO {} (
                    l_address_protocol_chain_id,
                    pit_token_symbol,
                    pit_token_reserve,
                    pit_token_price
                ) VALUES (
                    {}, '{}', {}, {}
                )
                '''
        },
        'staking-pool-overview': {
            'query': '''
                INSERT INTO {} (
                    l_address_protocol_chain_id,
                    pit_token_symbol,
                    pit_token_reserve,
                    pit_token_price
                ) VALUES (
                    {}, '{}', {}, {}
                )
                '''
        },
        'lending-pool-overview': {
            'query': '''
                INSERT INTO {} (
                    l_address_protocol_chain_id,
                    pit_token_symbol,
                    pit_token_reserve_size,
                    pit_token_borrow_size,
                    pit_token_price,
                    pit_token_deposit_apy,
                    pit_token_borrow_apy
                ) VALUES (
                    {}, '{}', {}, {}, {}, {}, {}
                )
                '''
        }
    }

    table: str = 'pit_' + overviewType.replace('-', '_')
    for i, overview in overviews.items():
        for aOverview in overview:
            if overviewType in ['liquidity-pool-overview', 'staking-pool-overview']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['reserve'], aOverview['price']
                ]
            elif overviewType in ['lending-pool-overview']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['reserve'], aOverview['borrow'], aOverview['price'],
                    aOverview['depositAPY'], aOverview['borrowAPY']
                ]

            query = queries[overviewType]['query'].format(*values)
            writer.execute(query=query)
