import json

import common


def update_dns_lb():
    port_rules = []
    for lb_rule in crate_dns_lb.lbConfig.portRules:
        d = lb_rule.__dict__
        rule = {
            'type': lb_rule.type,
            'hostname': lb_rule.hostname,
            'protocol': lb_rule.protocol,
            'sourcePort': lb_rule.sourcePort,
            'targetPort': lb_rule.targetPort,
        }
        if lb_rule.hostname == f'crate-kong.{env_name}.crate.farm':
            rule['serviceId'] = crate_kong_lb.id
        elif 'selector' in d:
            rule['selector'] = lb_rule.selector
        elif 'serviceId' in d:
            rule['serviceId'] = lb_rule.serviceId
        port_rules.append(rule)
    lb_config = {
        'type': 'lbConfig',
        'portRules': port_rules
    }
    print(lb_config)

    # update the lb config
    client.update(crate_dns_lb, lbConfig=lb_config)


def update_kong_lb():
    # read the lb config backup
    with open(f'./lb-config/{env_name}.json', 'r') as f:
        lb_config = json.load(f)

    port_rules = []
    for lb_rule in crate_kong_lb.lbConfig.portRules:
        d = lb_rule.__dict__
        rule = {
            'type': lb_rule.type,
            'hostname': lb_rule.hostname,
            'protocol': lb_rule.protocol,
            'sourcePort': lb_rule.sourcePort,
            'targetPort': lb_rule.targetPort,
        }
        if 'selector' in d:
            rule['selector'] = lb_rule.selector
        if 'serviceId' in d:
            rule['serviceId'] = lb_rule.serviceId
        port_rules.append(rule)
    for lb_rule in lb_config['portRules']:
        port_rules.append(lb_rule)
    lb_config = {
        'type': 'lbConfig',
        'portRules': port_rules
    }
    print(lb_config)

    # update the lb config
    client.update(crate_kong_lb, lbConfig=lb_config)


if __name__ == '__main__':
    env_name = ''  # name of environment to process
    if not env_name:
        raise Exception('env_name must be set')

    client = common.get_rancher_client()
    project = client.list_project(name=env_name).data[0]

    # get handle to the kong lb
    crate_kong_stack = project.stacks(system='true', name='crate-kong').data[0]
    crate_kong_lb = project.loadBalancerServices(stackId=crate_kong_stack.id, name='kong-lb').data[0]

    # get handle to the dns lb
    crate_dns_stack = project.stacks(system='true', name='crate-dns').data[0]
    crate_dns_lb = project.loadBalancerServices(stackId=crate_dns_stack.id, name='crate-dns-lb').data[0]

    update_dns_lb()
    update_kong_lb()
