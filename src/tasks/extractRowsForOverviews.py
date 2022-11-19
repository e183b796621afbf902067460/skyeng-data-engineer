from typing import List
from airflow.decorators import task


@task()
def extractRowsForOverviews(
        protocolCategory: str,
        overviewType: str,
        exposureTypes: list
) -> List[tuple]:
    import jinja2
    from src.conf.clients import reader
    from src.queries.selects.conf import conf

    j: jinja2.Environment = jinja2.Environment(loader=jinja2.BaseLoader())

    params: dict = {
        'h_protocol_category_name': protocolCategory
    }
    q: str = conf[protocolCategory]['types'][overviewType]['query']
    template = j.from_string(q)
    query = template.render(params)

    rows = reader.execute(query=query)

    if overviewType.lower() in exposureTypes:
        config: list = [(row.l_address_protocol_category_chain_id, row.pooladdress, row.walletaddress, row.h_protocol_name, row.h_network_name) for row in rows]
    else:
        config: list = [(row.l_address_protocol_category_chain_id, row.h_address, row.h_protocol_name, row.h_network_name) for row in rows]

    return config
