import click
from cbrctl.utilities import validate_configuration, run_shell_command

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Current Status. (lists all resources created by Carbonara)")
def status():
    # Validate configuration complete
    # TODO: Better validation
    validate_configuration()
    run_shell_command("kubectl get all --namespace carbonara-monitoring", print=True)
