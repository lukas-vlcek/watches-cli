"""Tests for our `watches cluster_health` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport
from watches.util import ESClientProducer


class TestClusterHealth(TestSecureSupport):
    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)


    def test_returns_cluster_health_with_sniffing(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--sniff'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 15)
        self.assertTrue('status' in o)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)

    def test_returns_cluster_health_with_verbose(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--verbose'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        self.assertTrue('Supplied options' in output)

    def test_returns_cluster_health_with_timestamp(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--timestamp'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        # Unless we index some data to cluster we can only check the indices field is present
        o = json.loads(output)
        self.assertTrue(len(o) == 16)
        self.assertTrue('timestamp' in o)

    def test_returns_cluster_health(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('number_of_nodes' in o)
        self.assertTrue('number_of_data_nodes' in o)
        self.assertTrue('active_primary_shards' in o)
        self.assertTrue('active_shards' in o)
        self.assertTrue('relocating_shards' in o)
        self.assertTrue('initializing_shards' in o)
        self.assertTrue('unassigned_shards' in o)
        # These are not found in object unless we explicitly use option
        self.assertTrue('indices' not in o)
        self.assertTrue('shards' not in o)
        self.assertTrue('timestamp' not in o)

    def test_returns_cluster_health_with_indices(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--level=indices'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('indices' in o)
        self.assertTrue('shards' not in o)

    def test_returns_cluster_health_with_shards(self):

        # Unless we index some data to cluster the output does not contain "shards" part
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'cluster_health', '--level=shards'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('indices' in o)
        self.assertTrue('shards' in o['indices']['i'])