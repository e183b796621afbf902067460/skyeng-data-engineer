from src.queries.selects.extractAllPools.query import q as extractAllPools
from src.queries.selects.extractAllPositions.query import q as extractAllPositions


conf: dict = {
    'DEX': {
        'types': {
            'allocation': {
                'query': extractAllPositions
            },
            'pool': {
                'query': extractAllPools
            }
        }
    },
    'Farming': {
        'types': {
            'allocation': {
                'query': extractAllPositions
            },
            'incentive': {
                'query': extractAllPositions
            },
            'pool': {
                'query': extractAllPools
            }
        }
    },
    'Staking': {
        'types': {
            'allocation': {
                'query': extractAllPositions
            },
            'incentive': {
                'query': extractAllPositions
            },
            'pool': {
                'query': extractAllPools
            }
        }
    },
    'Lending': {
        'types': {
            'allocation': {
                'query': extractAllPositions
            },
            'borrow': {
                'query': extractAllPositions
            },
            'incentive': {
                'query': extractAllPositions
            },
            'pool': {
                'query': extractAllPools
            }
        }
    }
}
