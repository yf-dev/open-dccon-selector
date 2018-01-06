from collections import OrderedDict
import requests
import json

from flask import abort
from flask_restful import Resource, reqparse

from .. import api
from ..dccon_data import DcconData
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


def get_data_from_url(url):
    r = None
    try:
        r = requests.get(url)
    except requests.HTTPError:
        abort(500, 'Cannot get data from url')

    return r.content.decode("utf-8")


def convert_dccon_funzinnu(data):
    # note: funzinnu's dccon data is a json object. It is written as pair of keyword without prefix and url.
    # note2: Converted dccon data should keep original order of keywords
    # example: {'test': 'http://url', 'hello': 'http://world'}

    data_json = None
    try:
        data_json = json.loads(data, object_pairs_hook=OrderedDict) # keeping order of keywords
    except json.JSONDecodeError:
        abort(500, 'Cannot decode json data from url')

    dccon_data = DcconData()
    for keyword, url in data_json.items():
        dccon_data.add_dccon([keyword], url)

    return dccon_data.json_data


# noinspection PyMethodMayBeStatic
@api.resource('/api/convert-dccon-url')
class ApiConvertDcconUrl(Resource):
    TYPE_FUNZINNU = 'funzinnu'
    TYPES = (
        TYPE_FUNZINNU,
    )

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        args = parser.parse_args()

        _type = args['type']
        url = args['url']

        if _type not in ApiConvertDcconUrl.TYPES:
            abort(400, 'Invalid type')

        data = get_data_from_url(url)
        converted = None

        if _type == ApiConvertDcconUrl.TYPE_FUNZINNU:
            converted = convert_dccon_funzinnu(data)

        return converted, 200
