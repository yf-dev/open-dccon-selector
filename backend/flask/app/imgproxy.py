# https://github.com/imgproxy/imgproxy/blob/de21b937db3e469e8cfcc2850f49ba9eb1eaa55d/examples/signature.py

import base64
import hashlib
import hmac
import textwrap

from .consts import IMGPROXY_PROTOCOL, IMGPROXY_HOSTNAME, IMGPROXY_KEY, IMGPROXY_SALT


key = bytes.fromhex(IMGPROXY_KEY)
salt = bytes.fromhex(IMGPROXY_SALT)

def generate_url(original_url):
    encoded_url = base64.urlsafe_b64encode(original_url.encode()).rstrip(b'=').decode()
    # You can trim padding spaces to get good-looking url
    encoded_url = '/'.join(textwrap.wrap(encoded_url, 16))

    path = '/resize:{resizing_type}:{width}:{height}:{enlarge}/{encoded_url}'.format(
        encoded_url=encoded_url,
        resizing_type='fit',
        width=100,
        height=100,
        enlarge=0,
    ).encode()
    digest = hmac.new(key, msg=salt+path, digestmod=hashlib.sha256).digest()

    protection = base64.urlsafe_b64encode(digest).rstrip(b'=')

    url = b'%s://%s/%s%s' % (
        IMGPROXY_PROTOCOL.encode(),
        IMGPROXY_HOSTNAME.encode(),
        protection,
        path,
    )

    return url.decode()
