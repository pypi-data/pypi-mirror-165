import click

from cbrctl.utilities import run_shell_command_and_forget, validate_configuration, run_shell_command_with_response

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Forward one or more local ports to a Grafana pod. "
                   "Enables visualization with existing Carbonara dashboards. "
                   "Redirects to the default browser on the local machine.")
@click.option('--port', default=8080, type=int, help="Local Port form Grafana. (Default: 8080)")
def show(port):
    # Validate configuration complete
    # TODO: Better validation
    validate_configuration()
    if False: # port-forward # default
        click.launch(f'http://localhost:{port}')
        _port_forward_grafana(port)
    else: # load-balancer
        external_ip = _parse_external_ip()
        click.secho(f"Launching http://{external_ip} ...",  fg='blue')
        click.launch(f'http://{external_ip}')


def _port_forward_grafana(local_port_no):
    # Port-forward to Grafana
    run_shell_command_and_forget(
        f"kubectl port-forward --namespace carbonara-monitoring svc/prometheus-grafana {local_port_no}:80")

def _parse_external_ip():
    # Extract Eternal Ip
    returncode, stdout, stderr = run_shell_command_with_response(
        "kubectl get service/prometheus-grafana -n carbonara-monitoring --output jsonpath='{.status.loadBalancer.ingress[0].ip}'")
    if (returncode != 0 or stdout == ""):
        click.secho(f"If running `kubectl get service/prometheus-grafana -n carbonara-monitoring` doesn't provide expected result, configure the cluster again. \n {stderr}", fg='green')
        raise click.Abort
    return stdout.decode('UTF-8')