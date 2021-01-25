import click
import pprint

from common import (core_addr,
                    get_state,
                    get_characters_block)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('address')
def activated(address):
    """Check given address is activated or not"""
    activated_accs = [
        f'0x{b.hex()}' 
        for b 
        in get_state(core_addr(8))['accounts']
    ]
    click.echo(address.lower() in activated_accs)


@cli.command()
@click.argument('address')
def inspect(address):
    """Inspect given address characters"""
    pprint.pprint(get_characters_block(address))


if __name__ == '__main__':
    cli()
