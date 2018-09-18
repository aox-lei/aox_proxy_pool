# -*- coding: utf-8 -*-
import click
from script.check_proxy import check_proxy


@click.group()
def cli():
    pass


@click.command()
def check_proxy_shell():
    check_proxy().run()


cli.add_command(check_proxy_shell)

if __name__ == '__main__':
    cli()