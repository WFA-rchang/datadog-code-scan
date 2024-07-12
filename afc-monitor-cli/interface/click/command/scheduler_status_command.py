import click
from dependency_injector.wiring import Provide, inject

from infrastructure.dependency_injection.container import Container
from application.scheduler_status_application_implementation import SchedulerStatusApplicationImplementation


@click.command(name='scheduler-status', help="Execute Scheduler Execution Status Check")
@click.option('--scheduler-names', help="Execute Scheduler Execution Status Check")
@click.option('--env', '-e', help="Environment to check system health", required=True)
@inject
def scheduler_status_command(
    scheduler_status_application: SchedulerStatusApplicationImplementation = Provide[
        Container.scheduler_status_application
    ],
    scheduler_names: str = '',
    env: str = '',
):
    # Get Scheduler Status
    click.echo("- Getting Scheduler Status -")

    scheduler_names_list = []
    if scheduler_names is not None:
        scheduler_names_list = scheduler_names.split(',')

    error, scheduler_status = scheduler_status_application.get_scheduler_status(
        scheduler_names=scheduler_names_list, env=env
    )

    if error is not None:
        raise click.ClickException(error)

    for scheduler in scheduler_status:
        click.echo(f"Scheduler Name: {scheduler.name}, Status: {scheduler.status}")
    click.echo("- End of Scheduler Status -")
