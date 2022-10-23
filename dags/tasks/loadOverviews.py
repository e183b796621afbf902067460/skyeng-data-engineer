from typing import List, Dict, Any
from airflow.decorators import task


@task()
def loadOverviews(overviews: Dict[int, List[Dict[str, Any]]], protocolCategory: str) -> None:
    from conf.clients import writer

    queries: dict = {
        'DEX': {
            'query': '''
                INSERT INTO {} (
                    l_address_protocol_category_chain_id,
                    pit_token_symbol,
                    pit_token_reserve,
                    pit_token_price
                ) VALUES (
                    {}, '{}', {}, {}
                )
                '''
        },
        'Staking': {
            'query': '''
                INSERT INTO {} (
                    l_address_protocol_category_chain_id,
                    pit_token_symbol,
                    pit_token_reserve,
                    pit_token_price
                ) VALUES (
                    {}, '{}', {}, {}
                )
                '''
        },
        'Lending': {
            'query': '''
                INSERT INTO {} (
                    l_address_protocol_category_chain_id,
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

    table: str = 'pit_' + protocolCategory.lower() + '_pool_overview'
    for i, overview in overviews.items():
        for aOverview in overview:
            if protocolCategory in ['DEX', 'Staking']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['reserve'], aOverview['price']
                ]
            elif protocolCategory in ['Lending']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['reserve'], aOverview['borrow'], aOverview['price'],
                    aOverview['depositAPY'], aOverview['borrowAPY']
                ]
            else:
                values: list = list()

            query = queries[protocolCategory]['query'].format(*values)
            writer.execute(query=query)
