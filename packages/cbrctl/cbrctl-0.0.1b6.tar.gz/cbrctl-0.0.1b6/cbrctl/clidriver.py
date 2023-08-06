import click

from cbrctl.commands import init, config, show, version, status, refresh, eject, auth
from kubernetes import config as kube_config


@click.group(help="CLI tool to manage carbonara context of projects")
def main():
    driver = create_clidriver()
    rc = driver.main()
    return rc

# Adding commands logic
main.add_command(init.init)
main.add_command(config.config)
main.add_command(show.show)
main.add_command(version.version)
main.add_command(status.status)
main.add_command(eject.eject)
main.add_command(refresh.refresh)
main.add_command(auth.auth)

def create_clidriver():
    # define session
    driver = CLIDriver()
    return driver


class CLIDriver(object):

    def __init__(self):
        try:
            kube_config.load_incluster_config()
        except kube_config.ConfigException:
            try:
                kube_config.load_kube_config()
            except kube_config.ConfigException:
                click.echo("Err: Could not configure kubernetes python client", color=True)
                raise click.Abort

    def main(self, args=None):
        """
        """
        # if args is None:
        #     args = sys.argv[1:]
        #
        return 0