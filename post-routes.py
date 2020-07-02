import requests
from os import scandir
import json

def post_new_database_schema(kong_type):
    session = requests.session()
    directory = f'./{kong_type}-json/'
    id_list = [f.name for f in scandir(directory) if f.is_dir]
    print(id_list)
    for id in id_list:
        print(id)
        data = open(f'./{kong_type}-json/{id}/{kong_type}.json')
        data = json.load(data)
        response = session.put(url=f'{kong_url}/{kong_type}/{id}', headers=headers, json=data)
        print(f'{response.text} + {response.status_code}')
    return id_list


if __name__ == '__main__':
    kong_url = 'http://crate-kong.formal-chicken-dinner.crate.farm/api'
    kong_admin_key = #api key needed
    headers = {"Kong-Admin-Token": kong_admin_key}
    # Consider adding logic to ensure that kong_type is one of 'routes, plugins, or services'
    kong_type = 'plugins'

    print(post_new_database_schema(kong_type))



