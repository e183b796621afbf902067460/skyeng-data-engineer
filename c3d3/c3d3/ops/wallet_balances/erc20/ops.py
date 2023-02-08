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
        'fabric': 'wallet_balances_erc20'
    },
    out=DynamicOut(dict)
)
def extract_from_d3vault(context) -> List[dict]:
    query = '''
        SELECT
            h_addresses0.h_address as wallet_address,
            h_addresses1.h_address as token_address,
            h_chains.h_network_name,
            h_chains.h_network_rpc_node,
            h_labels.h_label_name
        FROM
            l_tokens_on_wallets
        LEFT JOIN
            l_addresses_chains_labels USING(l_address_chain_label_id)
        LEFT JOIN
            h_labels USING(h_label_id)
        LEFT JOIN
            l_addresses_chains AS l_addresses_chains0 ON l_addresses_chains_labels.l_address_chain_id = l_addresses_chains0.l_address_chain_id
        LEFT JOIN
            h_addresses as h_addresses0 ON l_addresses_chains0.h_address_id = h_addresses0.h_address_id
        LEFT JOIN
            l_addresses_chains AS l_addresses_chains1 ON l_tokens_on_wallets.l_address_chain_id = l_addresses_chains1.l_address_chain_id
        LEFT JOIN
            h_addresses as h_addresses1 ON l_addresses_chains1.h_address_id = h_addresses1.h_address_id
        LEFT JOIN
            h_chains ON l_addresses_chains0.h_chain_id = h_chains.h_chain_id
    '''
    context.resources.logger.info(f"{query}")

    samples = context.resources.d3vault.read(query=query)
    for sample in samples:
        wallet_address, token_address, label_name = sample[0], sample[1], sample[4]
        network_name, network_rpc_node = sample[2], sample[3]
        yield DynamicOutput(
            {
                'wallet_address': wallet_address,
                'token_address': token_address,
                'network_name': network_name,
                'network_rpc_node': network_rpc_node,
                'label_name': label_name
            },
            mapping_key=f'subtask_for_{wallet_address}_{token_address}_{network_name}'
        )


@op(
    name='load_to_dwh',
    required_resource_keys={
        'dwh',
        'logger',
        'df_serializer'
    },
    tags={
        'fabric': 'wallet_balances_erc20'
    }
)
def load_to_dwh(context, df: List[list]) -> None:
    now = datetime.utcnow()
    for mini_df in df:
        mini_df = context.resources.df_serializer.df_from_list(mini_df)
        mini_df['pit_ts'] = now
        context.resources.logger.info(mini_df.head())
