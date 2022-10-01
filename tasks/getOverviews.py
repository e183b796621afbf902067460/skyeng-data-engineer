from typing import List, Dict, Any
from airflow.decorators import task


@task()
def task(rows: List[tuple], protocolCategory: str) -> Dict[int, List[Dict[str, Any]]]:
    import logging

    from head.bridge.configurator import BridgeConfigurator

    from overviews.abstracts.fabric import overviewAbstractFabric
    from providers.abstracts.fabric import providerAbstractFabric

    from traders.head.trader import headTrader

    futures: dict = dict()

    for row in rows:
        i, address, protocol, chain = row[0], row[1], row[2], row[3]

        provider = BridgeConfigurator(
            abstractFabric=providerAbstractFabric,
            fabricKey='http',
            productKey=chain) \
            .produceProduct()

        handler = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey=f'{protocolCategory.lower()}-pool-overview',
            productKey=protocol.lower()
        ) \
            .produceProduct()() \
            .setAddress(address=address) \
            .setProvider(provider=provider) \
            .setTrader(trader=headTrader) \
            .create()

        futures[i] = handler.getOverview()

        logging.info(f'Current Overview for ({chain}){protocol} is {handler}: {handler.address}')

    overviews: dict = dict()
    for i, future in futures.items():
        overview = future.result()
        overviews[str(i)] = overview

        logging.info(f'Current Result is {overview}')

    return overviews
