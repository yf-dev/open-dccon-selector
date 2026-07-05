from datetime import datetime, timezone

import requests

from .consts import TWITCH_EXTENSION_CLIENT_ID, TWITCH_EXTENSION_CLIENT_SECRET

_app_access_token = None


def utcnow():
    """Naive datetime in UTC, matching the DB's timezone-less columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _fetch_app_access_token():
    global _app_access_token
    r = requests.post('https://id.twitch.tv/oauth2/token', data={
        'client_id': TWITCH_EXTENSION_CLIENT_ID,
        'client_secret': TWITCH_EXTENSION_CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }, timeout=5)
    r.raise_for_status()
    _app_access_token = r.json()['access_token']
    return _app_access_token


def _get_users(channel_name, token):
    return requests.get('https://api.twitch.tv/helix/users', params={
        'login': channel_name,
    }, headers={
        'Authorization': 'Bearer ' + token,
        'Client-Id': TWITCH_EXTENSION_CLIENT_ID,
    }, timeout=5)


def twitch_channel_name_to_id(channel_name):
    token = _app_access_token or _fetch_app_access_token()
    r = _get_users(channel_name, token)
    if r.status_code == 401:
        # cached app access token may have expired; fetch a new one and retry once
        r = _get_users(channel_name, _fetch_app_access_token())
    r.raise_for_status()

    users = r.json().get('data', [])
    if users:
        return users[0]['id']
    return None
