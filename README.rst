Watch Elasticsearch CLI
=======================

A CLI tool that can be used to watch Elasticsearch cluster.
*This work is under development.*

Build status
------------

.. image:: https://secure.travis-ci.org/ViaQ/watches-cli.png
   :target: http://travis-ci.org/#!/ViaQ/watches-cli

Synopsis
--------

The tool uses `docopt <http://docopt.org/>`_ to describe command line language and supports the following options::

    Usage:
      watches cluster_health [-i=INTERVAL -d=DURATION --url=URL -tsv] [(--cacert=CACERT --cert=CERT --key=KEY)] [-f=FILTER...] [--level=LEVEL --local]
      watches cluster_state  [-i=INTERVAL -d=DURATION --url=URL -tsv] [(--cacert=CACERT --cert=CERT --key=KEY)] [-f=FILTER...]
      watches cluster_stats  [-i=INTERVAL -d=DURATION --url=URL -tsv] [(--cacert=CACERT --cert=CERT --key=KEY)] [-f=FILTER...]
      watches nodes_stats    [-i=INTERVAL -d=DURATION --url=URL -tsv] [(--cacert=CACERT --cert=CERT --key=KEY)] [-f=FILTER...]
      watches nodes_info     [-i=INTERVAL -d=DURATION --url=URL -tsv] [(--cacert=CACERT --cert=CERT --key=KEY)] [-f=FILTER...] [--node_id=NODE_ID]
      watches indices_stats  [-i=INTERVAL -d=DURATION --url=URL -tsv] [(--cacert=CACERT --cert=CERT --key=KEY)] [-f=FILTER...] [--level=LEVEL --index=INDEX]
      watches -h
      watches --version

    Options:
      -d=DURATION, --duration=DURATION   How long the watches should run in seconds. Use value '-1' to run forever. [default: 0].
      -i=INTERVAL, --interval=INTERVAL   Interval between data retrievals. Apply if 'duration' > 0. [default: 3].
      --url=URL           URL of ES node HTTP endpoint [default: http://localhost:9200].
      -t, --timestamp     Add timestamp field to data. The value is local datetime converted to UTC in ISO 8601 format.
      -s, --sniff         Turn on sniffing.
      -v, --verbose       Print more debug info: input options, ... etc.
      -f=FILTER, --filter_path=FILTER   Filter returned JSON (see http://elasticsearch-py.readthedocs.io/en/master/api.html#response-filtering)
      --cacert=CACERT     Path to Certification Authority Certificate pem file
      --cert=CERT         Path to Client Certificate pem file
      --key=KEY           Path to Client Key pem file
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

      # Alternatively, using short option notation
      $ watches cluster_health -i 1 -d 10 -s

      # Get cluster health from secured node
      $ watches cluster_health \
          --url=https://localhots:9200 \
          --cacert /tmp/search-guard-ssl/example-pki-scripts/ca/chain-ca.pem \
          --cert /tmp/search-guard-ssl/example-pki-scripts/kirk.crt.pem \
          --key /tmp/search-guard-ssl/example-pki-scripts/kirk.key.pem

      # Filter cluster health for status fields
      $ watches cluster_health --level=shards -f status -f indices.*.status -f indices.*.shards.*.status

To connect to Elasticsearch cluster ``watches`` uses official
`elasticsearch-py <https://github.com/elastic/elasticsearch-py/>`_ client which
can use `Sniffing <http://elasticsearch-py.readthedocs.io/en/master/index.html#sniffing>`_.
It is recommended to use ``--sniff`` option (see above) to enable sniffing for long running tasks.

Install, Test and Release
-------------------------

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Read `Testing.md <./tests/Testing.md>`_ to learn more details.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!

Credits
-------

Built on top of `skele-cli <https://github.com/rdegges/skele-cli.git>`_ skeleton, read
`skele-cli blog post <https://stormpath.com/blog/building-simple-cli-interfaces-in-python>`_
to learn more.


License
-------

Watches CLI is licensed under the `Apache License, Version 2.0 <http://www.apache.org/licenses/>`_.