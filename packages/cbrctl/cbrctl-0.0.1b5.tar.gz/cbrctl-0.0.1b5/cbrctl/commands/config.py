import click
import os
import random
import requests

from cbrctl.utilities import run_shell_command, get_carbonara_config_filepath, \
    validate_configuration, get_carbonara_config, get_carbonara_agent_manifest_filepath, \
        get_carbonara_server_persistent_filepath
from cbrctl.platforms.eks import EKS_CONFIG_ACTIONS
from cbrctl.platforms.quotes import CARBONARA_QUOTES
from kubernetes import config as kube_config

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


def _get_kube_current_context():
    # checks if kubectl current context is the passed cluster
    contexts, active_context = kube_config.list_kube_config_contexts()
    if not contexts:
        click.echo("Cannot find any context in kube-config file.")
        raise click.Abort
    # contexts = [context['name'] for context in contexts]
    # active_index = contexts.index(active_context['name'])
    # click.echo(active_index)
    kube_current_context = active_context['name']
    if '@' in kube_current_context:
        kube_current_context = kube_current_context.split('@')[1]
    kube_current_context = kube_current_context.split('.')[0]
    return kube_current_context

@click.command(help="Configures target cluster with Carbonara packages. "
                   "Validates if passed cluster is also the current kubectl context.")
@click.option('--cluster', '-c', prompt=f'Enter target cluster [Type: {_get_kube_current_context()}]', help='Target Cluster (current kubectl context).')
@click.option('--namespace', '-n', default="carbonara-monitoring", help='Target namespace for monitoring. (Default: carbonara-monitoring)')
@click.option('--token', '-t', default="default", help='Authorization Token for Carbonara Agent. (Default: read from context file)')
@click.option('--new-setup', '-s', default=True, is_flag=True, help='[Not-Available] Flag for using existing monitoring (Prometheus).')
def config(cluster, namespace, new_setup, token):
    # TODO: make sure of namespace parameter
    # checking if initialization succeeded:
    carbonara_config = get_carbonara_config_filepath()
    if not os.path.exists(carbonara_config):
        click.echo('Please initialize the context again.')
        raise click.Abort
    config = get_carbonara_config(carbonara_config)
    current_context = config['contexts'][0]
    cloud_provider = current_context['infrastructureComponent']
    if not token or token == "default":
        if 'token' in current_context:
            token = current_context['token']
        else:
            click.echo("Authorization Token not found.")
            raise click.Abort
    kube_current_context = _get_kube_current_context()
    if kube_current_context != cluster:
        click.echo("Current kubectl context doesn't match the passed one.")
        raise click.Abort
    _setup_cluster(namespace, cloud_provider, token)

def _setup_cluster(namespace, cloud_provider, auth_token):
    return _setup_cluster_eks(namespace, cloud_provider, auth_token)

def _setup_cluster_eks(namespace, cloud_provider, auth_token):

    #TODO: Optimize
    # download agent manifest to local path
    URL = "https://raw.githubusercontent.com/TryCarbonara/CarbonaraResources/main/carbonara-agent-manifest.yaml"
    response = requests.get(URL)
    agent_manifest_file = get_carbonara_agent_manifest_filepath()
    content = response.content.decode("utf-8")
    try:
        if '{{CLOUDPROVIDER}}' in content:
            content = content.replace('{{CLOUDPROVIDER}}', cloud_provider)
        if '{{TOKEN}}' in content:
            content = content.replace('{{TOKEN}}', auth_token)
        open(agent_manifest_file, "w").write(content)
        if not os.path.exists(agent_manifest_file):
            raise click.Abort
    except FileNotFoundError as ex:
        logger.debug(ex)

    #TODO: Optimize
    # download agent manifest to local path
    URL = "https://raw.githubusercontent.com/TryCarbonara/CarbonaraResources/main/server-persistent.yaml"
    response = requests.get(URL)
    server_manifest_file = get_carbonara_server_persistent_filepath()
    content = response.content.decode("utf-8")
    try:
        if '{{STORAGECLASSNAME}}' in content:
            if cloud_provider == "aws":
                content = content.replace('{{STORAGECLASSNAME}}', "gp2")
            elif cloud_provider == "azure":
                content = content.replace('{{STORAGECLASSNAME}}', "default")
            elif cloud_provider == "gcp":
                content = content.replace('{{STORAGECLASSNAME}}', "standard")
        open(server_manifest_file, "w").write(content)
        if not os.path.exists(server_manifest_file):
            raise click.Abort
    except FileNotFoundError as ex:
        logger.debug(ex)

    click.secho("Configuring cluster for monitoring ... (still running)", fg='blue', bold=True)
    with click.progressbar(EKS_CONFIG_ACTIONS, length=len(EKS_CONFIG_ACTIONS)) as bar:
        random_list = list(range(0, len(CARBONARA_QUOTES) - 1))
        for action in bar:
            random_number = random.choice(random_list)
            bar.label = CARBONARA_QUOTES[random_number] + "\n"
            bar.color = True
            if '{{AGENT_MANIFEST_FILE}}' in action:
                action = action.replace('{{AGENT_MANIFEST_FILE}}', agent_manifest_file)
            if '{{SERVER_MANIFEST_FILE}}' in action:
                action = action.replace('{{SERVER_MANIFEST_FILE}}', server_manifest_file)
            if (run_shell_command(action) != 0):
                raise click.Abort
            random_list.remove(random_number)

    click.secho("Validating the configured namespace.", fg='blue')

    # (Optional) Validate configuration ready
    validate_configuration()
    # Cleaning
    if os.path.exists(agent_manifest_file):
        os.remove(agent_manifest_file)
    if os.path.exists(server_manifest_file):
        os.remove(server_manifest_file)

    click.secho("You can use `cbrctl status` to view the configured resources.", fg='green')
    click.secho("Cluster Configured Successfully. Happy Carbonara \m/", fg='blue')