import json
import pathlib

import requests
from jinja2 import Environment, FileSystemLoader


# retrieve json data for Kong Services
def get_kong_services(kong_url, kong_admin_key):
    kong_url = kong_url
    kong_admin_key = kong_admin_key
    session = requests.session()
    headers = {"Kong-Admin-Token": kong_admin_key}
    r = session.get(kong_url + '/services', headers=headers)
    print(r.json()['data'])
    return r.json()['data']

# retrieve json data for Kong Routes
def get_kong_routes(kong_url, kong_admin_key):
    kong_url = kong_url
    kong_admin_key = kong_admin_key
    session = requests.session()
    headers = {"Kong-Admin-Token": kong_admin_key}
    r = session.get(kong_url + '/routes', headers=headers)
    print(r.json()['data'])
    return r.json()['data']

# return json data for Kong Plugins
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
    # set template variables from json data from services
    for x in services_json:
        template = env.get_template('./services.json.hbs')
        id = json.dumps(x.get('id', 'null'))
        host = json.dumps(x.get('host', 'null'))
        name = json.dumps(x.get('name', 'null'))
        port = json.dumps(x.get('port', 'null'))
        protocol = json.dumps(x.get('protocol', 'null'))
        connect_timeout = json.dumps(x.get('connect_timeout', 60000))
        read_timeout = json.dumps(x.get('read_timeout', 60000))
        write_timeout = json.dumps(x.get('write_timeout', 60000))
        # render the jinja template
        output = template.render(service_name=name, service_protocol=protocol, service_port=port, service_host=host,
                                 service_connect_timeout=connect_timeout, service_id=id,
                                 service_write_timeout=write_timeout, service_read_timeout=read_timeout)
        base_dir = f'./services-json/{env_name}'
        pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True)
        with open(f'{base_dir}/{x["id"]}.json', 'w') as service:
            service.write(output)
    # create a list of service ID's to parse through so that they can be looped through and Posted back to Kong
    for x in services_json:
        service_ids.append(x['id'])
    return service_ids

def create_new_routes_data(routes_json):
    routes_json = routes_json
    route_ids = []
    file_loader = FileSystemLoader('./templates')
    env = Environment(loader=file_loader)
    for x in routes_json:
        template = env.get_template('./routes.json.hbs')
        #name = x.get('name', 'null')
        hosts = json.dumps(x.get("hosts", 'null'))
        methods = json.dumps(x.get("methods", 'null'))
        protocols = json.dumps(x.get("protocols", 'null'))
        route_id = json.dumps(x.get("id", 'null'))
        service_id = json.dumps(x.get("service", 'null'))
        preserve_host = json.dumps(x.get("preserve_host", 'true'))
        regex_priority = json.dumps(x.get("regex_priority", 0))
        paths = json.dumps(x.get("paths", 'null'))
        strip_path = json.dumps(x.get("strip_path", 'false'))

        output = template.render(route_protocol=protocols, route_methods=methods, route_hosts=hosts,
                                 route_id=route_id, route_service_id=service_id, route_preserve_host=preserve_host,
                                 route_regex_priority=regex_priority, route_paths=paths, route_strip_path=strip_path)
        base_dir = f'./routes-json/{env_name}'
        pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True)
        with open(f'{base_dir}/{x["id"]}.json', 'w') as route:
            route.write(output)
    for x in routes_json:
        route_ids.append(x['id'])
    return route_ids

def create_new_plugins_data(plugins_json):
    plugins_json = plugins_json
    plugin_ids = []
    file_loader = FileSystemLoader('./templates')
    env = Environment(loader=file_loader)
    for x in plugins_json:
        template = env.get_template('./plugins.json.hbs')
        config = x.get('config', 'null')
        keycloak_client = json.dumps(config['client_id'])
        keycloak_client = str(keycloak_client).strip("[]")
        print(keycloak_client)
        config_scope = config['scopes']
        config_scope_string = ' '.join(config_scope)
        print(config_scope_string)
        enabled = json.dumps(x.get('enabled', 'null'))
        route_id = json.dumps(x.get('route_id', 'null'))
    # render the plugins template
        output = template.render(plugins_name="oidc", plugins_enabled=enabled, config_keycloak_client=keycloak_client,
                                 plugins_route=route_id, config_scope=config_scope_string)
        base_dir = f'./plugins-json/{env_name}'
        pathlib.Path(base_dir).mkdir(parents=True, exist_ok=True)
        with open(f'{base_dir}/{x["id"]}.json', 'w') as plugin:
            plugin.write(output)

    for x in plugins_json:
        plugin_ids.append(x['id'])
    return plugin_ids


if __name__ == '__main__':
    env_name = None  # name of environment to process
    if not env_name:
        raise Exception('env_name must be set')

    kong_url = f'http://crate-kong.{env_name}.crate.farm/api'
    kong_admin_key = None  # api key to use for Kong calls
    if not kong_admin_key:
        raise Exception('kong_admin_key must be set')

    services_json = get_kong_services(kong_url, kong_admin_key)
    routes_json = get_kong_routes(kong_url, kong_admin_key)
    plugins_json = get_kong_plugins(kong_url, kong_admin_key)

    print(create_new_services_data(services_json))
    print(create_new_plugins_data(plugins_json))
    print(create_new_routes_data(routes_json))

