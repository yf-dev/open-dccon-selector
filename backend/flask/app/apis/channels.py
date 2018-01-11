from datetime import datetime

from flask import abort
from flask_restful import Resource, reqparse
from sqlalchemy import exists

from .. import api, db
from ..consts import CACHED_DCCON_UPDATE_DELTA
from ..models import Channel
from .common import verify_broadcaster, decode_twitch_token, update_twitch_rc, get_channel_by_user_id, \
    update_cached_dccon, update_db, parse_bool


# noinspection PyMethodMayBeStatic
@api.resource('/api/channels')
class ApiChannels(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()

        token = args['token']

        decoded_token = decode_twitch_token(token)
        user_id = verify_broadcaster(decoded_token)
        if db.session.query(exists().where(Channel.user_id == user_id)).scalar():
            abort(400, 'Channel {user_id} is already exist'.format(user_id=user_id))

        # noinspection PyArgumentList
        channel = Channel(
            user_id=user_id,
        )
        db.session.add(channel)

        update_db()

        return channel.json(), 200


# noinspection PyMethodMayBeStatic
@api.resource('/api/channel/<string:user_id>')
class ApiChannel(Resource):
    def put(self, user_id):
        def twitch_rc_dccon(dccon_url):
            if dccon_url:
                update_twitch_rc(decoded_token, ['dcconUrl'])
            else:
                update_twitch_rc(decoded_token, [])

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('dccon_url', type=str, required=False)
        parser.add_argument('is_using_cache', type=int, required=False)
        args = parser.parse_args()

        token = args['token']
        dccon_url = args['dccon_url'] if 'dccon_url' in args else None
        is_using_cache = parse_bool(args['is_using_cache']) if 'is_using_cache' in args else None

        decoded_token = decode_twitch_token(token)
        broadcaster_user_id = verify_broadcaster(decoded_token)

        if user_id != broadcaster_user_id:
            abort(400, 'Mismatched user_id')

        channel = get_channel_by_user_id(user_id)

        old_dccon_url = channel.dccon_url
        if dccon_url is not None:
            channel.dccon_url = dccon_url
            twitch_rc_dccon(dccon_url)

        if is_using_cache is not None:
            channel.is_using_cache = is_using_cache

        update_db(cb_rollback=lambda: twitch_rc_dccon(old_dccon_url))

        return channel.json(), 200

    def get(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()

        token = args['token']

        decoded_token = decode_twitch_token(token)
        broadcaster_user_id = verify_broadcaster(decoded_token)

        if user_id != broadcaster_user_id:
            abort(400, 'Mismatched user_id')

        channel = get_channel_by_user_id(user_id)

        return channel.json(), 200


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
