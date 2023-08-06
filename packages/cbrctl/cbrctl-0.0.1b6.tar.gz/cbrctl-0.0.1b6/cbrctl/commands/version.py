import click
from cbrctl import __version__
from cbrctl.utilities import run_shell_command_with_response

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Version Info.")
def version():
    user_agent_name = 'cbrctl'
    user_agent_version = __version__
    kubectl_version = _kubectl_version().decode("utf-8")
    helm_version = _helm_version().decode("utf-8")
    click.echo(f'{user_agent_name} Version: {user_agent_version} \nkubectl: \n{kubectl_version if len(kubectl_version) > 0 else "Unavailable"}helm: \n{helm_version if len(helm_version) > 0 else "Unavailable"}')

def _kubectl_version():
    returncode, stdout, stderr = run_shell_command_with_response("kubectl version")
    if returncode != 0:
        click.echo(stderr)
    return stdout

def _helm_version():
    returncode, stdout, stderr =  run_shell_command_with_response("helm version")
    if returncode != 0:
        click.echo(stderr)
    return stdout
