#!/usr/bin/env python

import argparse
import logging
from cinderclient import client as cinder_client
from glanceclient import client as glance_clients
from keystoneclient import client as keystone_client
from novaclient import client as nova_client
logging.basicConfig(level=logging.ERROR)


class ResourcePrinter(object):
    def __init__(self, *os_creds):
        self.nova = NovaManager(*os_creds)
        self.glance = GlanceManager(*os_creds)
        self.neutron = NeutronManager(*os_creds)
        self.cinder = CinderManager(*os_creds)

    def format_size(self, flavor):
        res = divmod(flavor.ram, 1024)
        if res[0] == 0:
            ram = ' '.join([str(res[1]) + 'MB', 'RAM'])
        else:
            ram = ' '.join([str(res[0]) + 'GB', 'RAM'])
        vcpus = ' '.join([str(flavor.vcpus), 'VCPU'])
        disk = ' '.join([str(flavor.disk) + 'GB', 'Disk'])
        return ' '.join([flavor.name, ram, vcpus, disk])

    def print_servers(self):
        table = nova_client(['ID', 'Instance Name',
                                         'Status', 'Image Name',
                                         'Size', 'Key Pair',
                                         'Network'])
        image_name = self.glance.image_get(server.image['id']).name
        flavor = self.nova.flavor_get(server.flavor['id'])

    def print_images(self):
        columns = ['ID', 'Name', 'Disk Format',
                   'Container Format', 'Size']
        tenant_images = self.glance.image_list()
        glance_client.print_list(tenant_images)


def main():
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("username", type=str, nargs=1,
                        help="A user name with access to the "
                             "project")
    parser.add_argument("password", type=str, nargs=1,
                        help="The user's password")
    parser.add_argument("project", type=str, nargs=1,
                        help="Name of project")
    parser.add_argument("auth_url", type=str, nargs=1,
                        help="Authentication URL")
    args = parser.parse_args()
    os_creds = (args.username[0], args.password[0],
                args.project[0], args.auth_url[0])

    ResourcePrinter(*os_creds).run()

if __name__ == "__main__":
    main()
