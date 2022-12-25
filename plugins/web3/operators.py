from airflow.decorators import task


@task()
def Web3OverviewOperator(rows, fabric_key: str, overview_type: str):
    import logging
    import pandas as pd

    from head.bridge.configurator import BridgeConfigurator

    from overviews.abstracts.fabric import overviewAbstractFabric
    from providers.abstracts.fabric import providerAbstractFabric

    from traders.head.trader import headTrader

    web3_parallelize: list = list()
    for row in rows:
        pool, network, protocol, protocol_category, wallet, label, pool_name  = row[0], row[1], row[2], row[3], row[4], row[5], row[6]

        provider = BridgeConfigurator(
            abstractFabric=providerAbstractFabric,
            fabricKey='http',
            productKey=network
        ).produceProduct()

        handler = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey=f'{fabric_key.lower()}',
            productKey=protocol.lower()
        ).produceProduct()()\
            .setAddress(address=pool)\
            .setProvider(provider=provider)\
            .setTrader(trader=headTrader)\
            .create()
        logging.info(f'Current Overview for ({network})({protocol_category}){protocol} is {handler}: {handler.address}, label {label} ({wallet})')
        web3_parallelize.append(
            {
                'h_network_name': network,
                'h_protocol_category': protocol_category,
                'h_protocol_name': protocol,
                'h_pool_address': pool,
                'h_label_name': label,
                'h_wallet_address': wallet,
                'h_pool_name': pool_name,
                's_overview_type': overview_type,
                '_handler_parallelize': handler.getOverview(address=wallet)
            }
        )

    columns = ['h_network_name', 'h_protocol_category', 'h_protocol_name', 'h_pool_address', 'h_label_name', 'h_wallet_address', 'h_pool_name', 's_overview_type']
    df = pd.DataFrame(columns=columns)
    for web3_parallel in web3_parallelize:
        master_data = {
            'h_network_name': web3_parallel['h_network_name'],
            'h_protocol_category': web3_parallel['h_protocol_category'],
            'h_protocol_name': web3_parallel['h_protocol_name'],
            'h_pool_address': web3_parallel['h_pool_address'],
            'h_label_name': web3_parallel['h_label_name'],
            'h_wallet_address': web3_parallel['h_wallet_address'],
            'h_pool_name': web3_parallel['h_pool_name'],
            's_overview_type': web3_parallel['s_overview_type']
        }
        for web3_overview in web3_parallel['_handler_parallelize'].result():
            master_data.update(web3_overview)
            df = pd.concat(
                [df, pd.DataFrame([master_data])],
                ignore_index=True
            )
    return df.to_dict(orient='list')
