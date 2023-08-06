import click

from logging import basicConfig, getLogger, INFO

formatter = " %(asctime)s | %(levelname)-6s | %(process)d | %(threadName)-12s |" \
            " %(thread)-15d | %(name)-30s | %(filename)s:%(lineno)d | %(message)s |"
basicConfig(level=INFO, format=formatter)
logger = getLogger(__name__)


@click.command(help="Refreshes the Carbonara Agent. (required in case the pod is not running)")
def refresh():
    # Validate configuration complete
    # TODO: Better validation
    click.secho("Paid Tier", fg='yellow')
