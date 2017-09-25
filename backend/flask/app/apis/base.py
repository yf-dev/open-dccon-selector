import base64
import os
from datetime import datetime, timedelta

import jwt
import requests
from flask_restful import Resource, reqparse
from requests import HTTPError
from twitch import TwitchClient

from .. import api, db
from ..models import Setting

TWITCH_EXTENSION_SECRET = base64.b64decode(os.environ['TWITCH_EXTENSION_SECRET'])
TWITCH_EXTENSION_CLIENT_ID = os.environ['TWITCH_EXTENSION_CLIENT_ID']
TWITCH_EXTENSION_VERSION = os.environ['TWITCH_EXTENSION_VERSION']

client = TwitchClient(client_id=TWITCH_EXTENSION_CLIENT_ID)


# noinspection PyMethodMayBeStatic
@api.resource('/api/update-dccon-url')
class ApiUpdateDcconUrl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        parser.add_argument('dcconUrl', type=str, required=True)
        args = parser.parse_args()

        token = args['token']
        dccon_url = args['dcconUrl'].strip()

        if not dccon_url:
            dccon_url = None

        try:
            decoded_token = jwt.decode(token, TWITCH_EXTENSION_SECRET)
        except jwt.InvalidTokenError as e:
            # raise e
            return 'Invalid token', 400

        if decoded_token['user_id'] != decoded_token['channel_id']:
            return 'Invalid userId', 400

        if decoded_token['role'] != 'broadcaster':
            return 'You are not a broadcaster', 400

        setting = Setting.query.filter_by(user_id=decoded_token['user_id']).first()
        if not setting:
            # noinspection PyArgumentList
            setting = Setting(
                user_id=decoded_token['user_id'],
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

        new_token_data = dict(decoded_token)
        new_token_data['exp'] = datetime.utcnow() + timedelta(minutes=1)
        new_token_data['role'] = 'external'
        new_token = jwt.encode(new_token_data, TWITCH_EXTENSION_SECRET).decode("utf-8")

        url = 'https://api.twitch.tv/extensions/' + TWITCH_EXTENSION_CLIENT_ID + '/' + \
              TWITCH_EXTENSION_VERSION + '/required_configuration?channel_id=' + decoded_token['channel_id']

        r = requests.put(url, data={
            'required_configuration': 'dcconUrl' if dccon_url else 'nope'
        }, headers={
            'Authorization': 'Bearer ' + new_token,
            'Client-Id': TWITCH_EXTENSION_CLIENT_ID
        })

        return r.content.decode("utf-8"), r.status_code


# noinspection PyMethodMayBeStatic
@api.resource('/api/dccon-url')
class ApiDcconUrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('channel_id', type=str, required=False)
        parser.add_argument('channel_name', type=str, required=False)
        args = parser.parse_args()

        if 'channel_id' in args and args['channel_id']:
            channel_id = args['channel_id']
        elif 'channel_name' in args and args['channel_name']:
            channel_name = args['channel_name']
            try:
                channels = client.users.translate_usernames_to_ids([channel_name])
                if channels and len(channels) > 0:
                    channel = channels[0]
                    channel_id = channel.id
                else:
                    return 'Cannot convert channel_name ' + str(channel_name), 400
            except HTTPError:
                return 'Cannot convert channel_name ' + str(channel_name), 400
        else:
            return 'You must set channel_id or channel_name', 400

        setting = Setting.query.filter_by(user_id=channel_id).first()
        if not setting:
            return 'Not found for channel_id ' + str(channel_id), 404
        else:
            return setting.json(), 200
