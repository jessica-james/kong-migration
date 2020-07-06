from json import load
from os import scandir

import requests


def post_new_database_schema(kong_type):
    session = requests.session()
    directory = f'./{kong_type}-json/{env_name}'
    id_list = [f.name.split('.', 1)[0] for f in scandir(directory) if f.is_file]
    print(id_list)
    for id in id_list:
        print(id)
        data = open(f'{directory}/{id}.json')
        data = load(data)
        response = session.put(url=f'{kong_url}/{kong_type}/{id}', headers=headers, json=data)
        print(f'{response.text} + {response.status_code}')
    return id_list


if __name__ == '__main__':
    env_name = None  # name of environment to process
    if not env_name:
        raise Exception('env_name must be set')

    kong_url = f'http://crate-kong.{env_name}.crate.farm/api'
    kong_admin_key = None  # api key for kong access
    headers = {"apikey": kong_admin_key}
    # Consider adding logic to ensure that kong_type is one of 'routes, plugins, or services'

    print(post_new_database_schema('services'))
    print(post_new_database_schema('routes'))
    print(post_new_database_schema('plugins'))



