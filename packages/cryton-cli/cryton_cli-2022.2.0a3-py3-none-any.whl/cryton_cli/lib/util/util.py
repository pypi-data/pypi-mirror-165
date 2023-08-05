import jinja2
import os
import configparser
from datetime import datetime
import yaml
import string
import random
import json
from typing import Tuple, List, Union, Optional
import pytz
import click
import requests

from cryton_cli.etc import config
from cryton_cli.lib.util import api, constants as co


def fill_template(template_path: str, inventory_paths: tuple) -> str:
    """
    Fill the missing values in the yaml with variables
    :param template_path: path to the template
    :param inventory_paths: list of paths to the inventories containing the variables to fill the template
    :return: filled json or yaml plan
    """
    path, filename = os.path.split(os.path.abspath(template_path))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

    conf = dict()
    for inventory in inventory_paths:
        to_update = read_config(inventory)
        if to_update is not None:
            conf.update(read_config(inventory))

    template = env.get_template(filename)
    filled_template = template.render(conf)

    return filled_template


def read_config(inventory_path: str) -> dict:
    """
    Reads inventory file and returns it as a dictionary
    :param inventory_path: path to the inventory file
    :return: dict containing the inventory
    """
    # JSON
    try:
        with open(inventory_path) as json_file:
            conf_dict = json.load(json_file)
            return conf_dict
    except json.decoder.JSONDecodeError:
        pass
    # YAML
    try:
        with open(inventory_path) as yaml_file:
            conf_dict = yaml.safe_load(yaml_file)
            return conf_dict
    except yaml.YAMLError:
        pass
    # INI
    try:
        config_parser = configparser.ConfigParser()
        config_parser.read(inventory_path)
        conf_dict = {section: dict(config_parser.items(section)) for section in config_parser.sections()}
        return conf_dict
    except configparser.Error:
        pass

    raise ValueError("Invalid inventory file provided: {}.".format(inventory_path))


def get_yaml_from_file(file: str, inventory_paths: tuple = None) -> dict:
    """
    Parse json/yaml file and optionally fill it with values
    :param file: File (template) containing the plan
    :param inventory_paths: list of paths to the inventories containing the variables to fill the template
    :return: yaml from the file, optionally filled with values
    """
    if inventory_paths is not None:
        plan_yaml = yaml.safe_load(fill_template(file, inventory_paths))
    else:
        with open(file, 'r') as plan_file:
            plan_yaml = yaml.safe_load(plan_file)

    return plan_yaml


def save_report_to_file(report: dict, file_name: str, file_details: str = '') -> Tuple[int, str]:
    """
    Save report into file
    :param file_name: Where to save the report (default is /tmp)
    :param report: What should be saved to report
    :param file_details: What should be added to the file name (only if path is /tmp)
    :return: tuple(0 as OK/-1 as FAIL, string defining err message or file location)
    """
    if file_name == '/tmp':
        time_stamp = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"))
        file_tail = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=5))
        file_name = '/tmp/report_{}_{}_{}'.format(file_details, time_stamp, file_tail)

    try:
        with open(file_name, 'w+') as report_file:
            yaml.dump(report, report_file, sort_keys=False)
    except IOError as e:
        return -1, 'Cannot access file path {}. Original exception: {}'.format(file_name, e)

    return 0, file_name


def convert_from_utc(utc_str: str) -> datetime:
    """
    Convert datetime in UTC timezone to specified timezone
    :param utc_str: datetime in UTC timezone to convert
    :return: datetime with the specified timezone
    """
    try:
        utc_datetime = datetime.strptime(utc_str, co.TIME_FORMAT)
    except ValueError:
        utc_datetime = datetime.strptime(utc_str, co.TIME_DETAILED_FORMAT)

    if not utc_datetime.tzinfo:
        utc_datetime = pytz.utc.localize(utc_datetime, is_dst=None)
    new_datetime = utc_datetime.astimezone(pytz.timezone(config.TIME_ZONE))

    return new_datetime.replace(tzinfo=None)


class CliContext(object):
    """
    Context object for CLI. Contains necessary data for link creation.
    """
    def __init__(self, host: Optional[str], port: Optional[int], ssl: bool, debug: bool):
        if host is None:
            host = config.API_HOST
        if port is None:
            port = config.API_PORT
        if config.API_SSL and not ssl:
            ssl = True
        self.api_url = api.create_rest_api_url(host, port, ssl)
        self.debug = debug


def get_response_data(response: requests.Response) -> Union[str, dict]:
    """
    Parse response's data.
    :param response: Response containing data from REST API
    :return: Parsed data
    """
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        if response.ok:
            response_data = 'Couldn\'t parse response details.'
        else:
            response_data = 'Couldn\'t parse response details. Object with ID you specified probably doesn\'t exist.'

    return response_data


def get_detailed_message(data: Union[str, dict]) -> Union[str, dict]:
    """
    Get the most detailed message for the best readability.
    :param data: Data to be parsed
    :return: Readable message for user
    """
    if isinstance(data, dict):
        if data.get('results') is not None:
            detailed_msg = data.get('results')
        elif data.get('detail') is not None and len(data) == 1:
            detailed_msg = data.get('detail')
        else:
            detailed_msg = data

    else:
        detailed_msg = data

    return detailed_msg


def echo_msg(response: Union[str, requests.Response], ok_message: str = 'Success!', debug: bool = False) -> None:
    """
    Echo message containing information about success or failure of user's request.
    :param response: Response containing data from REST API
    :param ok_message: Custom message for user in case of success
    :param debug: Show non formatted raw output
    :return: None
    """
    if isinstance(response, str):
        click.echo("{} ({}).".format(click.style('Something went wrong :/', fg='red'), response))
        return

    if debug:
        detailed_msg = response.text
        click.echo(detailed_msg)

    else:
        response_data = get_response_data(response)
        detailed_msg = get_detailed_message(response_data)

        if response.ok:
            click.echo("{} ({}).".format(click.style(ok_message, fg='green'), detailed_msg))
        else:
            err_message = 'Something went wrong :/'
            click.echo("{} ({}: {}).".format(click.style(err_message, fg='red'), response.reason, detailed_msg))


def parse_line_from_dict(line: dict, to_print: List[str], localize: bool) -> str:
    """
    Filter dictionary values and optionally update timezone.
    :param line: dictionary that should be parsed
    :param to_print: Keys to be shown (printed out)
    :param localize: If datetime variables should be converted to local timezone
    :return: Filtered and localized string
    """
    line_to_print = ""
    datetime_variables = ['finish_time', 'pause_time', 'start_time', 'created_at', 'updated_at', 'schedule_time']

    for key in to_print:
        value = line.get(key)

        if localize and value is not None and key in datetime_variables:
            value = convert_from_utc(value)

        if line_to_print != "":
            line_to_print += ", "
        line_to_print += "{}: {}".format(key, value)

    return line_to_print


def echo_list(response: Union[str, requests.Response], to_print: List[str], less: bool = False,
              localize: bool = False, debug: bool = False) -> None:
    """
    Remove ignored parameters and echo the rest.
    :param response: Response containing data from REST API
    :param to_print: Parameters to be shown (printed out)
    :param less: Show less like output
    :param localize: If datetime variables should be converted to local timezone
    :param debug: Show non formatted raw output
    :return: None
    """
    if isinstance(response, str):
        click.echo("{} ({}).".format(click.style('Something went wrong :/', fg='red'), response))
        return

    if debug:
        detailed_msg = response.text

    else:
        response_data = get_response_data(response)
        detailed_msg = get_detailed_message(response_data)

    if response.ok:
        if debug:
            click.echo(detailed_msg)
            return

        if not isinstance(detailed_msg, list):
            detailed_msg = [detailed_msg]

        length = len(detailed_msg)
        data_to_print = []
        for i in range(length):
            line = parse_line_from_dict(detailed_msg[i], to_print, localize)
            if length != 0 and i < length - 1:
                line += "\n\n"

            data_to_print.append(line)

        if less:
            click.echo_via_pager(data_to_print)
        else:
            if data_to_print is None or data_to_print == []:
                click.echo("{}".format(click.style('Empty response...', fg='green')))
            else:
                for line in data_to_print:
                    click.echo(line)

    else:
        err_message = 'Something went wrong :/'
        click.echo("{} ({}: {}).".format(click.style(err_message, fg='red'), response.reason, detailed_msg))


def update_report(iterable: dict, localize: bool):
    datetime_variables = ['finish_time', 'pause_time', 'start_time', 'created_at', 'updated_at', 'schedule_time']
    for key, value in iterable.items():
        if isinstance(value, dict):
            update_report(value, localize)
        elif isinstance(value, list):
            for inst in value:
                update_report(inst, localize)
        else:
            update = False
            if localize and value is not None and key in datetime_variables:
                value = convert_from_utc(value)
                update = True

            if update:
                iterable.update({key: value})


def get_report(response: Union[str, requests.Response], file_path: str, file_details: str, echo_only: bool = False,
               less: bool = False, localize: bool = False, debug: bool = False) -> None:
    """
    Get report and echo the result.
    :param response: Response containing data from REST API
    :param file_path: Where to save the report
    :param file_details: What should be added to the file name (only if path is /tmp)
    :param echo_only: If the report should be only printed out and not saved
    :param less: Show less like output
    :param debug: Show non formatted raw output
    :param localize: If datetime variables should be converted to local timezone
    :return: None
    """
    if isinstance(response, str):
        click.echo("{} ({}).".format(click.style('Something went wrong :/', fg='red'), response))
        return

    if debug:
        detailed_msg = response.text
    else:
        response_data = get_response_data(response)
        detailed_msg = get_detailed_message(response_data)

    if response.ok:
        if not debug:
            detailed_msg = detailed_msg
            if localize:  # if there are more things to update, add them here and pass them to update_report..
                update_report(detailed_msg, localize)
        if not echo_only:
            saved = save_report_to_file(detailed_msg, file_path, file_details)
            if saved[0] == 0:
                click.echo('{} ({}: {})'.format(click.style('Successfully created report!', fg='green'),
                                                'file saved at', saved[1]))
            else:
                click.echo('{} ({}: {})'.format(click.style('Something went wrong :/', fg='red'), 'details', saved[1]))

        else:
            if less:
                if debug:
                    click.echo_via_pager(detailed_msg)
                else:
                    click.echo_via_pager(yaml.dump(detailed_msg, sort_keys=False))
            else:
                if debug:
                    click.echo(detailed_msg)
                else:
                    click.echo(yaml.dump(detailed_msg, sort_keys=False))

    else:
        err_message = 'Something went wrong :/'
        click.echo("{} ({}: {}).".format(click.style(err_message, fg='red'), response.reason, detailed_msg))


def render_documentation(raw_documentation: dict, layer: int) -> str:
    """
    Process and create documentation in markdown.
    :param raw_documentation: Unprocessed documentation
    :param layer: Header level
    :return: Documentation in Markdown
    """
    doc = f"{'#' * layer} {raw_documentation.get('name')}\n"
    doc += raw_documentation.get('help')

    # Prepare arguments and options
    arguments, options = [], []
    for parameter in raw_documentation.get('params'):
        arguments.append(parameter) if 'argument' in parameter.get('param_type_name') else options.append(parameter)

    # Generate arguments for command
    if arguments:
        doc += '**Arguments:**  \n'
        for argument in arguments:
            doc += f"- {argument.get('name').upper()}  \n"

    # Generate options for command
    doc += '\n**Options:**  \n'
    for option in options:
        opts = option.get('opts')
        parsed_opts = f'`{opts[0]}`, `{opts[1]}`' if len(opts) != 1 else f'`{opts[0]}`'
        doc += f"- {option.get('name')} ({parsed_opts}) - {option.get('help')}  \n"

    doc += '\n'
    # Generate documentation for sub commands
    if raw_documentation.get('commands') is not None:
        for cmd_detail in raw_documentation.get('commands').values():
            doc += render_documentation(cmd_detail, layer + 1)

    return doc


def clean_up_documentation(documentation: str) -> str:
    """
    Remove forbidden characters from documentation.
    :param documentation: Human readable documentation
    :return: Clean documentation
    """
    return documentation.replace('_', r'\_')
