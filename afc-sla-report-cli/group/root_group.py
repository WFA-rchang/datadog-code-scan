import click

from command.gen_sla_report_command import gen_sla_report_command



# Banner art text
banner_art_text = """
\b
    ___    ____________   _____ __    ___       ____                        __     ________    ____
   /   |  / ____/ ____/  / ___// /   /   |     / __ \___  ____  ____  _____/ /_   / ____/ /   /  _/
  / /| | / /_  / /       \__ \/ /   / /| |    / /_/ / _ \/ __ \/ __ \/ ___/ __/  / /   / /    / /  
 / ___ |/ __/ / /___    ___/ / /___/ ___ |   / _, _/  __/ /_/ / /_/ / /  / /_   / /___/ /____/ /   
/_/  |_/_/    \____/   /____/_____/_/  |_|  /_/ |_|\___/ .___/\____/_/   \__/   \____/_____/___/   
                                                      /_/                                          
"""

# Root Group
@click.group(help=banner_art_text)
def root_cli_group():
    pass


# Add commands to Root Group
root_cli_group.add_command(gen_sla_report_command)
