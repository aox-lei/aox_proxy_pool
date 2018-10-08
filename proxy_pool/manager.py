# -*- coding: utf-8 -*-
import click
from proxy_pool.script.check_proxy import check_proxy
from proxy_pool.script.sync_squid import update_squid_conf


@click.group()
def cli():
    pass


@click.command()
def check_ip():
    check_proxy().run()


@click.command()
@click.option('--default-conf-path', '-d', help='默认的squid的配置文件地址')
@click.option('--conf-path', '-c', help='配置文件地址')
def sync_squid(default_conf_path, conf_path):
    update_squid_conf(default_conf_path, conf_path)


cli.add_command(check_ip)
cli.add_command(sync_squid)

if __name__ == '__main__':
    cli()