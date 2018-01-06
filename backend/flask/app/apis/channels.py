from datetime import datetime

from flask import abort
from flask_restful import Resource, reqparse

from .. import api, db
from ..consts import CACHED_DCCON_UPDATE_DELTA
from ..models import Channel
from .common import verify_broadcaster, decode_twitch_token, update_twitch_rc, get_channel_by_user_id, \
    update_cached_dccon, update_db


# noinspection PyMethodMayBeStatic
@api.resource('/api/channels')
class ApiChannels(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('dcconUrl', type=str, required=True)
        args = parser.parse_args()

        token = args['token']
        dccon_url = args['dcconUrl'].strip()

        if not dccon_url:
            dccon_url = None

        decoded_token = decode_twitch_token(token)
        user_id = verify_broadcaster(decoded_token)

        channel = Channel.query.filter_by(user_id=user_id).first()
        if not channel:
            # noinspection PyArgumentList
            channel = Channel(
                user_id=user_id,
                dccon_url=dccon_url,
            )
            db.session.add(channel)
        else:
            channel.dccon_url = dccon_url

        update_db()

        return update_twitch_rc(decoded_token, ['dcconUrl'])



# note: If you edit url of cached dccon, you should change Channel.cached_dccon_url method too.
# noinspection PyMethodMayBeStatic
@api.resource('/api/channel/<string:user_id>/cached-dccon')
class ApiChannelCachedDccon(Resource):
    def get(self, user_id):
        channel = get_channel_by_user_id(user_id)

        if not channel.last_cache_update:
            update_cached_dccon(channel)
        else:
            utc_now = datetime.utcnow()
            checkpoint = channel.last_cache_update + CACHED_DCCON_UPDATE_DELTA
            if checkpoint < utc_now:
                update_cached_dccon(channel)

        return channel.cached_dccon, 200


# noinspection PyMethodMayBeStatic
@api.resource('/api/channel/<string:user_id>/cached-dccon/update')
class ApiChannelCachedDcconUpdate(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()

        token = args['token']

        decoded_token = decode_twitch_token(token)
        broadcaster_user_id = verify_broadcaster(decoded_token)

        if user_id != broadcaster_user_id:
            abort(400, 'Mismatched user_id')

        channel = get_channel_by_user_id(user_id)
        update_cached_dccon(channel)

        return channel.json(), 200
