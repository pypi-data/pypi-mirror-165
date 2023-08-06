import os
import sys
import json
from contextlib import redirect_stderr, redirect_stdout
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager


def parse_inventory(path):
    with open(os.devnull, 'w') as fd, redirect_stderr(fd), redirect_stdout(fd):
        loader = DataLoader()
        inventory = InventoryManager(
            loader=loader,
            sources=path
        )
    data = dict(groups=[], hosts=[], vars={})

    for group in inventory.groups:
        if group == 'ungrouped':
            continue
        elif group == 'all':
            data['vars'] = inventory.groups[group].vars
            continue
        group_data = dict(
            name=group,
            hosts=[],
            groups=[],
            vars=inventory.groups[group].vars
        )
        for host in inventory.groups[group].hosts:
            group_data['hosts'].append(host.name)
        for child_group in inventory.groups[group].child_groups:
            group_data['groups'].append(child_group.name)
        data['groups'].append(group_data)

    for host in inventory.hosts:
        host_data = dict(name=host, vars=inventory.hosts[host].vars)
        del host_data['vars']['inventory_file']
        del host_data['vars']['inventory_dir']
        data['hosts'].append(host_data)

    return json.dump(data, sys.stdout, indent=4)


def handler(args=sys.argv[1:]):
    return parse_inventory(args[0])
