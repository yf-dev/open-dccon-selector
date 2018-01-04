from flask import abort
from flask_restful import Resource, reqparse

from .. import api, db
from ..models import Channel
from .common import verify_broadcaster, decode_twitch_token, update_twitch_rc, get_channel_by_user_id, \
    update_cached_dccon


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

        setting = Channel.query.filter_by(user_id=user_id).first()
        if not setting:
            # noinspection PyArgumentList
            setting = Channel(
                user_id=user_id,
                dccon_url=dccon_url,
            )
            db.session.add(setting)
        else:
            setting.dccon_url = dccon_url

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return 'Cannot update database', 500

        return update_twitch_rc(decoded_token, ['dcconUrl'])


# noinspection PyMethodMayBeStatic
@api.resource('/api/channel/<string:user_id>/update-cached-dccon')
class ApiChannelUpdateCachedDccon(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        args = parser.parse_args()

        token = args['token']

        decoded_token = decode_twitch_token(token)
        broadcaster_user_id = verify_broadcaster(decoded_token)

        if user_id != broadcaster_user_id:
            abort(400, 'Mismatched user_id')

        setting = get_channel_by_user_id(user_id)
        update_cached_dccon(setting)

        return setting.json(), 200
