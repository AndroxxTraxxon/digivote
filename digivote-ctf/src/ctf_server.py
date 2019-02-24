import flask
import time
import ssl
import sqlite3

app = flask.Flask(__name__)
global counter
counter = 0

def get_hit_count():
    global counter
    counter += 1
    return counter


@app.route('/hello')
def hello():
    count = get_hit_count()
    return 'CTF Server:: Hello World! I have been seen {} times.\n'.format(count)


context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('ctf.crt', 'ctf.key')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)