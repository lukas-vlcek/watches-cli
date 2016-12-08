"""The Cluster Stats command."""


from .base import Base


class ClusterStats(Base):
    """Get cluster stats"""

    def getData(self):
        args = {}
        self.check_filter_path(args)
        return self.es.cluster.stats(**args)

