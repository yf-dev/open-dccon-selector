from .imgproxy import generate_url

class DcconData:
    def __init__(self):
        self._data = {
            'dccons': []
        }

    def add_dccon(self, keywords, url, tags=None):
        self._data['dccons'].append({
            'keywords': keywords,
            'path': url,
            'tags': tags if tags else []
        })

    def get_dccon(self, keyword):
        for dccon in self._data['dccons']:
            if keyword in dccon['keywords']:
                return dccon
        return None

    def apply_proxyimg(self):
        for index, dccon in enumerate(self._data['dccons']):
            self._data['dccons'][index]['path'] = generate_url(dccon['path'])

    @classmethod
    def from_json_data(cls, data):
        instance = DcconData()
        instance._data = data
        return instance

    @property
    def json_data(self):
        return self._data
