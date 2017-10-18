import stat
import os

import click
import requests


BOTTLENOSE_API_URL = 'http://127.0.0.1:8000/api/'


def has_valid_permissions(path):
    perm = oct(stat.S_IMODE(os.lstat(path).st_mode))
    return perm == oct(0o600)


def get_token():
    try:
        tokenfile = os.path.join(os.environ['HOME'], '.bnose')
        token = None
        if os.path.isfile(tokenfile):
            with open(tokenfile, 'r') as outfile:
                token = outfile.read().rstrip()
            if not has_valid_permissions(tokenfile):
                # invalidate token
                token = None
        return token
    except KeyError:
        raise OSError('Could not find .bnose: $HOME is not set')


def get_headers(**kwargs):
    headers = {
        'user-agent': 'bnose/1.0'
    }
    headers.update(**kwargs)
    return headers


def get_auth_headers():
    return get_headers(**{'Authorization': 'Token %s' % get_token()})


def _request(endpoint, **kwargs):
    url = '{base_api_url}{endpoint}'.format(
        base_api_url=BOTTLENOSE_API_URL,
        endpoint=endpoint
    )
    response = requests.post(url, headers=get_auth_headers(), data=kwargs)
    output = response.json()
    message = output['message']
    if 'color' in output.keys():
        color = output['color']
    else:
        color = 'green'
    click.secho(message, fg=color)


@click.group()
def cli():
    pass


@cli.command()
def login():
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)

    endpoint = '%sauth/' % BOTTLENOSE_API_URL
    response = requests.post(endpoint, data={'username': username, 'password': password}, headers=get_headers())
    output = response.json()

    if 'token' in output.keys():
        try:
            tokenfile = os.path.join(os.environ['HOME'], '.bnose')
            with open(tokenfile, 'w') as outfile:
                outfile.write(output['token'])
            os.chmod(tokenfile, 0o600)
        except KeyError:
            raise OSError('Could not find .bnose: $HOME is not set')

    click.echo(output)


@cli.command()
@click.option('--memo', '-m', default='')
def start(memo):
    """Start worklog tracking"""
    _request('worklog/start/', **{'memo': memo})


@cli.command()
def pause():
    """Pause worklog tracking"""
    _request('worklog/pause/')


@cli.command()
def resume():
    """Resume worklog tracking"""
    _request('worklog/resume/')


@cli.command()
def status():
    """Status of the current worklog tracking session"""
    _request('worklog/status/')


@cli.command()
def stop():
    """Stop worklog tracking"""
    _request('worklog/stop/')


@cli.command()
def log():
    click.echo('Log')
