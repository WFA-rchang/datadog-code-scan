import click
from dependency_injector.wiring import Provide, inject

from infrastructure.dependency_injection.container import Container
from application.system_health_implementation import SystemHealthApplicationImplementation


@click.command(name='system-health', help="Execute System Health Check")
@click.option('--system-names', '-s', help="System names to check, string separated by comma, default: all systems")
@click.option('--env', '-e', help="Environment to check system health", required=True)
@inject
def system_health_command(system_health_application: SystemHealthApplicationImplementation = Provide[Container.system_health_application],
                          system_names: str = '', env: str = ''):
    # Get System Healths
    click.echo("- Getting System Healths -")

    system_name_list = []
    if system_names != None:
        system_name_list = system_names.split(',')

    error, system_healths = system_health_application.get_system_health(
        system_names=system_name_list,
        env=env
    )

    if error is not None:
        raise click.ClickException(error)

    for system_health in system_healths:
        click.echo(
            f"System Name: {system_health.name}, Status: {system_health.status}"
        )
    click.echo("- End of System Healths -")
