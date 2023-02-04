from typing import List
from dagster import op


@op(
    required_resource_keys={
        'd3vault',
        'logger'
    }
)
def get_cfgs(context) -> List[dict]:
    data = [
        {
            'h_wallet_address': '0xe771d0daf2062aaaa09ddd93e0171d572fc09e66',
            'h_label_name': 'MATIC_ROBOT',
            'h_erc20_token_address': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
            'h_network_name': 'polygon',
            'h_network_rpc_node': 'https://rpc.ankr.com/polygon'
        }
    ]
    context.resources.logger.info(f"Current data: {data}")
    return data


@op(
    required_resource_keys={
        'dwh',
        'logger'
    }
)
def load(context, get_overviews: List[List[dict]]) -> None:
    for overview in get_overviews:
        context.resources.logger.info(f"Current overview: {overview}")
