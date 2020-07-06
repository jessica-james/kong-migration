import json
import pathlib

import common

if __name__ == '__main__':
    env_name = ''  # name of environment to process
    if not env_name:
        raise Exception('env_name must be set')

    client = common.get_rancher_client()
    project = client.list_project(name=env_name).data[0]
    crate_kong_stack = project.stacks(system='true', name='crate-kong').data[0]
    crate_kong_lb = project.loadBalancerServices(stackId=crate_kong_stack.id, name='kong-lb').data[0]

    # get port rules for all user defined api gateway routes
    current_config = {
        'portRules': []
    }
    for cfg in crate_kong_lb.lbConfig.portRules:
        if cfg.hostname == f'crate-kong.{env_name}.crate.farm':
            continue
        d = cfg.__dict__
        rule = {}
        if 'hostname' in d:
            rule['hostname'] = cfg.hostname
        if 'path' in d:
            rule['path'] = cfg.path
        if 'priority' in d:
            rule['priority'] = cfg.priority
        if 'protocol' in d:
            rule['protocol'] = cfg.protocol
        if 'selector' in d:
            rule['selector'] = cfg.selector
        if 'sourcePort' in d:
            rule['sourcePort'] = cfg.sourcePort
        if 'targetPort' in d:
            rule['targetPort'] = cfg.targetPort
        current_config['portRules'].append(rule)

    # persist the port rules to a json file
    directory = f'./lb-config'
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    with open(f'{directory}/{env_name}.json', 'w') as f:
        json.dump(current_config, f, indent=4)
