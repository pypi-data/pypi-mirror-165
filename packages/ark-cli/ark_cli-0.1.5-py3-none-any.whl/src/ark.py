# coding: utf-8

import os
import click
import src.commands.init as cmd_init
from src.definitions.platform import Platform
from src.models.project import Project


@click.group()
@click.pass_context
def cli(ctx):
    """ark - Command line tool to manage ark mobile app"""
    ctx.obj = Project()


@cli.command()
@click.pass_obj
@click.option('--name', prompt = 'name of your mobile app', default = 'my-app', required = True, help = 'Name of your mobile app')
@click.option('--platform', prompt = '{0}/{1}'.format(Platform.ANDROID, Platform.IOS),
              default = Platform.ANDROID, type=click.Choice([Platform.ANDROID, Platform.IOS]), required = True, help = 'Select a platform')
@click.option('--package', prompt = 'package name / app identifier', default = 'com.example.myapp', required = True, help = 'PackageName / App identifier')
def init(project: Project, name: str, platform: str, package: str):
    cmd_init.init(name, platform, package)

