from flask_restful import Resource, reqparse

from .. import api
from .common import get_channel


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

        channel = get_channel(user_id, channel_name)
        channel_data = channel.json()
        filtered = {
            'user_id': channel_data['user_id'],
            'dccon_url': channel_data['dccon_url']
        }
        return filtered, 200
