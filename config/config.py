import os
import pathlib

LOGGER_FORMAT = '%(levelname)s: %(message)s'
STR_ENCODING = 'utf-8'

ROOT_FOLDER = pathlib.Path(__file__).parent.parent
RESOURCES_FOLDER = os.path.join(ROOT_FOLDER, 'resources')

ERROR_PERMISSION_MSG = "You do not have permission to perform this action."

API_PAGE_SIZE = 300
API_DEFAULT_THROTTLE_RATES_ANON = '300/day'
API_DEFAULT_THROTTLE_RATES_USER = '30/minute'
