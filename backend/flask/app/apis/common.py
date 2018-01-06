import jwt
import json
import requests
from datetime import datetime, timedelta
from requests import HTTPError
from flask import abort

from .. import db
from ..consts import TWITCH_EXTENSION_SECRET, TWITCH_EXTENSION_CLIENT_ID, TWITCH_EXTENSION_VERSION
from ..utils import twitch_channel_name_to_id
from ..models import Channel


def get_channel(user_id, channel_name):
    if user_id and channel_name:
        abort(400, 'Cannot set channel_id and channel_name at the same time.')
    elif not user_id and not channel_name:
        abort(400, 'You must set channel_id or channel_name')

    if channel_name:
        try:
            user_id = twitch_channel_name_to_id(channel_name)
            if user_id is None:
                abort(400, 'Cannot convert channel_name ' + str(channel_name))
        except HTTPError:
            abort(400, 'Cannot convert channel_name ' + str(channel_name))

    return get_channel_by_user_id(user_id)


def get_channel_by_user_id(user_id):
    channel = Channel.query.filter_by(user_id=user_id).first()
    if not channel:
        abort(404, 'Not found for channel_id ' + str(user_id))
    return channel


def decode_twitch_token(token):
    decoded_token = None
    try:
        decoded_token = jwt.decode(token, TWITCH_EXTENSION_SECRET)
    except jwt.InvalidTokenError as e:
        # raise e
        abort(400, 'Invalid token')
    return decoded_token


def verify_broadcaster(decoded_token):
    if decoded_token['user_id'] != decoded_token['channel_id']:
        abort(400, 'Invalid userId')

    if decoded_token['role'] != 'broadcaster':
        abort(400, 'You are not a broadcaster')

    return decoded_token['user_id']


def update_twitch_rc(decoded_token, rc):
    new_token_data = dict(decoded_token)
    new_token_data['exp'] = datetime.utcnow() + timedelta(minutes=1)
    new_token_data['role'] = 'external'
    new_token = jwt.encode(new_token_data, TWITCH_EXTENSION_SECRET).decode("utf-8")

    url = 'https://api.twitch.tv/extensions/' + TWITCH_EXTENSION_CLIENT_ID + '/' + \
          TWITCH_EXTENSION_VERSION + '/required_configuration?channel_id=' + decoded_token['channel_id']

    r = None
    try:
        r = requests.put(url, data={
            'required_configuration': ','.join(rc) if rc else 'nope'
        }, headers={
            'Authorization': 'Bearer ' + new_token,
            'Client-Id': TWITCH_EXTENSION_CLIENT_ID
        })
    except HTTPError:
        abort(400, 'Cannot update required configuration for twitch')

    return r.content.decode("utf-8"), r.status_code


def update_cached_dccon(channel):
    r = requests.get(channel.dccon_url)

    dccon_json = None
    try:
        dccon_json = json.loads(r.content.decode('utf-8'))
    except json.JSONDecodeError as e:
        abort(400, 'Cannot decode json from ' + str(channel.dccon_url))

    channel.cached_dccon = dccon_json
    channel.last_cache_update = datetime.utcnow()

    update_db()


def update_db():
    # noinspection PyBroadException
    try:
        db.session.commit()
        db.session.flush()
    except:
        db.session.rollback()
        abort(500, 'Cannot update database')
