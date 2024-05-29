import click
from dependency_injector.wiring import Provide, inject

from infrastructure.dependency_injection.container import Container
from application.mp_application_implementation import MPApplicationImplementation


@click.command(name='proactive-monitor', help="Execute Proactive Monitor")
@inject
def proactive_monitor_command(mp_application: MPApplicationImplementation = Provide[Container.mp_application]):
    # Get NRAs
    click.echo("- Getting NRAs -")
    error, nras = mp_application.get_nras()
    if error is not None:
        raise click.ClickException(error)

    for nra in nras:
        click.echo(f"Ruleset ID: {nra.ruleset_id}, Certification ID: {nra.certification_id}, Is Authed: {nra.is_authed}")
    click.echo("- End of NRAs -")
