from datetime import datetime, timedelta

import jwt
import requests
from flask import abort
from requests.exceptions import RequestException

from .. import db
from ..consts import TWITCH_EXTENSION_SECRET, TWITCH_EXTENSION_CLIENT_ID, TWITCH_EXTENSION_OWNER_ID
from ..models import Channel
from ..utils import twitch_channel_name_to_id
from ..dccon_data import DcconData


def parse_bool(val):
    if val is None:
        return val
    elif val is 1:
        return True
    elif val is 0:
        return False
    else:
        abort(400, 'Boolean value must be one of 1 or 0.')


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
        except RequestException:
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


def update_twitch_rc(decoded_token, twitch_extension_version, rc):
    token_data = {
        'exp': datetime.utcnow() + timedelta(minutes=1),
        'user_id': TWITCH_EXTENSION_OWNER_ID,
        'role': 'external',
    }
    token = jwt.encode(token_data, TWITCH_EXTENSION_SECRET).decode("utf-8")

    url = 'https://api.twitch.tv/extensions/' + TWITCH_EXTENSION_CLIENT_ID + '/' + \
          twitch_extension_version + '/required_configuration?channel_id=' + decoded_token['channel_id']

    r = None
    try:
        r = requests.put(url, data={
            'required_configuration': ','.join(rc) if rc else 'nope'
        }, headers={
            'Authorization': 'Bearer ' + token,
            'Client-Id': TWITCH_EXTENSION_CLIENT_ID
        }, timeout=5)
    except RequestException:
        abort(400, 'Cannot update required configuration for twitch')

    res = r.content.decode("utf-8")
    code = r.status_code

    if code // 100 != 2:
        abort(code, 'Twitch required_configuration failed: {res}'.format(res=res))


def update_cached_dccon(channel):
    from .exports import convert_dccon
    dccon_json, result_code = convert_dccon(channel.dccon_type, channel.dccon_url)

    channel.cached_dccon = dccon_json
    channel.last_cache_update = datetime.utcnow()

    update_db()


def update_db(cb_rollback=None):
    # noinspection PyBroadException
    try:
        db.session.commit()
        db.session.flush()
    except:
        db.session.rollback()
        if cb_rollback:
            cb_rollback()
        abort(500, 'Cannot update database')

def proxyimg_dccon_json(dccon_json):
    dccon = DcconData.from_json_data(dccon_json)
    dccon.apply_proxyimg()
    return dccon.json_data
