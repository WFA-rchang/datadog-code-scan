import click
from dependency_injector.wiring import Provide, inject

from infrastructure.dependency_injection.container import Container
from application.mp_application_implementation import MPApplicationImplementation
from application.afc_service_status_application_implementation import AFCServiceStatusApplicationImplementation


@click.command(name='proactive-monitor', help="Execute Proactive Monitor")
@inject
def proactive_monitor_command(mp_application: MPApplicationImplementation = Provide[Container.mp_application],
                              afc_service_status_application: AFCServiceStatusApplicationImplementation = Provide[Container.afc_service_status_application]):
    # Get NRAs
    click.echo("- Getting NRAs -")
    error, nras = mp_application.get_nras()
    if error is not None:
        raise click.ClickException(error)

    for nra in nras:
        click.echo(f"Ruleset ID: {nra.ruleset_id}, Certification ID: {nra.certification_id}, Is Authed: {nra.is_authed}")
    click.echo("- End of NRAs -")

    # Get Datadog End to End Status
    click.echo("- Getting End to End Status -")
    error, end_to_end_status = afc_service_status_application.get_end_to_end_status()
    if error is not None:
        raise click.ClickException(error)
    
    regions_status = end_to_end_status.regions_status
    for region in regions_status:
        click.echo(f"Region: {region.region}, Status: {region.status}")
    click.echo("- End of End to End Status -")