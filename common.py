import os

import gdapi


def get_rancher_client():
    if 'RANCHER_API_URL' not in os.environ:
        raise Exception('RANCHER_API_URL env var must be set')
    if 'RANCHER_ACCESS_KEY' not in os.environ:
        raise Exception('RANCHER_ACCESS_KEY env var must be set')
    if 'RANCHER_SECRET_KEY' not in os.environ:
        raise Exception('RANCHER_SECRET_KEY env var must be set')
    return gdapi.Client(url=os.getenv('RANCHER_API_URL'),
                        access_key=os.getenv('RANCHER_ACCESS_KEY'),
                        secret_key=os.getenv('RANCHER_SECRET_KEY'))
