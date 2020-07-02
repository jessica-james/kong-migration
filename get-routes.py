import requests
from os import path, mkdir
import json
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
        id = x.get('id', 'null')
        id = json.dumps(id)
        host = x.get('host', 'null')
        host = json.dumps(host)
        name = x.get('name', 'null')
        name = json.dumps(name)
        port = x.get('port', 'null')
        port = json.dumps(port)
        protocol = x.get('protocol', 'null')
        protocol = json.dumps(protocol)
        #service_path = x.get('path', 'null')
        connect_timeout = x.get('connect_timeout', 60000)
        connect_timeout = json.dumps(connect_timeout)
        read_timeout = x.get('read_timeout', 60000)
        read_timeout = json.dumps(read_timeout)
        write_timeout = x.get('write_timeout', 60000)
        write_timeout = json.dumps(write_timeout)
        #retries = x.get('retries', 'null')
        # render the jinja template
        output = template.render(service_name=name, service_protocol=protocol, service_port=port, service_host=host,
                                 service_connect_timeout=connect_timeout, service_id=id,
                                 service_write_timeout=write_timeout, service_read_timeout=read_timeout)
        if not path.isdir(f'./services-json/{x["id"]}/'):
            mkdir(f'./services-json/{x["id"]}')
        with open(f'./services-json/{x["id"]}/services.json', 'w') as service:
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
        hosts = x.get("hosts", 'null')
        hosts = json.dumps(hosts)
        methods = x.get("methods", 'null')
        methods = json.dumps(methods)
        protocols = x.get("protocols", 'null')
        protocols = json.dumps(protocols)
        route_id = x.get("id", 'null')
        route_id = json.dumps(route_id)
        service_id = x.get("service", 'null')
        service_id = json.dumps(service_id)
        preserve_host = x.get("preserve_host", 'true')
        preserve_host = json.dumps(preserve_host)
        regex_priority = x.get("regex_priority", 0)
        regex_priority = json.dumps(regex_priority)
        paths = x.get("paths", 'null')
        paths = json.dumps(paths)
        strip_path = x.get("strip_path", 'false')
        strip_path = json.dumps(strip_path)

        output = template.render(route_protocol=protocols, route_methods=methods, route_hosts=hosts,
                                 route_id=route_id, route_service_id=service_id, route_preserve_host=preserve_host,
                                 route_regex_priority=regex_priority, route_paths=paths, route_strip_path=strip_path)
        if not path.isdir(f'./routes-json/{x["id"]}/'):
            mkdir(f'./routes-json/{x["id"]}/')
        with open(f'./routes-json/{x["id"]}/routes.json', 'w') as route:
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
        config_scope_string = ''
        config_scope = config['scopes']
        for scope in config_scope:
            if len(config_scope) == 2:
                if scope == 'openid':
                    config_scope_string += f'{scope} '
                else:
                    config_scope_string += scope
            else:
                config_scope_string += scope
        print(config_scope_string)
        enabled = x.get('enabled', 'null')
        enabled = json.dumps(enabled)
        # name = x.get('name', 'null')
        # name = json.dumps(name)
        route_id = x.get('route_id', 'null')
        route_id = json.dumps(route_id)
    # render the plugins template
        output = template.render(plugins_name="oidc", plugins_enabled=enabled, config_keycloak_client=keycloak_client,
                                 plugins_route=route_id, config_scope=config_scope_string)
        if not path.isdir(f'./plugins-json/{x["id"]}/'):
            mkdir(f'./plugins-json/{x["id"]}')
        with open(f'./plugins-json/{x["id"]}/plugins.json', 'w') as plugin:
            plugin.write(output)

    for x in plugins_json:
        plugin_ids.append(x['id'])
    return plugin_ids


if __name__ == '__main__':
    kong_url = #kong_url e.g. 'http://crate-kong.formal-chicken-dinner.crate.farm'
    kong_admin_key = #kong_api_key

    services_json = get_kong_services(kong_url, kong_admin_key)
    routes_json = get_kong_routes(kong_url, kong_admin_key)
    plugins_json = get_kong_plugins(kong_url, kong_admin_key)

    print(create_new_services_data(services_json))
    print(create_new_plugins_data(plugins_json))
    print(create_new_routes_data(routes_json))

