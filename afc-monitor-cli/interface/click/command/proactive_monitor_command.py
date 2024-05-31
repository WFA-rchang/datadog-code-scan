import click
from tabulate import tabulate
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
    error, devices = mp_application.get_registered_devices_in_period('2d')
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
                device.license_id
            ]
        )
    click.echo(tabulate(registered_devices_list, headers=["Company Name", "Ruleset ID", "Certification ID", "Serial Number", "License ID"], tablefmt="fancy_grid"))
    click.echo("- End of newly registered devices -")
