from typing import List, Dict, Any
from airflow.decorators import task


@task()
def getOverviews(
        rows: List[tuple],
        fabricKey: str,
        overviewType: str,
        exposureTypes: list
) -> Dict[int, List[Dict[str, Any]]]:
    import logging

    from head.bridge.configurator import BridgeConfigurator

    from overviews.abstracts.fabric import overviewAbstractFabric
    from providers.abstracts.fabric import providerAbstractFabric

    from traders.head.trader import headTrader

    futures: dict = dict()

    for row in rows:
        if overviewType.lower() in exposureTypes:
            i, poolAddress, walletAddress, protocol, chain = row[0], row[1], row[2], row[3], row[4]
        else:
            i, poolAddress, protocol, chain = row[0], row[1], row[2], row[3]

        provider = BridgeConfigurator(
            abstractFabric=providerAbstractFabric,
            fabricKey='http',
            productKey=chain) \
            .produceProduct()

        handler = BridgeConfigurator(
            abstractFabric=overviewAbstractFabric,
            fabricKey=f'{fabricKey.lower()}',
            productKey=protocol.lower()
        ) \
            .produceProduct()() \
            .setAddress(address=poolAddress) \
            .setProvider(provider=provider) \
            .setTrader(trader=headTrader) \
            .create()

        if overviewType.lower() in exposureTypes:
            futures[i] = handler.getOverview(address=walletAddress)
        else:
            futures[i] = handler.getOverview()

        logging.info(f'Current Overview for ({chain}){protocol} is {handler}: {handler.address}')

    overviews: dict = dict()
    for i, future in futures.items():
        overview = future.result()
        overviews[str(i)] = overview

        logging.info(f'Current Result is {overview}')

    return overviews
