from typing import List, Dict, Any
from concurrent.futures import Future
from airflow.decorators import task


@task()
def getOverviews(rows: List[tuple], overviewType: str) -> Dict[int, List[Dict[str, Any]]]:

    def parallel(rows: List[tuple], overviewType: str) -> Dict[int, Future]:
        import logging
        import threading

        from head.bridge.configurator import BridgeConfigurator

        from overviews.abstracts.fabric import overviewAbstractFabric
        from providers.abstracts.fabric import providerAbstractFabric

        from traders.head.trader import headTrader

        overviews: dict = dict()

        for row in rows:
            i, address, protocol, chain = row[0], row[1], row[2], row[3]

            provider = BridgeConfigurator(
                abstractFabric=providerAbstractFabric,
                fabricKey='http',
                productKey=chain) \
                .produceProduct()

            overview = BridgeConfigurator(
                abstractFabric=overviewAbstractFabric,
                fabricKey=overviewType,
                productKey=protocol.lower()
            ) \
                .produceProduct()() \
                .setAddress(address=address) \
                .setProvider(provider=provider) \
                .setTrader(trader=headTrader) \
                .create()

            overviews[i] = overview.getOverview()

            logging.info(f'Current Overview for ({chain}){protocol} is {overview}: {overview.address}')
        return overviews

    def produce(futures: Dict[int, Future]) -> Dict[int, List[Dict[str, Any]]]:
        import logging

        overviews: dict = dict()
        for i, future in futures.items():
            overview = future.result()
            overviews[str(i)] = overview

            logging.info(f'Current Result is {overview}')

        return overviews

    futures = parallel(rows=rows, overviewType=overviewType)
    overviews = produce(futures=futures)
    return overviews
