#!/usr/bin/env python3

import sys
import click
from .__version__ import __version__
from .playlist import downloadPlaylist


@click.group()
@click.version_option(__version__)
def main():
    """A pyvdo Download and Lookup CLI"""
    pass


@main.command()
@click.argument('playlist', required=False)
def playlist(**kwargs):
    """Search through CVE Database for vulnerabilities"""
    if not kwargs['playlist']:
        click.echo("Invalid positional argument: no playlist url was provided")
    else:
        downloadPlaylist(kwargs['playlist'])


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("PYVDO")
    main()
