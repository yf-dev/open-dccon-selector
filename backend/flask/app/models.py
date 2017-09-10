from datetime import datetime

from . import db


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
                if "INTEGER" == str(c.type) or "NUMERIC" == str(c.type):
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


class Setting(db.Model, CommonModel):
    __tablename__ = 'setting'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Unicode(64, collation='c'), nullable=False, unique=True)
    dccon_url = db.Column(db.Unicode(512, collation='c'), nullable=True)

    def json(self):
        setting = self._serialize()
        setting.pop('id')
        return setting
