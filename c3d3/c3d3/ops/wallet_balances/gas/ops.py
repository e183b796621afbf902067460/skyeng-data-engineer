from typing import List
from datetime import datetime
from dagster import op, DynamicOut, DynamicOutput


@op(
    name='configs',
    required_resource_keys={
        'd3vault',
        'logger'
    },
    tags={
        'fabric': 'wallet_balances_gas'
    },
    out=DynamicOut(dict)
)
def extract_from_d3vault(context) -> List[dict]:
    query = '''
        SELECT
            h_addresses.h_address,
            h_labels.h_label_name,
            h_chains.h_network_name,
            h_chains.h_network_rpc_node,
            h_chains.h_native_chain_token
        FROM
            l_addresses_chains_labels
        LEFT JOIN
            h_labels USING(h_label_id)
        LEFT JOIN
            l_addresses_chains USING(l_address_chain_id)
        LEFT JOIN
            h_chains USING(h_chain_id)
        LEFT JOIN
            h_addresses USING(h_address_id)
    '''
    context.resources.logger.info(f"{query}")

    samples = context.resources.d3vault.read(query=query)
    for sample in samples:
        wallet_address, label_name = sample[0], sample[1]
        network_name, network_rpc_node, native_chain_token = sample[2], sample[3], sample[4]
        yield DynamicOutput(
            {
                'wallet_address': wallet_address,
                'label_name': label_name,
                'network_name': network_name,
                'network_rpc_node': network_rpc_node,
                'native_chain_token': native_chain_token,
            },
            mapping_key=f'subtask_for_{wallet_address}_{network_name}'
        )


@op(
    name='load_to_dwh',
    required_resource_keys={
        'dwh',
        'logger',
        'df_serializer'
    },
    tags={
        'fabric': 'wallet_balances_gas'
    }
)
def load_to_dwh(context, df: List[list]) -> None:
    now = datetime.utcnow()
    for mini_df in df:
        mini_df = context.resources.df_serializer.df_from_list(mini_df)
        mini_df['pit_ts'] = now
        context.resources.logger.info(mini_df.head())
