

poolOverview: str = '''
    INSERT INTO {} (
        l_address_protocol_category_chain_id,
        pit_token_symbol,
        pit_token_reserve,
        pit_token_price
    ) VALUES (
        {}, '{}', {}, {}
    )
'''

lendingPoolOverview: str = '''
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

exposureOverview: str = '''
    INSERT INTO {} (
        l_address_protocol_category_label_chain_id,
        pit_token_symbol,
        pit_token_amount,
        pit_token_price
    ) VALUES (
        {}, '{}', {}, {}
    )
'''

borrowOverview: str = '''
    INSERT INTO {} (
        l_address_protocol_category_label_chain_id,
        pit_token_symbol,
        pit_token_amount,
        pit_token_price,
        pit_health_factor
    ) VALUES (
        {}, '{}', {}, {}, {}
    )
'''


queries: dict = {
    'DEX': {
        'types': {
            'allocation': {
                'query': exposureOverview
            },
            'pool': {
                'query': poolOverview
            }
        }
    },
    'Farming': {
        'types': {
            'allocation': {
                'query': exposureOverview
            },
            'incentive': {
                'query': exposureOverview
            },
            'pool': {
                'query': poolOverview
            }
        }
    },
    'Staking': {
        'types': {
            'allocation': {
                'query': exposureOverview
            },
            'incentive': {
                'query': exposureOverview
            },
            'pool': {
                'query': poolOverview
            }
        }
    },
    'Lending': {
        'types': {
            'allocation': {
                'query': exposureOverview
            },
            'borrow': {
                'query': borrowOverview
            },
            'incentive': {
                'query': exposureOverview
            },
            'pool': {
                'query': lendingPoolOverview
            }
        }
    }
}

