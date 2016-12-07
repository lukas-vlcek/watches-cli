"""Provider of Elasticsearch client."""

from elasticsearch import Elasticsearch

def create_client(options):
    """Produces a new Elasticsearch client according to provided options."""

    user_kwargs = {}

    if "--url" in options:
        user_kwargs.update({
            'hosts': options["--url"]
        })

    # "true" is not translated to native True value ?
    if "--sniff" in options and "true" == options["--sniff"]:
        user_kwargs.update({
            # sniff before doing anything
            "sniff_on_start": True,
            # refresh nodes after a node fails to respond
            "sniff_on_connection_fail": True,
            # and also every 60 seconds
            "sniffer_timeout": 60
        })

    # We can test just for --cacert because all the three options are required
    # if at least one of them is provided.
    if "--cacert" in options and options["--cacert"] is not None and len(options["--cacert"]) > 0:
        user_kwargs.update({
            "ca_certs": options["--cacert"],
            "client_cert": options["--cert"],
            "client_key": options["--key"]
        })

    es = Elasticsearch(**user_kwargs)

    return es