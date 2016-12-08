"""The Cluster State command."""


from .base import Base


class ClusterState(Base):
    """Get cluster state"""

    def getData(self):
        args = {}
        self.check_filter_path(args)
        return self.es.cluster.state(**args)

