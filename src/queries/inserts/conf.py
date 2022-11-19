from src.queries.inserts.loadPoolOverviews.query import (
    q0 as loadPoolOverivew,
    q1 as loadLendingPoolOverview
)
from src.queries.inserts.loadPositionOverviews.query import (
    q0 as loadPositionOverview,
    q1 as loadBorrowPositionOverview
)


conf: dict = {
    'DEX': {
        'types': {
            'allocation': {
                'query': loadPositionOverview
            },
            'pool': {
                'query': loadPoolOverivew
            }
        }
    },
    'Farming': {
        'types': {
            'allocation': {
                'query': loadPositionOverview
            },
            'incentive': {
                'query': loadPositionOverview
            },
            'pool': {
                'query': loadPoolOverivew
            }
        }
    },
    'Staking': {
        'types': {
            'allocation': {
                'query': loadPositionOverview
            },
            'incentive': {
                'query': loadPositionOverview
            },
            'pool': {
                'query': loadPoolOverivew
            }
        }
    },
    'Lending': {
        'types': {
            'allocation': {
                'query': loadPositionOverview
            },
            'borrow': {
                'query': loadBorrowPositionOverview
            },
            'incentive': {
                'query': loadPositionOverview
            },
            'pool': {
                'query': loadLendingPoolOverview
            }
        }
    }
}
