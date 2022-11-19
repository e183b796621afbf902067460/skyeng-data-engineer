import jinja2


exposureTypes: list = ['allocation', 'borrow', 'incentive']


conf: dict = {
    'DEX': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'dex-pool-allocation-overview'
            },
            'pool': {
                'fabricKey': 'dex-pool-overview'
            }
        }
    },
    'Farming': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'farming-pool-allocation-overview'
            },
            'incentive': {
                'fabricKey': 'farming-pool-incentive-overview'
            },
            'pool': {
                'fabricKey': 'farming-pool-overview'
            }
        }
    },
    'Staking': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'staking-pool-allocation-overview'
            },
            'incentive': {
                'fabricKey': 'staking-pool-incentive-overview'
            },
            'pool': {
                'fabricKey': 'staking-pool-overview'
            }
        }
    },
    'Lending': {
        'fabrics': {
            'allocation': {
                'fabricKey': 'lending-pool-allocation-overview'
            },
            'borrow': {
                'fabricKey': 'lending-pool-borrow-overview'
            },
            'incentive': {
                'fabricKey': 'lending-pool-incentive-overview'
            },
            'pool': {
                'fabricKey': 'lending-pool-overview'
            }
        }
    }
}
