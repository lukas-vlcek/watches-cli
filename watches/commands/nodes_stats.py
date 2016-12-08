"""The Nodes Stats command."""


from .base import Base


class NodesStats(Base):
    """Get nodes stats"""

    def getData(self):
        args = {}
        self.check_filter_path(args)
        return self.es.nodes.stats(**args)