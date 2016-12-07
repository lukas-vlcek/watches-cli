"""The base command."""


from datetime import datetime
from json import dumps
from elasticsearch import Elasticsearch


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        if self.options["--verbose"]:
            print 'Supplied options:', dumps(self.options, indent=2, sort_keys=True)

        user_kwargs = {}

        user_kwargs["hosts"] = options["--url"]

        if self.options["--sniff"]:
            # sniff before doing anything
            user_kwargs["sniff_on_start"] = True
            # refresh nodes after a node fails to respond
            user_kwargs["sniff_on_connection_fail"] = True
            # and also every 60 seconds
            user_kwargs["sniffer_timeout"] = 60

        # We can test just for --cacert because all the three options are required
        # if at least one of them is provided.
        if self.options["--cacert"]:
            user_kwargs["ca_certs"] = options["--cacert"]
            user_kwargs["client_cert"] = options["--cert"]
            user_kwargs["client_key"] = options["--key"]

        self.es = Elasticsearch(**user_kwargs)

    def run(self):
        # Not sure if this is the best way to convert localtime to UTC in ISO 8601 format
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = self.getData()
        if self.options["--timestamp"]:
            data['timestamp'] = ts

        print dumps(data, indent=2, sort_keys=False, default=lambda x:str(x))

    def getData(self):
        raise NotImplementedError('You must implement the run() method yourself!')
