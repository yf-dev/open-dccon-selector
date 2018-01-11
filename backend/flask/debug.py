# noinspection PyUnresolvedReferences
from app import app

if __name__ == '__main__':
    context = ('/etc/ssl/private/localhost-ssl.crt', '/etc/ssl/private/localhost-ssl.key')
    app.run(host="0.0.0.0", port=8088, ssl_context=context, debug=True)
