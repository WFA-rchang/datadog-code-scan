import click
from tabulate import tabulate
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

    # Get Companies Contracts Usages
    click.echo("- Getting Companies Contracts Usages -")
    error, companies_contracts_usages = mp_application.get_companies_contracts_usages()
    if error is not None:
        raise click.ClickException(error)

    companies_contracts_usages_list = []
    for company_contracts_usage in companies_contracts_usages:
        for contract_group in company_contracts_usage.contract_groups:
            for monthly_bucket in contract_group.monthly_buckets:
                companies_contracts_usages_list.append(
                    [
                        company_contracts_usage.company_name,
                        contract_group.comtract_group_id,
                        monthly_bucket.month,
                        monthly_bucket.licensed_count
                    ]
                )
    click.echo(tabulate(companies_contracts_usages_list, headers=["Company Name", "Contract Group ID", "Month", "Licensed Count"], tablefmt="fancy_grid"))
    click.echo("- End of Companies Contracts Usages -")

    # Get newly registered devices
    click.echo("- Getting newly registered devices within 1 day -")
    error, devices = mp_application.get_registered_devices_in_period('1d')
    if error is not None:
        raise click.ClickException(error)

    registered_devices_list = []
    for device in devices:
        registered_devices_list.append(
            [
                device.company.name,
                device.nra.ruleset_id,
                device.nra.certification_id,
                device.serial_number,
                device.license_id,
                device.contract.contract_group_id,
                device.contract.monthly_bucket
            ]
        )
    click.echo(tabulate(registered_devices_list,
                        headers=["Company Name", "Ruleset ID", "Certification ID", "Serial Number", "License ID", "Contract Group ID", "Monthly Bucket"],
                        tablefmt="fancy_grid"))
    click.echo("- End of newly registered devices -")

    # Get Query Call Stats
    click.echo("- Getting Query Call Stats within 1 day -")
    error, query_call_usages = mp_application.get_query_call_usages_in_period('1d')
    if error is not None:
        raise click.ClickException(error)

    query_call_usages_list = []
    for query_call_usage in query_call_usages:
        query_call_usages_list.append(
            [
                query_call_usage.company_name,
                query_call_usage.usages
            ]
        )
    click.echo(tabulate(query_call_usages_list,
                        headers=["Company Name", "Usages"],
                        tablefmt="fancy_grid"))
    click.echo("- End of Query Call Stats -")

    # Get Datadog End to End Status
    click.echo("- Getting End to End Status -")
    error, end_to_end_status = afc_service_status_application.get_end_to_end_status()
    if error is not None:
        raise click.ClickException(error)
    
    regions_status = end_to_end_status.regions_status
    for region in regions_status:
        click.echo(f"Region: {region.region}, Status: {region.status}")
    click.echo("- End of End to End Status -")
