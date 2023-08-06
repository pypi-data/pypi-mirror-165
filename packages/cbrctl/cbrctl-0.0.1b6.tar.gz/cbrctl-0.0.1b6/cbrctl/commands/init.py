import click
import shutil

from cbrctl.utilities import run_shell_command, create_context_file

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Initialize Carbonara context. "
                   "Validates dependent tools/packages.")
@click.option('--provider', '-p', default="aws", type=click.Choice(['aws', 'gcp', 'azure'], case_sensitive=False), prompt='Enter cloud to deploy to', help='Cloud Provider')
def init(provider):
    # checks if dependency exists
    # kubectl & helm
    if shutil.which('kubectl') is None or shutil.which('helm') is None:
        click.echo("Tools not available: {'kubectl', 'helm'}")
        raise click.Abort

    #TODO: Install Helm

    # Adding Helm repo for resource configuration:
    if ((run_shell_command("helm repo add prometheus-community https://prometheus-community.github.io/helm-charts") != 0) or
            (run_shell_command("helm repo update") != 0)):
        raise click.Abort

    # Create config file
    dict_data = {'kind': 'Config', 'contexts': [{'infrastructureComponent': provider}]}
    create_context_file(dict_data)
    click.secho("Context Initialized.", fg='blue')