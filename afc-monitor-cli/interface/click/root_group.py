import click

from interface.click.command.system_health_command import system_health_command
from interface.click.command.scheduler_status_command import scheduler_status_command
from interface.click.command.proactive_monitor_command import proactive_monitor_command


# Banner art text
banner_art_text = """
\b
    ___    ____________   __  ___            _ __                ________    ____
   /   |  / ____/ ____/  /  |/  /___  ____  (_) /_____  _____   / ____/ /   /  _/
  / /| | / /_  / /      / /|_/ / __ \/ __ \/ / __/ __ \/ ___/  / /   / /    / /  
 / ___ |/ __/ / /___   / /  / / /_/ / / / / / /_/ /_/ / /     / /___/ /____/ /   
/_/  |_/_/    \____/  /_/  /_/\____/_/ /_/_/\__/\____/_/      \____/_____/___/   
                                                                                 
"""

# Root Group
@click.group(help=banner_art_text)
def root_cli_group():
    pass


# Add commands to Root Group
root_cli_group.add_command(proactive_monitor_command)
root_cli_group.add_command(system_health_command)
root_cli_group.add_command(scheduler_status_command)
