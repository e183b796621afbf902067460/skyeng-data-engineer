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
    from conf.clients import writer
    from queries.load import queries

    table: str = f'pit_{re.sub("-", "_", fabricKey)}'

    for i, overview in overviews.items():
        for aOverview in overview:
            if overviewType in ['incentive', 'allocation']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['amount'], aOverview['price']
                ]
            elif overviewType in ['pool'] and protocolCategory in ['DEX', 'Farming', 'Staking']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['reserve'], aOverview['price']
                ]
            elif overviewType in ['pool'] and protocolCategory in ['Lending']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['reserve'], aOverview['borrow'], aOverview['price'],
                    aOverview['depositAPY'], aOverview['borrowAPY']
                ]
            elif overviewType in ['borrow']:
                values: list = [
                    table, int(i), aOverview['symbol'], aOverview['amount'], aOverview['price'], aOverview['healthFactor']
                ]
            else:
                values: list = list()

            query = queries[protocolCategory]['types'][overviewType]['query'].format(*values)
            writer.execute(query=query)
