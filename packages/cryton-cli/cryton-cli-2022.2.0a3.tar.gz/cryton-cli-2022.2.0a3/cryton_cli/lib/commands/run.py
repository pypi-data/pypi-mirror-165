import click
from typing import List, Optional

from cryton_cli.etc import config
from cryton_cli.lib.util import api, util


# Run
@click.group('runs')
@click.pass_obj
def run(_) -> None:
    """
    Manage Runs from here.

    \f
    :param _: Click ctx object
    :return: None
    """


@run.command('list')
@click.option('--less', is_flag=True, help='Show \'less\' like output.')
@click.option('-o', '--offset', type=click.INT, default=0, help='The initial index from which to return the results.')
@click.option('-l', '--limit', type=click.INT, default=20, help='Number of results to return per page.')
@click.option('--localize', is_flag=True, help='Convert UTC datetime to local timezone.')
@click.option('-f', '--filter', 'parameter_filters', type=click.STRING, multiple=True,
              help='Filter results using returned parameters (for example `id=1`, `name=test`, etc.).')
@click.pass_obj
def run_list(ctx: util.CliContext, less: bool, offset: int, limit: int, localize: bool, 
             parameter_filters: Optional[List[str]]) -> None:
    """
    List existing Runs in Cryton.

    \f
    :param ctx: Click ctx object
    :param less: Show less like output
    :param offset: Initial index from which to return the results
    :param limit: Number of results per page
    :param localize: If datetime variables should be converted to local timezone
    :param parameter_filters: Filter results using returned parameters (for example `id`, `name`, etc.)
    :return: None
    """
    results_filter = "&".join(parameter_filters)
    appendix = f'?limit={limit}&offset={offset}&{results_filter}'
    response = api.get_request(ctx.api_url, api.RUN_LIST + appendix)

    to_print = ['id', 'schedule_time', 'start_time', 'pause_time', 'finish_time', 'state', 'plan_model']
    util.echo_list(response, to_print, less, localize, ctx.debug)


@run.command('create')
@click.argument('plan_id', type=click.INT, required=True)
@click.argument('worker_ids', type=click.INT, nargs=-1, required=True)
@click.pass_obj
def run_create(ctx: util.CliContext, plan_id: int, worker_ids: list) -> None:
    """
    Create new Run with PLAN_ID and WORKER_IDS.

    PLAN_ID is ID of the Plan you want to create Run for. (for example 1)

    WORKER_IDS is list of IDs you want to use for Run. (1 2 3)

    \f
    :param ctx: Click ctx object
    :param plan_id: ID of the Plan that will be used in Run
    :param worker_ids: List of IDs you want to use for Run
    :return: None
    """
    arguments = {'plan_id': plan_id, 'worker_ids': worker_ids}
    response = api.post_request(ctx.api_url, api.RUN_CREATE, custom_dict=arguments)

    util.echo_msg(response, 'Run successfully created!', ctx.debug)


@run.command('show')
@click.argument('run_id', type=click.INT, required=True)
@click.option('--less', is_flag=True, help='Show less like output.')
@click.option('--localize', is_flag=True, help='Convert UTC datetime to local timezone.')
@click.pass_obj
def run_read(ctx: util.CliContext, run_id: int, less: bool, localize: bool) -> None:
    """
    Show Run with RUN_ID saved in Cryton.

    RUN_ID is ID of the Run you want to see.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :param less: Show less like output
    :param localize: If datetime variables should be converted to local timezone
    :return: None
    """
    response = api.get_request(ctx.api_url, api.RUN_READ, run_id)

    to_print = ['id', 'schedule_time', 'start_time', 'pause_time', 'finish_time', 'state', 'plan_model']
    util.echo_list(response, to_print, less, localize, ctx.debug)


@run.command('delete')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_delete(ctx: util.CliContext, run_id: int) -> None:
    """
    Delete Run with RUN_ID saved in Cryton.

    RUN_ID is ID of the Run you want to delete.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.delete_request(ctx.api_url, api.RUN_DELETE, run_id)

    util.echo_msg(response, 'Run successfully deleted!', ctx.debug)


@run.command('execute')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_execute(ctx: util.CliContext, run_id: int) -> None:
    """
    Execute Run saved in Cryton with RUN_ID.

    RUN_ID is ID of the Run you want to execute.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.post_request(ctx.api_url, api.RUN_EXECUTE, run_id)

    util.echo_msg(response, 'Run successfully executed!', ctx.debug)


@run.command('pause')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_pause(ctx: util.CliContext, run_id: int) -> None:
    """
    Pause Run saved in Cryton with RUN_ID.

    RUN_ID is ID of the Run you want to pause.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.post_request(ctx.api_url, api.RUN_PAUSE, run_id)

    util.echo_msg(response, 'Run successfully paused!', ctx.debug)


@run.command('postpone')
@click.argument('run_id', type=click.INT, required=True)
@click.argument('hours', type=click.INT, default=0)
@click.argument('minutes', type=click.INT, default=0)
@click.argument('seconds', type=click.INT, default=0)
@click.pass_obj
def run_postpone(ctx: util.CliContext, run_id: int, hours: int, minutes: int, seconds: int) -> None:
    """
    Postpone Run saved in Cryton with RUN_ID by HOURS, MINUTES and SECONDS.

    RUN_ID is ID of the Run you want to postpone.

    HOURS is number of hours.

    MINUTES is number of minutes.

    SECONDS is number of seconds.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :param hours: how many hours should be added to Run's start time
    :param minutes: how many hours should be added to Run's start time
    :param seconds: how many hours should be added to Run's start time
    :return: None
    """
    arguments = {'delta': "{}h{}m{}s".format(hours, minutes, seconds)}
    response = api.post_request(ctx.api_url, api.RUN_POSTPONE, run_id, arguments)

    util.echo_msg(response, 'Run successfully postponed!', ctx.debug)


@run.command('report')
@click.argument('run_id', type=click.INT, required=True)
@click.option('-f', '--file', type=click.Path(exists=True), default='/tmp',
              help='File to save the report to (default is /tmp).')
@click.option('--less', is_flag=True, help='Show less like output.')
@click.option('--localize', is_flag=True, help='Convert UTC datetime to local timezone.')
@click.pass_obj
def run_report(ctx: util.CliContext, run_id: int, file: str, less: bool, localize: bool) -> None:
    """
    Create report for Run with RUN_ID saved in Cryton.

    RUN_ID is ID of the Run you want to create report for.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :param file: File to save the report to (default is /tmp)
    :param less: Show less like output
    :param localize: If datetime variables should be converted to local timezone
    :return: None
    """
    response = api.get_request(ctx.api_url, api.RUN_REPORT, run_id)

    util.get_report(response, file, 'run_{}'.format(run_id), less, less, localize, ctx.debug)


@run.command('reschedule')
@click.argument('run_id', type=click.INT, required=True)
@click.argument('to_date', type=click.STRING, required=True)
@click.argument('to_time', type=click.STRING, required=True)
@click.option('--utc-timezone', is_flag=True, help='Input time in UTC timezone.')
@click.pass_obj
def run_reschedule(ctx: util.CliContext, run_id: int, to_date: str, to_time: str, utc_timezone: bool) -> None:
    """
    Reschedule Run saved in Cryton with RUN_ID to specified DATE and TIME.

    RUN_ID is ID of the Run you want to reschedule.

    DATE in format year-month-day (Y-m-d).

    TIME in format hours:minutes:seconds (H:M:S).

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :param to_date: to what date you want to reschedule Run
    :param to_time: to what time you want to reschedule Run
    :param utc_timezone: Use UTC timezone instead of local timezone
    :return: None
    """
    if utc_timezone:
        timezone = 'UTC'
    else:
        timezone = config.TIME_ZONE

    arguments = {'start_time': f"{to_date}T{to_time}Z", 'time_zone': timezone}
    response = api.post_request(ctx.api_url, api.RUN_RESCHEDULE, run_id, arguments)

    util.echo_msg(response, 'Run successfully rescheduled!', ctx.debug)


@run.command('schedule')
@click.argument('run_id', type=click.INT, required=True)
@click.argument('to_date', type=click.STRING, required=True)
@click.argument('to_time', type=click.STRING, required=True)
@click.option('--utc-timezone', is_flag=True, help='Input time in UTC timezone.')
@click.pass_obj
def run_schedule(ctx: util.CliContext, run_id: int, to_date: str, to_time: str, utc_timezone: bool) -> None:
    """
    Schedule Run saved in Cryton with RUN_ID to specified DATE and TIME.

    RUN_ID is ID of the Run you want to schedule.

    DATE in format year-month-day (Y-m-d).

    TIME in format hours:minutes:seconds (H:M:S).

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :param to_date: to what date you want to reschedule Run
    :param to_time: to what time you want to reschedule Run
    :param utc_timezone: Use UTC timezone instead of local timezone
    :return: None
    """
    if utc_timezone:
        timezone = 'UTC'
    else:
        timezone = config.TIME_ZONE

    arguments = {'start_time': f"{to_date}T{to_time}Z", 'time_zone': timezone}
    response = api.post_request(ctx.api_url, api.RUN_SCHEDULE, run_id, arguments)

    util.echo_msg(response, 'Run successfully scheduled!', ctx.debug)


@run.command('resume')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_unpause(ctx: util.CliContext, run_id: int) -> None:
    """
    Resume Run saved in Cryton with RUN_ID.

    RUN_ID is ID of the Run you want to resume.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.post_request(ctx.api_url, api.RUN_UNPAUSE, run_id)

    util.echo_msg(response, 'Run successfully resumed!', ctx.debug)


@run.command('unschedule')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_unschedule(ctx: util.CliContext, run_id: int) -> None:
    """
    Unschedule Run saved in Cryton with RUN_ID.

    RUN_ID is ID of the Run you want to unschedule.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.post_request(ctx.api_url, api.RUN_UNSCHEDULE, run_id)

    util.echo_msg(response, 'Run successfully unscheduled!', ctx.debug)


@run.command('kill')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_kill(ctx: util.CliContext, run_id: int) -> None:
    """
    Kill Run saved in Cryton with RUN_ID.

    RUN_ID is ID of the Run you want to kill.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.post_request(ctx.api_url, api.RUN_KILL, run_id)

    util.echo_msg(response, 'Run successfully killed!', ctx.debug)


@run.command('validate-modules')
@click.argument('run_id', type=click.INT, required=True)
@click.pass_obj
def run_validate_modules(ctx: util.CliContext, run_id: int) -> None:
    """
    Validate modules for Run with RUN_ID saved in Cryton.

    RUN_ID is ID of the Run you want to validate modules for.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :return: None
    """
    response = api.post_request(ctx.api_url, api.RUN_VALIDATE_MODULES, run_id)

    util.echo_msg(response, 'Modules were validated!', ctx.debug)


@run.command('get-plan')
@click.argument('run_id', type=click.INT, required=True)
@click.option('-f', '--file', type=click.Path(exists=True), default='/tmp',
              help='File to save the plan to (default is /tmp).')
@click.option('--less', is_flag=True, help='Show less like output.')
@click.option('--localize', is_flag=True, help='Convert UTC datetime to local timezone.')
@click.pass_obj
def run_get_plan(ctx: util.CliContext, run_id: int, file: str, less: bool, localize: bool) -> None:
    """
    Get plan from Run with RUN_ID saved in Cryton.

    RUN_ID is ID of the Run you want to get plan from.

    \f
    :param ctx: Click ctx object
    :param run_id: ID of the desired Run
    :param file: File to save the plan to (default is /tmp)
    :param less: Show less like output
    :param localize: If datetime variables should be converted to local timezone
    :return: None
    """
    response = api.get_request(ctx.api_url, api.RUN_GET_PLAN, run_id)

    util.get_report(response, file, 'run_{}'.format(run_id), less, less, localize, ctx.debug)
