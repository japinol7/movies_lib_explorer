import os

from collections import namedtuple
from config.aws.modules.aws.ssm_client import SSMParamClient

ConfigVars = namedtuple('config_vars', ['environ', 'ssm'])
CONFIG_VARS = {
    'mlme_dj_secret_key': ConfigVars('MLME_DJ_SECRET_KEY', 'mlme-dj-secret-key'),
    'mlme_dj_allowed_hosts': ConfigVars('MLME_DJ_ALLOWED_HOSTS', 'mlme-dj-allowed-hosts'),
    }


class ConfigParser:
    """Represents a configuration parser.
    Loads variables from the environment when available; otherwise it loads them from SSM.
    """

    def __init__(self):
        self._config = {}
        ssm = SSMParamClient()
        for cv, vals in CONFIG_VARS.items():
            self._config.update({
                    cv: os.environ.get(vals.environ) or ssm.get(vals.ssm)
                    })

    def __getitem__(self, item):
        return self._config[item]

    def get(self, item, default=None):
        return self.__getitem__(item) or default
