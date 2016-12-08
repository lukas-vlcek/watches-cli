"""The Indices Stats command."""


from .base import Base


class IndicesStats(Base):
    """Get indices stats"""

    def getData(self):
        args = {
            'index': self.options['--index'],
            'level': self.options['--level']
        }
        self.check_filter_path(args)
        return self.es.indices.stats(**args)