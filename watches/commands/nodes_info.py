"""The Nodes Info command."""


from .base import Base


class NodesInfo(Base):
    """Get nodes info"""

    def getData(self):
        args = {
            'node_id': self.options['--node_id']
        }
        self.check_filter_path(args)
        return self.es.nodes.info(**args)