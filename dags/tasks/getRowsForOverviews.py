from typing import List
from airflow.decorators import task


@task()
def getRowsForOverviews(
        protocolCategory: str,
        overviewType: str
) -> List[tuple]:
    from conf.clients import reader
    from queries.get import queries

    isExposure: bool = 'allocation' == overviewType.lower() or 'borrow' == overviewType.lower() or 'incentive' == overviewType.lower()

    query: str = queries[protocolCategory]['types'][overviewType]['query'].format(protocolCategory)
    rows = reader.execute(query=query)

    if isExposure:
        config: list = [(row.l_address_protocol_category_chain_id, row.pooladdress, row.walletaddress, row.h_protocol_name, row.h_network_name) for row in rows]
    else:
        config: list = [(row.l_address_protocol_category_chain_id, row.h_address, row.h_protocol_name, row.h_network_name) for row in rows]

    return config
