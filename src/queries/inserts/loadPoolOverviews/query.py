import jinja2


q0: str = '''
    INSERT INTO {{ table }} (
        l_address_protocol_category_chain_id,
        pit_token_symbol,
        pit_token_reserve,
        pit_token_price
    ) VALUES (
        {{ l_address_protocol_category_chain_id }}, 
        '{{ pit_token_symbol }}', 
        {{ pit_token_reserve }}, 
        {{ pit_token_price }}
    )
'''

q1: str = '''
    INSERT INTO {{ table }} (
        l_address_protocol_category_chain_id,
        pit_token_symbol,
        pit_token_reserve_size,
        pit_token_borrow_size,
        pit_token_price,
        pit_token_deposit_apy,
        pit_token_borrow_apy
    ) VALUES (
        {{ l_address_protocol_category_chain_id }}, 
        '{{ pit_token_symbol }}', 
        {{ pit_token_reserve_size }}, 
        {{ pit_token_borrow_size }}, 
        {{ pit_token_price }}, 
        {{ pit_token_deposit_apy }}, 
        {{ pit_token_borrow_apy }}
    )
'''