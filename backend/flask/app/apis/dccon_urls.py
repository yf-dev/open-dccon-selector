from datetime import datetime

from flask_restful import Resource, reqparse

from .. import api
from ..consts import CACHED_DCCON_UPDATE_DELTA
from .common import get_channel, get_channel_by_user_id, update_cached_dccon


# noinspection PyMethodMayBeStatic
@api.resource('/api/dccon-url')
class ApiDcconUrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('channel_id', type=str, required=False)  # deprecated, use user_id instead
        parser.add_argument('user_id', type=str, required=False)
        parser.add_argument('channel_name', type=str, required=False)
        args = parser.parse_args()

        user_id = None
        channel_name = None

        if 'channel_id' in args and args['channel_id']:
            user_id = args['channel_id']
        if 'user_id' in args and args['user_id']:
            user_id = args['user_id']

        if 'channel_name' in args and args['channel_name']:
            channel_name = args['channel_name']

        setting = get_channel(user_id, channel_name)
        setting_data = setting.json()
        filtered = {
            'user_id': setting_data['user_id'],
            'dccon_url': setting_data['dccon_url']
        }
        return filtered, 200


# noinspection PyMethodMayBeStatic
@api.resource('/cached-dccon.json')
class ApiCachedDccon(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True)
        args = parser.parse_args()

        user_id = args['user_id']
        setting = get_channel_by_user_id(user_id)

        if not setting.last_cache_update:
            update_cached_dccon(setting)
        else:
            utc_now = datetime.utcnow()
            checkpoint = setting.last_cache_update + CACHED_DCCON_UPDATE_DELTA
            if checkpoint < utc_now:
                update_cached_dccon(setting)

        return setting.cached_dccon, 200
