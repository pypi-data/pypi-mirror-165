from os import getenv, path
from tzlocal import get_localzone_name
from dotenv import load_dotenv


APP_DIRECTORY = getenv('CRYTON_CLI_APP_DIRECTORY', path.expanduser("~/.local/cryton-cli/"))

load_dotenv(path.join(APP_DIRECTORY, ".env"))

TIME_ZONE = getenv('CRYTON_CLI_TIME_ZONE')
if TIME_ZONE is None or TIME_ZONE.lower() == 'auto':
    TIME_ZONE = get_localzone_name()

API_HOST = getenv('CRYTON_CLI_API_HOST')
API_PORT = getenv('CRYTON_CLI_API_PORT')
API_SSL = True if getenv('CRYTON_CLI_API_SSL').lower() == 'true' else False
API_ROOT = getenv('CRYTON_CLI_API_ROOT')
