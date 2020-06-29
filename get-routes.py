import requests
from os import path, mkdir
import json
from jinja2 import Environment, FileSystemLoader


def get_kong_services(kong_url, kong_admin_key):
    kong_url = kong_url
    kong_admin_key = kong_admin_key
    session = requests.session()
    headers = {"Kong-Admin-Token": kong_admin_key}
    r = session.get(kong_url + '/services', headers=headers)
    print(r.json()['data'])
    return r.json()['data']

def get_kong_routes(kong_url, kong_admin_key):
    kong_url = kong_url
    kong_admin_key = kong_admin_key
    session = requests.session()
    headers = {"Kong-Admin-Token": kong_admin_key}
    r = session.get(kong_url + '/routes', headers=headers)
    print(r.json()['data'])
    return r.json()['data']

def get_kong_plugins(kong_url, kong_admin_key):
    kong_url = kong_url
    kong_admin_key = kong_admin_key
    session = requests.session()
    headers = {"Kong-Admin-Token": kong_admin_key}
    r = session.get(kong_url + '/plugins', headers=headers)
    print(r.json()['data'])
    return r.json()['data']


def create_new_services_data(services_json):
    service_ids = []
    services_json = services_json
    file_loader = FileSystemLoader('./templates')
    env = Environment(loader=file_loader)
    for x in services_json:
        template = env.get_template('./services.json.hbs')
        host = x['host']
        name = x['name']
        port = x['port']
        protocol = x['protocol']
        service_path = x['path']
        connect_timeout = x['connect_timeout']
        read_timeout = x['read_timeout']
        write_timeout = x['write_timeout']
        retries = x['retries']
        output = template.render(service_name=name, service_protocol=protocol, service_port=port, service_host=host,
                                 service_path=service_path, service_connect_timeout=connect_timeout,
                                 service_write_timeout=write_timeout, service_read_timeout=read_timeout,
                                 service_retries=retries)
        if not path.isdir(f'./services-json/{x["id"]}/'):
            mkdir(f'./services-json/{x["id"]}')
        with open(f'./services-json/{x["id"]}/service.json', 'w') as service:
            service.write(output)

    for x in services_json:
        service_ids.append(x['id'])
    return service_ids

def create_new_routes_data(routes_json):
    routes_json = routes_json
    route_ids = []
    file_loader = FileSystemLoader('./templates')
    env = Environment(loader=file_loader)
    for x in routes_json:
        template = env.get_template('./templates/routes.json.hbs')




# def post_new_schema(kong_url, kong_admin_key):
#     kong_url = kong_url
#     kong_admin_key = kong_admin_key
#     session = requests.session()
#     headers = {"Kong-Admin-Token": kong_admin_key}



if __name__ == '__main__':
    kong_url = 'http://crate-kong.formal-chicken-dinner.crate.farm/api'
    kong_admin_key = '14_Little_Known_Ski_Jumping_Tips_From_Elon_Musk'

    services_json = get_kong_services(kong_url, kong_admin_key)
    routes_json = get_kong_routes(kong_url, kong_admin_key)
    plugins_json = get_kong_plugins(kong_url, kong_admin_key)

    print(create_new_services_data(services_json))

    # for x in services_json['data']:
    #     print(x['id'])
