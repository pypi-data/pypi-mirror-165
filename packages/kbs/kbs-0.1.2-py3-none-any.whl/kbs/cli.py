import sys

import click
import pykube

from .secret import Secret

kube_api = None


@click.group()
def cli():
    global kube_api
    config = pykube.KubeConfig.from_file("~/.kube/config")
    kube_api = pykube.HTTPClient(config)


@cli.command("list")
@click.argument("secret")
def list(secret):
    """list configuration in var=value (envfile) format"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    for key in sorted(cfg.keys()):
        click.echo("{}={}".format(key, cfg[key]))


@cli.command("get")
@click.argument("secret")
@click.argument("key")
def get(secret, key):
    """get a single config variable"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    if key not in cfg:
        click.echo("No var found for `{}.{}`".format(secret, key))
        return
    click.echo(cfg[key])


@cli.command("set")
@click.argument("secret")
@click.argument("key")
@click.argument("value")
def set(secret, key, value):
    """set a single config variable"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    cfg[key] = value
    cfg.update()


@cli.command("unset")
@click.argument("secret")
@click.argument("key")
def unset(secret, key):
    """remove a single config variable"""
    global kube_api
    try:
        cfg = Secret.objects(kube_api).get_by_name(secret)
    except pykube.exceptions.ObjectDoesNotExist:
        click.echo(
            f"Could not find secret object named '{secret}' in the current kubectl context"
        )
        sys.exit(1)

    if click.confirm(
        "Do you wish to delete config variable {}.{} with value of `{}`".format(
            secret, key, cfg[key]
        )
    ):
        del cfg[key]
        cfg.update()
