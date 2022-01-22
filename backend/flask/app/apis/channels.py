from datetime import datetime

from flask import abort
from flask_restful import Resource, reqparse
from sqlalchemy import exists

from .common import verify_broadcaster, decode_twitch_token, update_twitch_rc, get_channel_by_user_id, \
    update_cached_dccon, update_db, parse_bool, proxyimg_dccon_json
from .. import api, db
from ..consts import CACHED_DCCON_UPDATE_DELTA
from ..models import Channel


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
                update_twitch_rc(decoded_token, twitch_extension_version, ['dcconUrl'])
            else:
                update_twitch_rc(decoded_token, twitch_extension_version, [])

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('dccon_url', type=str, required=False)
        parser.add_argument('dccon_type', type=str, required=False)
        parser.add_argument('is_using_cache', type=int, required=False)
        parser.add_argument('twitch_extension_version', type=str, required=False) # TODO: change required options to true after v0.0.2 
        args = parser.parse_args()

        token = args['token']
        dccon_url = args['dccon_url'] if 'dccon_url' in args else None
        dccon_type = args['dccon_type'] if 'dccon_type' in args else None
        is_using_cache = parse_bool(args['is_using_cache']) if 'is_using_cache' in args else None
        twitch_extension_version = args['twitch_extension_version'] if 'twitch_extension_version' in args else None

        if twitch_extension_version is None:
            twitch_extension_version = '0.0.1'

        if dccon_type not in Channel.DCCON_TYPES:
            abort(400, '{dccon_type} is invalid dccon_type'.format(dccon_type=dccon_type))

        decoded_token = decode_twitch_token(token)
        broadcaster_user_id = verify_broadcaster(decoded_token)

        if user_id != broadcaster_user_id:
            abort(400, 'Mismatched user_id')

        channel = get_channel_by_user_id(user_id)

        old_dccon_url = channel.dccon_url
        if dccon_url is not None:
            channel.dccon_url = dccon_url
            twitch_rc_dccon(dccon_url)

        if dccon_type is not None:
            channel.dccon_type = dccon_type

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


# note: If you edit url of proxy dccon, you should change Channel.proxy_dccon_url method too.
# noinspection PyMethodMayBeStatic
@api.resource('/api/channel/<string:user_id>/proxy-dccon')
class ApiChannelProxyDccon(Resource):
    def get(self, user_id):
        channel = get_channel_by_user_id(user_id)

        dccon = None

        if channel.is_using_cache:
            if not channel.last_cache_update:
                update_cached_dccon(channel)
            else:
                utc_now = datetime.utcnow()
                checkpoint = channel.last_cache_update + CACHED_DCCON_UPDATE_DELTA
                if checkpoint < utc_now:
                    update_cached_dccon(channel)
            dccon = channel.cached_dccon
        else:
            from .exports import convert_dccon
            dccon, result_code = convert_dccon(channel.dccon_type, channel.dccon_url)

        return proxyimg_dccon_json(dccon), 200
