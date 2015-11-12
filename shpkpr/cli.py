# stdlib imports
import os
import sys

# third-party imports
import click

# local imports
from shpkpr.marathon import MarathonClient
from shpkpr.mesos import MesosClient


CONTEXT_SETTINGS = dict(auto_envvar_prefix='SHPKPR')


class Context(object):

    def __init__(self):
        self.marathon_client = None

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class ShpkprCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('shpkpr.commands.cmd_' + name, None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ShpkprCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--marathon_url', required=True, help="URL of the Marathon API to use.")
@click.option('--mesos_master_url', required=True, help="URL of the Mesos master to use.")
@pass_context
def cli(ctx, mesos_master_url, marathon_url):
    """A tool to manage applications running on Marathon."""
    ctx.mesos_client = MesosClient(mesos_master_url)
    ctx.marathon_client = MarathonClient(marathon_url)
