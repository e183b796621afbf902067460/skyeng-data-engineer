

exposure: str = '''
        SELECT
            l_addresses_protocols_categories_chains.l_address_protocol_category_chain_id,
            h_addresses0.h_address as poolAddress,
            h_addresses1.h_address as walletAddress,
            h_protocols.h_protocol_name,
            h_chains.h_network_name
        FROM l_addresses_protocols_categories_labels_chains
        LEFT JOIN l_addresses_protocols_categories_chains USING(l_address_protocol_category_chain_id)
        LEFT JOIN l_protocols_categories_chains USING(l_protocol_category_chain_id)
        LEFT JOIN l_protocols_categories USING(l_protocol_category_id)
        LEFT JOIN h_protocols USING(h_protocol_id)
        LEFT JOIN h_protocols_categories USING(h_protocol_category_id)
        LEFT JOIN h_chains USING(h_chain_id)
        LEFT JOIN l_addresses_labels_chains USING(l_address_label_chain_id)
        LEFT JOIN l_addresses_chains l_addresses_chains0 on l_addresses_protocols_categories_chains.l_address_chain_id = l_addresses_chains0.l_address_chain_id
        LEFT JOIN l_addresses_chains l_addresses_chains1 on l_addresses_labels_chains.l_address_chain_id = l_addresses_chains1.l_address_chain_id
        LEFT JOIN h_addresses h_addresses0 on l_addresses_chains0.h_address_id = h_addresses0.h_address_id
        LEFT JOIN h_addresses h_addresses1 on l_addresses_chains1.h_address_id = h_addresses1.h_address_id
        WHERE
            h_protocols_categories.h_protocol_category_name = '{}'
        '''

notExposure: str = '''
        SELECT
            l_addresses_protocols_categories_chains.l_address_protocol_category_chain_id,
            h_addresses.h_address,
            h_protocols.h_protocol_name,
            h_chains.h_network_name
        FROM l_addresses_protocols_categories_chains
        LEFT JOIN l_protocols_categories_chains USING(l_protocol_category_chain_id)
        LEFT JOIN l_protocols_categories USING(l_protocol_category_id)
        LEFT JOIN h_protocols USING(h_protocol_id)
        LEFT JOIN h_protocols_categories USING(h_protocol_category_id)
        LEFT JOIN l_addresses_chains USING(l_address_chain_id)
        LEFT JOIN h_chains ON l_addresses_chains.h_chain_id = h_chains.h_chain_id
        LEFT JOIN h_addresses USING(h_address_id)
        WHERE
            h_protocols_categories.h_protocol_category_name = '{}'
        '''


queries: dict = {
    'DEX': {
        'types': {
            'allocation': {
                'query': exposure
            },
            'pool': {
                'query': notExposure
            }
        }
    },
    'Farming': {
        'types': {
            'allocation': {
                'query': exposure
            },
            'incentive': {
                'query': exposure
            },
            'pool': {
                'query': notExposure
            }
        }
    },
    'Staking': {
        'types': {
            'allocation': {
                'query': exposure
            },
            'incentive': {
                'query': exposure
            },
            'pool': {
                'query': notExposure
            }
        }
    },
    'Lending': {
        'types': {
            'allocation': {
                'query': exposure
            },
            'borrow': {
                'query': exposure
            },
            'incentive': {
                'query': exposure
            },
            'pool': {
                'query': notExposure
            }
        }
    }
}

