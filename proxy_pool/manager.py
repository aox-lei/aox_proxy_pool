# -*- coding: utf-8 -*-
import click
from proxy_pool.script.check_proxy import check_proxy

@click.group()
def cli():
    pass

@click.command()
def check_ip():
    check_proxy().run()

cli.add_command(check_ip)

if __name__ == '__main__':
    cli()