"""
watches

Usage:
  watches cluster_health [-i=INTERVAL -d=DURATION --url=URL -tsv] [--level=LEVEL --local]
  watches cluster_state  [-i=INTERVAL -d=DURATION --url=URL -tsv]
  watches cluster_stats  [-i=INTERVAL -d=DURATION --url=URL -tsv]
  watches nodes_stats    [-i=INTERVAL -d=DURATION --url=URL -tsv]
  watches nodes_info     [-i=INTERVAL -d=DURATION --url=URL -tsv] [--node_id=NODE_ID]
  watches indices_stats  [-i=INTERVAL -d=DURATION --url=URL -tsv] [--level=LEVEL --index=INDEX]
  watches -h
  watches --version

Options:
  -d=DURATION, --duration=DURATION   How long the watches should run in seconds. Use value '-1' to run forever. [default: 0].
  -i=INTERVAL, --interval=INTERVAL   Interval between data retrievals. Apply if 'duration' > 0. [default: 3].
  --url=URL           URL of ES node HTTP endpoint [default: http://localhost:9200].
  -t, --timestamp     Add timestamp field to data. The value is local datetime converted to UTC in ISO 8601 format.
  -s, --sniff         Turn on sniffing.
  -v, --verbose       Print more debug info: input options, ... etc.
  --level=LEVEL       Aggregation level of returned data, valid options: cluster, indices or shards. [default: cluster].
  --local             Return the local node information instead of master node.
  --node_id=NODE_ID   A comma-separated list of node IDs or names to limit the returned information; use `_local` to return information from local node you're connecting to [default: ].
  --index=INDEX       A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices.
  -h, --help          Show this screen.
  --version           Show version.

Examples:
  # Get cluster health from specified HTTP endpoint with added "timestamp" field in the response
  $ watches cluster_health --timestamp --url=http://127.0.0.1:9200

  # Get cluster health every 1 second, run forever until process is terminated
  $ watches cluster_health --interval=1 --duration=-1

  # Get cluster health every 1 second during next 10 seconds and use sniffing
  $ watches cluster_health --interval=1 --duration=10 --sniff

Help:
  For help using this tool, please open an issue on the GitHub repository:
  https://github.com/ViaQ/watches-cli
"""


from inspect import getmembers, isclass

from docopt import docopt
import time
import calendar

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)

            startsec = calendar.timegm(time.gmtime())
            duration = int(options['--duration'])
            interval = int(options['--interval'])
            endsec = (startsec + duration)

            while True:
                execute(command)
                if duration == 0:
                    break
                time.sleep(interval)
                actualsec = calendar.timegm(time.gmtime())
                # print duration, interval, startsec, actualsec, endsec
                if interval > -1 and actualsec >= endsec:
                    break

def execute(command):
    """
    Execute the command. If any exceptions occur they are caught and logged.
    :param command:
    :return:
    """
    try:
        command.run()
    except Exception, e:
        # TODO: this should go to a log
        print "Error executing command:", e
        pass

