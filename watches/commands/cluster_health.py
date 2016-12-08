"""The Cluster Health command."""


from .base import Base


class ClusterHealth(Base):
    """Get cluster health"""

    def getData(self):
        args = {
            'level': self.options['--level'],
            'local': self.options['--local'],
            'request_timeout': 1
        }
        self.check_filter_path(args)
        return self.es.cluster.health(**args)

