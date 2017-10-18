import click
import requests

BOTTLENOSE_AUTH_TOKEN = '5a5da3a959fa2cf23105d0fe24efe5fb3116aee4'  # test token
BOTTLENOSE_API_URL = 'http://127.0.0.1:8000/api/'

headers = {
    'Authorization': f'Token {BOTTLENOSE_AUTH_TOKEN}'
}

print(headers)

@click.group()
def cli():
    pass


@cli.command()
def login():
    click.echo('Login')


@cli.command()
def start():
    click.echo('Start')
    endpoint = 'worklog/start/'
    r = requests.post(f'{BOTTLENOSE_API_URL}{endpoint}', headers=headers)
    click.echo(r.url)
    click.echo(r.status_code)
    click.echo('-----')
    click.echo(r.json())


@cli.command()
def stop():
    click.echo('Stop')


@cli.command()
def log():
    click.echo('Log')
