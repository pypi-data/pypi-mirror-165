from click import Group

from edgescan.cli.command_groups.data_exports import data_exports
from edgescan.cli.command_groups.assets import assets
from edgescan.cli.command_groups.hosts import hosts
from edgescan.cli.command_groups.licenses import licenses
from edgescan.cli.command_groups.vulnerabilities import vulnerabilities

import click
import logging

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


COMMAND_GROUPS = [
    data_exports,
    assets,
    hosts,
    licenses,
    vulnerabilities,
]
for command_group in COMMAND_GROUPS:
    assert isinstance(command_group, Group)
    cli.add_command(command_group)
