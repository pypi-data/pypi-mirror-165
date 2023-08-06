import os


class EnvironmentConfig:
    """
    Base class for attribute-based config

    Config attributes must be defined as uppercase; on init, they are replaced with existing env values, if set
    Note: All replaceable values must be of string type
    """

    def __init__(self, prefix=''):
        """
        Load override values from OS environment variables
        :param prefix: optional variable prefix
        """
        for name in dir(self):
            if name.isupper():
                value = getattr(self, name)
                if not callable(value):
                    setattr(self, name, os.environ.get(prefix+name, value))