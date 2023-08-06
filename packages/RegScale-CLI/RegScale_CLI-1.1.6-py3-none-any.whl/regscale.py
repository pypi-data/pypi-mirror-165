#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard python imports"""
import click
from rich.console import Console

import app.healthcheck as hc
import app.login as lg

############################################################
# Versioning
############################################################
from app._version import __version__
from app.ad import ad
from app.application import Application
from app.cisa import cisa
from app.jira import jira
from app.logz import create_logger
from app.migrations import migrations
from app.oscal import oscal
from app.servicenow import servicenow
from app.wiz import wiz

############################################################
# CLI Command Definitions
############################################################

console = Console()

app = Application()


class Mutex(click.Option):
    """Mutex Class to modify click context"""

    def __init__(self, *args, **kwargs):
        kwargs["help"] = (
            kwargs.get("help", "") + "Option is mutually exclusive with " + "."
        ).strip()
        self.logger = logger
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        logger.debug(ctx.__dict__)
        if lg.is_valid(app=app):
            logger.debug("valid")
        else:
            prompt = list(ctx.__dict__["params"].keys())[0]
            if prompt == "username":
                self.logger.debug(prompt)
                self.prompt = "Enter your RegScale Password"
            # raise click.UsageError(
            #     "Illegal usage: '"
            #     + str(self.name)b
            #     + "' is mutually exclusive with "
            #     + str(mutex_opt)
            #     + "."
            # )
        # if ctx.params["username"] is None:
        #     self.prompt = "Enter your RegScale Password"

        return super().handle_parse_result(ctx, opts, args)


logger = create_logger()


@click.group()
def cli():
    """
    CLI click object
    """


# About function
@cli.command()
def about():
    """Provides information about the CLI and its current version."""
    banner()
    console.print("[red]RegScale[/red] CLI Version: " + __version__)
    console.print("Author: J. Travis Howerton (thowerton@regscale.com)")
    console.print("Copyright: RegScale Incorporated")
    console.print("Website: https://www.regscale.com")
    console.print("Read the CLI Docs: https://regscale.com/documentation/cli-overview")
    java = app.get_java()
    matches = ["not found", "internal or external"]
    if not any(x in java for x in matches):
        console.print(f"Java: {java}")


def banner():
    """Banner"""
    txt = """

\t [#21a5bb]///////////////////////////\t
\t[#21a5bb]/////////////////////////*****\t
\t//////                  /*******\t
\t//////                      //////
\t//////              [#ef5d23]////[/#ef5d23]     //////
\t ////            [#ef5d23]////////[/#ef5d23]    /////
\t               [#ef5d23]////////[/#ef5d23]     //////[/#21a5bb]\t
\t [#f8b737]***[/#f8b737]         [#ef5d23]////////[/#ef5d23]    /(((///\t
\t[#f8b737]******[/#f8b737]      [#ef5d23]/((((/(([/#ef5d23]   ((((((((\t
\t[#f8b737]******[/#f8b737]    [#ef5d23](((((((([/#ef5d23]   ((((((((\t
\t[#f8b737]******[/#f8b737]  [#ef5d23]((((((([/#ef5d23]     (((((((\t
\t[#f8b737]******[/#f8b737] [#ef5d23](((#(([/#ef5d23]        (((([#23539e]####[/#23539e]\t
\t[#f8b737]******[/#f8b737] [#ef5d23]((##[/#ef5d23]            [#23539e]########[/#23539e]\t
\t[#f8b737]******[/#f8b737][#ef5d23]##[/#ef5d23]                [#23539e]######(([/#23539e]\t
\t[#f8b737]****[/#f8b737][#ef5d23]#[/#ef5d23]                   [#23539e]######[/#23539e]
\t[#f8b737]****[/#f8b737]                      [#23539e]#####[/#23539e]
    """
    console.print(txt)


# Log into RegScale to get a token
@cli.command()
@click.option(
    "--username",
    hide_input=False,
    help="RegScale User Name",
    prompt="Enter RegScale User Name"
    # cls=Mutex,
)
@click.option(
    "--password",
    hide_input=True,
    help="RegScale Password",
    cls=Mutex,
)
def login(username, password=None):
    """Logs the user into their RegScale instance"""

    logger.debug("login: ")
    if password:
        lg.login(username, password, app=app)
    else:
        valid = lg.is_valid(app=app)
        if valid:
            logger.info("Already logged in!")


# Check the health of the RegScale Application
@cli.command()
def healthcheck():
    """Monitoring tool to check the health of the RegScale instance"""
    hc.status()


# add OSCAL support
cli.add_command(oscal)

# add Wiz support
cli.add_command(wiz)

# add data migration support
cli.add_command(migrations)

# add Azure Active Directory (AD) support
cli.add_command(ad)

# add ServiceNow support
cli.add_command(servicenow)

# add JIRA support
cli.add_command(jira)

# add JIRA support
cli.add_command(cisa)

# start function for the CLI
if __name__ == "__main__":
    cli()
