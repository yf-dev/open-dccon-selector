import base64
import os
from datetime import timedelta

TWITCH_EXTENSION_SECRET = base64.b64decode(os.environ['TWITCH_EXTENSION_SECRET'])
TWITCH_EXTENSION_CLIENT_ID = os.environ['TWITCH_EXTENSION_CLIENT_ID']
TWITCH_EXTENSION_VERSION = os.environ['TWITCH_EXTENSION_VERSION']

CACHED_DCCON_UPDATE_DELTA = timedelta(hours=1)
