import bencodex
import requests
import click


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
core_addr = lambda n: f'0x{n:0>40x}'

def get_state(address):
    data = {"query": f"query{{ state(address: \"{address}\") }}"}
    response = requests.post(
        'http://localhost:23061/graphql', headers=headers, json=data
    )
    try:
        return bencodex.loads(
            bytes.fromhex(response.json()['data']['state'])
        )
    except TypeError:
        return {}


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

if __name__ == '__main__':
    cli()
