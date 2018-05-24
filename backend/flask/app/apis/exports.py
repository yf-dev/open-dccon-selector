import json
import re
from collections import OrderedDict
from urllib.parse import urljoin

import requests
from flask import abort
from flask_restful import Resource, reqparse

from .common import get_channel
from .. import api
from ..dccon_data import DcconData
from ..models import Channel


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
            'dccon_url': channel_data['cached_dccon_url'] if channel.is_using_cache else channel_data['dccon_url']
        }
        return filtered, 200


def get_data_from_url(url):
    r = None
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        abort(500, 'Cannot get data from url: {url}'.format(url=url))

    return r.content


def convert_data_to_json(data, order_dict=False):
    data_json = None
    try:
        if order_dict:
            data_json = json.loads(data.decode('utf-8-sig'), object_pairs_hook=OrderedDict)
        else:
            data_json = json.loads(data.decode('utf-8-sig'))
    except json.JSONDecodeError as e:
        abort(500, 'Cannot decode json data from url: {e}'.format(e=e.msg))
    return data_json


def parse_open_dccon(data):
    data_json = convert_data_to_json(data)

    if not isinstance(data_json, dict):
        abort(500, 'Invalid data format: root must be object')
    if 'dccons' not in data_json:
        abort(500, 'Invalid data format: cannot find "dccons"')
    if not isinstance(data_json['dccons'], list):
        abort(500, 'Invalid data format: "dccons" must be list')

    dccon_data = DcconData()
    for index, dccon in enumerate(data_json['dccons']):
        if 'keywords' not in dccon:
            abort(500, 'Invalid data format: cannot find "keywords" on {index}th dccon'.format(index=index + 1))
        if 'tags' not in dccon:
            abort(500, 'Invalid data format: cannot find "tags" on {index}th dccon'.format(index=index + 1))
        if 'path' not in dccon:
            abort(500, 'Invalid data format: cannot find "path" on {index}th dccon'.format(index=index + 1))

        keywords = dccon['keywords']
        tags = dccon['tags']
        path = dccon['path']

        if not isinstance(keywords, list):
            abort(500, 'Invalid data format: "keywords" on {index}th dccon must be list'.format(index=index + 1))
        if not isinstance(tags, list):
            abort(500, 'Invalid data format: "tags" on {index}th dccon must be list'.format(index=index + 1))
        if not isinstance(path, str):
            abort(500, 'Invalid data format: "path" on {index}th dccon must be string'.format(index=index + 1))

        for keyword in keywords:
            if not isinstance(keyword, str):
                abort(500,
                      'Invalid data format: "keywords" on {index}th dccon must be list of string'.format(
                          index=index + 1))

        for tag in tags:
            if not isinstance(tag, str):
                abort(500,
                      'Invalid data format: "tags" on {index}th dccon must be list of string'.format(index=index + 1))

        dccon_data.add_dccon(keywords, path, tags)

    return dccon_data.json_data


def parse_open_dccon_rel_path(data, url):
    json_data = parse_open_dccon(data)
    for dccon in json_data['dccons']:
        dccon['path'] = urljoin(url, dccon['path'])

    return json_data


def parse_bridge_bbcc_general(data, url, relpath):
    REGEX_DATA = r'dcConsData\s*=\s*(\[(\s*{\s*[\s\S]*?}\s*)*\])'
    REGEX_NAME = r'(name)(\s*:\s*")'
    REGEX_KEYWORDS = r'(keywords)(\s*:\s*\[)'
    REGEX_TAGS = r'(tags)(\s*:\s*\[)'

    match = re.search(REGEX_DATA, data.decode('utf-8-sig'))
    if not match:
        abort(500, 'Invalid data format: Not matched data to "{regex}"'.format(regex=REGEX_DATA))

    dccons_jo = match.group(1)
    dccons_jo = re.sub(REGEX_NAME, r'"\1"\2', dccons_jo)
    dccons_jo = re.sub(REGEX_KEYWORDS, r'"\1"\2', dccons_jo)
    dccons_jo = re.sub(REGEX_TAGS, r'"\1"\2', dccons_jo)

    dccons = None

    try:
        dccons = json.loads(dccons_jo)
    except json.JSONDecodeError as e:
        abort(500, 'Cannot decode data: {e}'.format(e=str(e)))

    dccon_data = DcconData()
    for index, dccon in enumerate(dccons):
        if 'keywords' not in dccon:
            abort(500, 'Invalid data format: cannot find "keywords" on {index}th dccon'.format(index=index + 1))
        if 'tags' not in dccon:
            abort(500, 'Invalid data format: cannot find "tags" on {index}th dccon'.format(index=index + 1))
        if 'name' not in dccon:
            abort(500, 'Invalid data format: cannot find "name" on {index}th dccon'.format(index=index + 1))

        keywords = dccon['keywords']
        tags = dccon['tags']
        name = dccon['name']

        if not isinstance(keywords, list):
            abort(500, 'Invalid data format: "keywords" on {index}th dccon must be list'.format(index=index + 1))
        if not isinstance(tags, list):
            abort(500, 'Invalid data format: "tags" on {index}th dccon must be list'.format(index=index + 1))
        if not isinstance(name, str):
            abort(500, 'Invalid data format: "name" on {index}th dccon must be string'.format(index=index + 1))

        path = urljoin(url, relpath.format(name=name))

        for keyword in keywords:
            if not isinstance(keyword, str):
                abort(500,
                      'Invalid data format: "keywords" on {index}th dccon must be list of string'.format(
                          index=index + 1))

        for tag in tags:
            if not isinstance(tag, str):
                abort(500,
                      'Invalid data format: "tags" on {index}th dccon must be list of string'.format(index=index + 1))

        dccon_data.add_dccon(keywords, path, tags)

    return dccon_data.json_data


def parse_bridge_bbcc(data, url):
    return parse_bridge_bbcc_general(data, url, '../images/dccon/{name}')


def parse_bridge_bbcc_custom_url(data, url):
    return parse_bridge_bbcc_general(data, url, './images/{name}')


def parse_funzinnu(data):
    # note: funzinnu's dccon data is a json object. It is written as pair of keyword without prefix and url.
    # note2: Converted dccon data should keep original order of keywords
    # example: {'test': 'http://url', 'hello': 'http://world'}

    data_json = convert_data_to_json(data, order_dict=True)

    if not isinstance(data_json, OrderedDict):
        abort(500, 'Invalid data format: root must be object')

    dccon_data = DcconData()
    for index, pair in enumerate(data_json.items()):
        keyword, url = pair
        if not isinstance(url, str):
            abort(500, 'Invalid data format: {index}th dccon\'s value must be string'.format(index=index + 1))
        dccon_data.add_dccon([keyword], url)

    return dccon_data.json_data


def parse_telk(data):
    # note: telk's dccon data is almost same with open dccon format but dccon url path is relative to specific url.

    base_url = 'http://tv.telk.kr/images/'

    json_data = parse_open_dccon(data)
    for dccon in json_data['dccons']:
        dccon['path'] = base_url + dccon['path']

    return json_data


def convert_dccon(_type, url):
    if _type not in Channel.DCCON_TYPES:
        abort(400, 'Invalid type')

    data = get_data_from_url(url)

    if _type == Channel.DCCON_TYPE_OPEN_DCCON_RELATIVE_PATH:
        converted = parse_open_dccon_rel_path(data, url)
    elif _type == Channel.DCCON_TYPE_BRIDGE_BBCC:
        converted = parse_bridge_bbcc(data, url)
    elif _type == Channel.DCCON_TYPE_BRIDGE_BBCC_CUSTOM_URL:
        converted = parse_bridge_bbcc_custom_url(data, url)
    elif _type == Channel.DCCON_TYPE_FUNZINNU:
        converted = parse_funzinnu(data)
    elif _type == Channel.DCCON_TYPE_TELK:
        converted = parse_telk(data)
    else:  # Channel.DCCON_TYPE_OPEN_DCCON
        converted = parse_open_dccon(data)

    return converted, 200


# noinspection PyMethodMayBeStatic
@api.resource('/api/convert-dccon-url')
class ApiConvertDcconUrl(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        args = parser.parse_args()

        _type = args['type']
        url = args['url']

        return convert_dccon(_type, url)
