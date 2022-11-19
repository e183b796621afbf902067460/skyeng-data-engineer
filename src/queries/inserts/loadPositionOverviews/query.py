import jinja2


q0: str = '''
    INSERT INTO {{ table }} (
        l_address_protocol_category_label_chain_id,
        pit_token_symbol,
        pit_token_amount,
        pit_token_price
    ) VALUES (
        {{ l_address_protocol_category_label_chain_id }}, 
        '{{ pit_token_symbol }}', 
        {{ pit_token_amount }}, 
        {{ pit_token_price }}
    )
'''

q1: str = '''
    INSERT INTO {{ table }} (
        l_address_protocol_category_label_chain_id,
        pit_token_symbol,
        pit_token_amount,
        pit_token_price,
        pit_health_factor
    ) VALUES (
        {{ l_address_protocol_category_label_chain_id }}, 
        '{{ pit_token_symbol }}', 
        {{ pit_token_amount }}, 
        {{ pit_token_price }}, 
        {{ pit_health_factor }}
    )
'''