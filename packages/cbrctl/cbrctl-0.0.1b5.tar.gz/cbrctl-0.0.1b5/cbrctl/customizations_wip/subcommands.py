import os
import webbrowser
import yaml

from kubernetes import config
from cbrctl.customizations_wip.commands import BasicCommand
from cbrctl.utilities import run_shell_command

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


class InitCommand(BasicCommand):
    NAME = 'init'
    DESCRIPTION = ("Initialize Carbonara context. "
                   "Validates dependent tools/packages. ")
    USAGE = "NONE"
    ARG_TABLE = [{'name': 'provider', 'nargs': 1, 'type': 'string', 'default': 'AWS', 'synopsis': USAGE}]
    # TODO: Add support for adding Filters for Carbonara Agent and pass by ENV

    def _run_main(self, parsed_args, parsed_globals):
        # checks if dependency exists
        # kubectl & helm
        if not self._is_tool('kubectl') and not self._is_tool('helm'):
            return 1
        provider_info = 'AWS'
        self._create_context_file(provider_info)

        # Adding Helm repo for resource configuration:
        if (run_shell_command("helm repo add prometheus-community https://prometheus-community.github.io/helm-charts") or
            run_shell_command("helm repo update")) != 0:
            return 1


    def _create_context_file(self, provider_info):
        pwd = os.path.expanduser('~')
        kube_dir = os.path.join(pwd, '.kube')
        os.mkdir(kube_dir)

        dict_file = {'kind': 'Config', 'contexts' : [{'infrastructureComponent' : provider_info}]}

        # create file
        with open(os.path.join(kube_dir, 'carbonara_config'), 'w') as file:
            documents = yaml.dump(dict_file, file)


class ConfigCommand(BasicCommand):
    NAME = 'config'
    DESCRIPTION = ("Configures target cluster with Carbonara packages. "
                   "Validates if passed cluster is also the current kubectl context. ")
    USAGE = "NONE"
    ARG_TABLE = [{'name': 'cluster', 'nargs': 1, 'type': 'string', 'synopsis': USAGE}]

    def _run_main(self, parsed_args, parsed_globals):
        # checks if kubectl current context is the passed cluster
        passed_cluster = ''
        contexts, active_context = config.list_kube_config_contexts()
        if not contexts:
            print("Cannot find any context in kube-config file.")
            return 1
        contexts = [context['name'] for context in contexts]
        active_index = contexts.index(active_context['name'])

    def _setup_cluster(self):
        return self._setup_cluster_eks()

    def _setup_cluster_eks(self):
        logger.info("Configuring cluster for monitoring ...")

        # Install kubernetes Prometheus monitoring stack
        if run_shell_command("helm upgrade -i prometheus \
        prometheus-community/kube-prometheus-stack \
        --namespace carbonara-monitoring \
        --create-namespace") != 0:
            return 1

        # Install prometheus pushgateway service
        if run_shell_command("helm upgrade -i prometheus-pushgateway prometheus-community/prometheus-pushgateway \
        --namespace carbonara-monitoring \
        --set serviceMonitor.enabled=true \
        --set serviceMonitor.namespace=carbonara-monitoring \
        --set persistentVolume.enabled=true \
        --set additionalLabels={release:prometheus} \
        --create-namespace") != 0:
            return 1

        # Add Grafana Dashboard
        if run_shell_command("kubectl apply -f https://gist.githubusercontent.com/saurabh-carbonara/4b73003e371154cca23ad11a99550660/raw/c1dabcafc1d67b81f0312d4901854a8afffbc376/grafana-dashboard-kubectl.yaml -n carbonara-monitoring") != 0:
            return 1

        # Configure Carbonara Agent
        # TODO: read the provider_info from context and apply to the POD below
        if run_shell_command("kubectl apply -f https://gist.githubusercontent.com/saurabh-carbonara/64b0e14b71cd4ae5fe3bc3333baa255b/raw/ --namespace carbonara-monitoring") != 0:
            return 1

        logger.info("Validating the configured namespace")

        # (Optional) Validate configuration ready
        if (run_shell_command("kubectl --namespace carbonara-monitoring get pods -l 'release=prometheus'") or
            run_shell_command("kubectl --namespace carbonara-monitoring get pods -l 'release=prometheus-pushgateway'")) != 0:
            return 1


class ShowCommand(BasicCommand):
    NAME = 'show'
    DESCRIPTION = ("Forward one or more local ports to a Grafana pod. "
                   "Enables visualization with existing Carbonara dashboards. "
                   "Redirects to the default browser on the local machine. ")
    USAGE = "NONE"
    ARG_TABLE = [{'name': 'port', 'nargs': '?', 'type': 'integer', 'default': '8080', 'synopsis': USAGE}]

    def _run_main(self, parsed_args, parsed_globals):
        port = 8080
        self._port_forward_grafana(port)
        webbrowser.open(f'http://localhost:{port}')

    def _port_forward_grafana(self, local_port_no):
        # Port-forward to Grafana
        run_shell_command(f"kubectl port-forward --namespace carbonara-monitoring svc/prometheus-grafana {local_port_no}:80", wait=False)

class ListCommand(BasicCommand):
    pass
