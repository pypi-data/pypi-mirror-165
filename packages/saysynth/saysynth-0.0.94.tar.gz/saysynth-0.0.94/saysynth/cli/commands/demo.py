
import os

import click
import yaml

from saysynth.cli.commands.seq import run as run_sequence
import pkg_resources

DEMO_DIR = pkg_resources.resource_filename('saysynth', 'cli/commands/demos/')
DEMO_NAMES = [f.split('/')[-1].split('.yml')[0] for f in os.listdir(DEMO_DIR)]

def run(**kwargs):
    run_sequence(**kwargs)


@click.command()
@click.argument("command", type=click.Choice(["play", "start", "stop", "render"]), required=True)
@click.argument("name", type=click.Choice(DEMO_NAMES), required=True)
@click.option("-c", "--config-overrides", type=lambda x: yaml.safe_load(x), default='{}', help="Override global and track configurations at runtime")
def cli(**kwargs):
    name = kwargs.pop("name")
    kwargs['base_config'] = open(os.path.join(DEMO_DIR, f"{name}.yml"), 'r')
    return run(**kwargs)
