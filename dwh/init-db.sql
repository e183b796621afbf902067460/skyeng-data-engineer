CREATE TABLE IF NOT EXISTS defi_management.bigtable_defi_management
(
    bigtable_defi_management_uuid UUID DEFAULT generateUUIDv4(),

    h_pool_address String,
    h_wallet_address String,
    h_network_name String,
    h_protocol_name String,
    h_pool_name String,
    h_label_name String,
    h_protocol_category String,

    pit_token_symbol Nullable(String),
    pit_token_qty Nullable(Float32),
    pit_token_price Nullable(Float32),
    pit_health_factor Nullable(Float32),
    pit_token_reserve_size Nullable(Float32),
    pit_token_borrow_size Nullable(Float32),
    pit_token_deposit_apy Nullable(Float32),
    pit_token_borrow_apy Nullable(Float32),

    s_overview_type String,

    bigtable_defi_management_load_ts DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY bigtable_defi_management_uuid
SETTINGS index_granularity = 8192;