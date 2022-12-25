SELECT
    h_addresses0.h_address as pool_address,
    h_chains.h_network_name,
    h_protocols.h_protocol_name,
    h_protocols_categories.h_protocol_category_name,
    h_addresses1.h_address as wallet_address,
    h_labels.h_label_name,
    l_addresses_chains0.l_address_chain_name
FROM
{% if params['overview_type'] in ['allocation', 'borrow', 'incentive'] %}
    s_addresses_protocols_categories_labels_chains
LEFT JOIN
    l_addresses_protocols_categories_chains USING(l_address_protocol_category_chain_id)
{% else %}
    l_addresses_protocols_categories_chains
{% endif %}
LEFT JOIN
    l_protocols_categories_chains USING(l_protocol_category_chain_id)
LEFT JOIN
    l_protocols_categories USING(l_protocol_category_id)
LEFT JOIN
    h_protocols USING(h_protocol_id)
LEFT JOIN
    h_protocols_categories USING(h_protocol_category_id)
LEFT JOIN
    l_addresses_labels_chains USING(l_address_label_chain_id)
LEFT JOIN
    h_labels USING(h_label_id)
LEFT JOIN
    l_addresses_chains AS l_addresses_chains0 ON l_addresses_protocols_categories_chains.l_address_chain_id = l_addresses_chains0.l_address_chain_id
LEFT JOIN
    h_addresses AS h_addresses0 ON l_addresses_chains0.h_address_id = h_addresses0.h_address_id
LEFT JOIN
    l_addresses_chains AS l_addresses_chains1 ON l_addresses_labels_chains.l_address_chain_id = l_addresses_chains1.l_address_chain_id
LEFT JOIN
    h_addresses AS h_addresses1 ON l_addresses_chains1.h_address_id = h_addresses1.h_address_id
LEFT JOIN
    h_chains ON l_addresses_chains0.h_chain_id = h_chains.h_chain_id
WHERE
    h_protocols_categories.h_protocol_category_name = '{{ params["protocol_category"] }}'
