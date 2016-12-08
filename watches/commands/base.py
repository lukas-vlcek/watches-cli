"""The base command."""


from datetime import datetime
from json import dumps
from watches.util import ESClientProducer


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        if self.options["--verbose"]:
            print 'Supplied options:', dumps(self.options, indent=2, sort_keys=True)

        self.es = ESClientProducer.create_client(self.options)

    def run(self):
        # Not sure if this is the best way to convert localtime to UTC in ISO 8601 format
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = self.getData()
        if self.options["--timestamp"]:
            data['timestamp'] = ts

        print dumps(data, indent=2, sort_keys=False, default=lambda x:str(x))

    def getData(self):
        raise NotImplementedError('You must implement the run() method yourself!')

    def check_filter_path(self, args):
        if self.options['--filter_path'] and self.options["--filter_path"] is not None and len(self.options["--filter_path"]) > 0:
            args.update({
                'filter_path': self.options['--filter_path']
            })
