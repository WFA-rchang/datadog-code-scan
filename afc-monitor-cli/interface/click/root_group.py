import click
from art import text2art, tprint

from interface.click.command.proactive_monitor_command import proactive_monitor_command


# Banner art text
banner_art_text = tprint("AFC Monitor CLI")

# Root Group
@click.group(help=banner_art_text)
def root_cli_group():
    pass


# Add commands to Root Group
root_cli_group.add_command(proactive_monitor_command)
