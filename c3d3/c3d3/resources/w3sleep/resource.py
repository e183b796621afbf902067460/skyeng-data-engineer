import time
import random
from dagster import resource


class W3Sleep:
    instance, n = None, 0

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(W3Sleep, cls).__new__(cls)
        return cls.instance

    @classmethod
    def sleep(cls):
        time.sleep(min(2 ** cls.n + random.uniform(0, .1), 64))
        cls.n += 1


@resource
def w3sleep(init_context) -> None:
    return W3Sleep()
