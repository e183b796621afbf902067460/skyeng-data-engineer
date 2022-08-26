import pendulum
from airflow.decorators import dag, task


overviewType: str = 'liquidity-pool-overview'


@dag(
    schedule_interval='*/5 * * * *',
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False
)
def liquidityPoolOverview():

    @task()
    def getRows():
        import os
        from urllib.parse import quote_plus

        from sqlalchemy import create_engine

        db_address = os.getenv('DB_ADDRESS', '')
        db_user = os.getenv('DB_USER', '')
        db_password = quote_plus(os.getenv('DB_PASSWORD', ''))
        db_name = os.getenv('DB_NAME', '')

        db_url = f'postgresql://{db_user}:{db_password}@{db_address}/{db_name}'
        db_engine = create_engine(db_url)

        query = f'''
            SELECT
                l_addresses_protocols_chains.l_address_protocol_chain_id,
                h_addresses.h_address,
                h_protocols.h_protocol_name,
                h_chains.h_network_name
            FROM l_addresses_protocols_chains
            LEFT JOIN l_protocols_chains USING(l_protocol_chain_id)
            LEFT JOIN h_protocols USING(h_protocol_id)
            LEFT JOIN l_addresses_chains USING(l_address_chain_id)
            LEFT JOIN h_chains ON l_addresses_chains.h_chain_id = h_chains.h_chain_id
            LEFT JOIN h_addresses USING(h_address_id)
            WHERE
                l_addresses_protocols_chains.l_address_protocol_chain_prefix = '{overviewType}'
            '''

        rows = db_engine.execute(query).fetchall()
        return [(row.l_address_protocol_chain_id, row.h_address, row.h_protocol_name, row.h_network_name) for row in rows]

    @task()
    def getOverviews(rows):
        import logging

        from head.consts.chains.const import Chains
        from head.bridge.configurator import BridgeConfigurator

        from overviews.abstracts.fabric import overviewAbstractFabric
        from providers.abstracts.fabric import providerAbstractFabric

        from traders.head.trader import headTrader

        chains: dict = {
            'ETH': Chains.ETH,
            'BSC': Chains.BSC
        }

        overviews: dict = dict()

        # prepare
        for row in rows:
            i, address, protocol, chain = row[0], row[1], row[2], row[3]

            provider = BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey=chains[chain])\
                .produceProduct()

            overview = BridgeConfigurator(
                abstractFabric=overviewAbstractFabric,
                fabricKey=overviewType,
                productKey=protocol.lower()
            )\
                .produceProduct()\
                ()\
                .setAddress(address=address)\
                .setProvider(provider=provider)\
                .setTrader(trader=headTrader)\
                .create()

            overviews[i] = overview  # {1: CurveLiquidityPoolOverview(), ...}

            logging.info(f'Current Overview for {protocol} is {overview}: {overview.address}')

        # extract
        futures: dict = dict()
        for i, overview in overviews.items():
            future = overview.getOverview()
            futures[i] = future

            logging.info(f'Current Future object is {future}')

        # result
        results: dict = dict()
        for i, future in futures.items():
            result = future.result()
            results[i] = result

            logging.info(f'Current Result is {result}')

        return results

    @task()
    def loadOverviews(overviews):
        import os
        from urllib.parse import quote_plus

        from sqlalchemy import create_engine

        db_address = os.getenv('DB_ADDRESS', 'localhost')
        db_user = os.getenv('DB_USER', 'username')
        db_password = quote_plus(os.getenv('DB_PASSWORD', '111222'))
        db_name = os.getenv('DB_NAME', 'dwh')

        db_url = f'postgresql://{db_user}:{db_password}@{db_address}/{db_name}'
        db_engine = create_engine(db_url)

        query = '''
            insert into pit_liquidity_pool_overview (
                l_address_protocol_chain_id,
                pit_token_symbol,
                pit_token_reserve,
                pit_token_price
            )
            values (
                {},
                '{}',
                {},
                {}
            )
            '''
        for i, overview in overviews.items():
            for aOverview in overview:
                db_engine.execute(query.format(
                    i,
                    aOverview['symbol'],
                    aOverview['reserve'],
                    aOverview['price']))

    rows = getRows()
    overviews = getOverviews(rows=rows)
    loadOverviews(overviews=overviews)


DAG = liquidityPoolOverview()
