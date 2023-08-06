import click
import os
import requests

from cbrctl.utilities import get_carbonara_config_filepath, get_carbonara_config, create_context_file
from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


CARBONARA_AUTH_URL = os.environ.get("AUTH_URL", "https://5iwp5kybbk.execute-api.us-east-2.amazonaws.com/demo/generatetoken")


@click.command(help="Authorizes you for using Carbonara on your cluster.")
def auth():
    # Validate configuration complete
    # TODO: Better validation
    name = click.prompt('Please enter a valid name', type=str)
    email = click.prompt('Please enter a valid email', type=str)
    response = _post_request_with_json_body(name, email)
    if 'token' in response:
        carbonara_config = get_carbonara_config_filepath()
        config = get_carbonara_config(carbonara_config)
        current_context = config['contexts'][0]
        current_context['token'] = response['token']
        create_context_file(config)
        click.secho("Please persist your auth token: " + response['token'], fg='green')
        click.secho("Context Updated.", fg='blue')
    else:
        click.secho('Token generation failed. Please try again or contact support.', fg='red')
        raise click.Abort

def _post_request_with_json_body(username, useremail):
    # Cleaning json
    constructed_input = {
      "username": username,
      "useremail": useremail
    }
    logger.debug(f"Request Body: '{constructed_input}'")
    r = requests.post(CARBONARA_AUTH_URL, json=constructed_input)
    logger.debug(f"Status Code: {r.status_code}, Response: {r.json()}")
    if r.status_code / 100 == 2:
        return r.json()
    else:
        return {}
