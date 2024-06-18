import click
from tabulate import tabulate
from dependency_injector.wiring import Provide, inject

from infrastructure.dependency_injection.container import Container
from application.mp_application_implementation import MPApplicationImplementation
from application.system_health_application_implementation import SystemHealthApplicationImplementation
from application.scheduler_status_application_implementation import SchedulerStatusApplicationImplementation
from application.afc_service_status_application_implementation import AFCServiceStatusApplicationImplementation
from application.error_logs_application_implementation import ErrorLogsApplicationImplementation

@click.command(name='proactive-monitor', help="Execute Proactive Monitor")
@click.option('--excel-out', default=False, show_default=True, is_flag=True)
@inject
def proactive_monitor_command(excel_out: bool,
                              mp_application: MPApplicationImplementation = Provide[Container.mp_application],
                              afc_service_status_application: AFCServiceStatusApplicationImplementation = Provide[Container.afc_service_status_application],
                              system_health_application: SystemHealthApplicationImplementation = Provide[Container.system_health_application],
                              scheduler_status_application: SchedulerStatusApplicationImplementation = Provide[Container.scheduler_status_application],
                              error_logs_application: ErrorLogsApplicationImplementation = Provide[Container.error_logs_application]):
    # Get NRAs
    click.echo("- Getting NRAs -")
    error, nras = mp_application.get_nras()
    if error is not None:
        raise click.ClickException(error)

    nra_list = []
    for nra in nras:
        nra_list.append(
            [
                nra.ruleset_id,
                nra.certification_id,
                nra.is_authed
            ]
        )
    click.echo(tabulate(nra_list, headers=["Ruleset ID", "Certification ID", "Is Authed"], tablefmt="fancy_grid"))
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

    end_to_end_status_list = []
    regions_status = end_to_end_status.regions_status
    for region in regions_status:
        end_to_end_status_list.append(
            [
                region.region,
                region.status
            ]
        )
    click.echo(tabulate(end_to_end_status_list, headers=["Region", "Status"], tablefmt="fancy_grid"))
    click.echo("- End of End to End Status -")

    # Get System Health
    click.echo("- Getting System Health -")
    error, system_healths = system_health_application.get_system_health([], None)
    if error is not None:
        raise click.ClickException(error)

    system_health_list = []
    for system_health in system_healths:
        system_health_list.append(
            [
                system_health.name,
                system_health.status
            ]
        )
    click.echo(tabulate(system_health_list, headers=["System Name", "Status"], tablefmt="fancy_grid"))
    click.echo("- End of System Health -")

    # Get Datadog Error Logs
    click.echo("- Getting Datadog Error Logs -")
    error, error_logs = error_logs_application.get_error_logs()
    if error is not None:
        raise click.ClickException(error)

    error_logs_overall_list = []
    error_logs_overall_list.append([
        error_logs.error_logs_overall.total_pattern_count,
        error_logs.error_logs_overall.total_logs_count
    ])

    error_logs_list = []
    for error_log in error_logs.error_logs_pattern_counts:
        error_logs_list.append(
            [
                error_log.pattern,
                error_log.count
            ]  
        )
    click.echo(tabulate(error_logs_overall_list, headers=["Total Patterns", "Total Logs Count"], tablefmt="fancy_grid"))
    click.echo(tabulate(error_logs_list, headers=["Message", "Count"], tablefmt="fancy_grid", maxcolwidths=[80, None]))
    click.echo("- End of Datadog Error Logs -")
   
    # Get Scheduler Status
    click.echo("- Getting Scheduler Status -")
    error, scheduler_status = scheduler_status_application.get_scheduler_status([], None)
    if error is not None:
        raise click.ClickException(error)

    scheduler_status_list = []
    for scheduler in scheduler_status:
        scheduler_status_list.append(
            [
                scheduler.name,
                scheduler.status
            ]
        )
    click.echo(tabulate(scheduler_status_list, headers=["Scheduler Name", "Status"], tablefmt="fancy_grid"))
    click.echo("- End of Scheduler Status -")

    # Export Excel when enabled
    if excel_out:
        click.echo("- Exporting Excel -")
        # TODO Excel export logic
        click.echo("- End of Excel Export -")
