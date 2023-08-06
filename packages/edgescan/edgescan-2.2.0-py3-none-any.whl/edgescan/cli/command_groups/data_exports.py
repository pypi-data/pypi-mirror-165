import os.path

import click
from click import Context

from edgescan.cli.command_groups import assets, hosts, vulnerabilities, licenses
from edgescan.constants import VULNERABILITIES, LICENSES, HOSTS, ASSETS


@click.group()
def data_exports():
    """
    Export assets, hosts, licenses, and/or vulnerabilities to a local file.
    """
    pass


@data_exports.command()
@click.argument('directory', required=True)
@click.pass_context
def export_all(ctx: Context, directory: str):
    for resource_type, f in [
        [ASSETS, export_assets],
        [HOSTS, export_hosts],
        [LICENSES, export_licenses],
        [VULNERABILITIES, export_vulnerabilities]
    ]:
        path = os.path.join(directory, resource_type + '.jsonl')
        ctx.invoke(f, path=path)


@data_exports.command()
@click.argument('path', required=True)
@click.pass_context
def export_assets(ctx: Context, path: str):
    ctx.invoke(assets.export_assets, path=path)


@data_exports.command()
@click.argument('path', required=True)
@click.pass_context
def export_hosts(ctx: Context, path: str):
    ctx.invoke(hosts.export_hosts, path=path)


@data_exports.command()
@click.argument('path', required=True)
@click.pass_context
def export_assets(ctx: Context, path: str):
    ctx.invoke(vulnerabilities.export_vulnerabilities, path=path)


@data_exports.command()
@click.argument('path', required=True)
@click.pass_context
def export_licenses(ctx: Context, path: str):
    ctx.invoke(licenses.export_licenses, path=path)


@data_exports.command()
@click.argument('path', required=True)
@click.pass_context
def export_vulnerabilities(ctx: Context, path: str):
    ctx.invoke(vulnerabilities.export_vulnerabilities, path=path)
