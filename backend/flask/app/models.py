from datetime import datetime

from . import db, api
from .consts import API_HOSTNAME


class CommonModel(object):
    def _serialize(self):
        """Jsonify the sql alchemy query result."""
        convert = dict()
        d = dict()
        # noinspection PyUnresolvedReferences
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            if c.type in convert.keys() and v is not None:
                try:
                    d[c.name] = convert[c.type](v)
                except:
                    d[c.name] = "Error: Failed to covert using ", str(
                        convert[c.type])
            elif v is None:
                if hasattr(c.type, '__visit_name__') and c.type.__visit_name__ == 'JSON':
                    d[c.name] = None
                elif "INTEGER" == str(c.type) or "NUMERIC" == str(c.type):
                    # print "??"
                    d[c.name] = 0
                elif "DATETIME" == str(c.type):
                    d[c.name] = None
                else:
                    # print c.type
                    d[c.name] = str()
            elif isinstance(v, datetime):
                if v.utcoffset() is not None:
                    v = v - v.utcoffset()
                d[c.name] = v.strftime('%Y-%m-%d %H:%M:%S')
            else:
                d[c.name] = v
        return d

    def json(self):
        raise NotImplementedError()


class Channel(db.Model, CommonModel):
    __tablename__ = 'channel'

    DCCON_TYPE_OPEN_DCCON = 'open_dccon'
    DCCON_TYPE_OPEN_DCCON_RELATIVE_PATH = 'open_dccon_rel_path'
    DCCON_TYPE_BRIDGE_BBCC = 'bridge_bbcc'
    DCCON_TYPE_FUNZINNU = 'funzinnu'
    DCCON_TYPE_TELK = 'telk'
    DCCON_TYPE_BRIDGE_BBCC_CUSTOM_URL = 'bridge_bbcc_cu'

    DCCON_TYPES = (
        DCCON_TYPE_OPEN_DCCON,
        DCCON_TYPE_OPEN_DCCON_RELATIVE_PATH,
        DCCON_TYPE_BRIDGE_BBCC,
        DCCON_TYPE_FUNZINNU,
        DCCON_TYPE_TELK,
        DCCON_TYPE_BRIDGE_BBCC_CUSTOM_URL
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Unicode(64, collation='c'), nullable=False, unique=True)
    dccon_url = db.Column(db.Unicode(512, collation='c'), nullable=True)
    dccon_type = db.Column(db.Unicode(32, collation='c'), nullable=False, default=DCCON_TYPE_OPEN_DCCON)
    last_cache_update = db.Column(db.DateTime(), nullable=True)
    is_using_cache = db.Column(db.Boolean(), nullable=False, default=False)
    cached_dccon = db.Column(db.JSON(), nullable=True)

    def json(self):
        channel = self._serialize()
        channel.pop('id')
        channel.pop('cached_dccon')
        if self.is_using_cache:
            channel['cached_dccon_url'] = self.cached_dccon_url()
        channel['proxy_dccon_url'] = self.proxy_dccon_url()
        return channel

    def cached_dccon_url(self):
        from .apis.channels import ApiChannelCachedDccon
        return 'https://{host}{url}'.format(
            host=API_HOSTNAME,
            url=api.url_for(ApiChannelCachedDccon, user_id=self.user_id)
        )

    def proxy_dccon_url(self):
        from .apis.channels import ApiChannelProxyDccon
        return 'https://{host}{url}'.format(
            host=API_HOSTNAME,
            url=api.url_for(ApiChannelProxyDccon, user_id=self.user_id)
        )
