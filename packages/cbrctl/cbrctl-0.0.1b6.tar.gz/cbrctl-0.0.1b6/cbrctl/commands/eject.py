import click
import os
import requests

from cbrctl.platforms.eks import EKS_DECONFIG_ACTIONS
from cbrctl.utilities import run_shell_command, get_carbonara_agent_manifest_filepath

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Uninstalls resources configured by Carbonara")
@click.option('-y', default=True, is_flag=True, prompt='Are you sure?', help='Confirmation')
def eject(y):
    if y == True:
        # TODO: Optimize
        # download agent manifest to local path
        URL = "https://raw.githubusercontent.com/TryCarbonara/CarbonaraResources/main/carbonara-agent-manifest.yaml"
        response = requests.get(URL)
        agent_manifest_file = get_carbonara_agent_manifest_filepath()
        content = response.content.decode("utf-8")
        try:
            if '{{CLOUDPROVIDER}}' in content:
                content = content.replace('{{CLOUDPROVIDER}}', "CLOUDPROVIDER")
            if '{{TOKEN}}' in content:
                content = content.replace('{{TOKEN}}', "TOKEN")
            open(agent_manifest_file, "w").write(content)
            if not os.path.exists(agent_manifest_file):
                raise click.Abort
        except FileNotFoundError as ex:
            logger.debug(ex)

        click.secho("Removing Carbonara resources...", fg='blue', bold=True)
        with click.progressbar(EKS_DECONFIG_ACTIONS) as bar:
            for action in bar:
                if '{{MANIFEST_FILE}}' in action:
                    action = action.replace('{{MANIFEST_FILE}}', agent_manifest_file)
                if (run_shell_command(action) != 0):
                    raise click.Abort
        # Cleaning
        if os.path.exists(agent_manifest_file):
            os.remove(agent_manifest_file)
        click.secho("Cluster Cleaned Successfully. Happy Carbonara \m/", fg='blue')
    else:
        click.echo('Aborted!')