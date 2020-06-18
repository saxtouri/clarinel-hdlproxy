import os
from urllib.parse import urljoin

from flask import Flask, request

app = Flask(__name__)

_hdl_uri = 'https://hdl.grnet.gr'
HDL_URI = os.environ.get('HDLPROXY_HDL_URI') or _hdl_uri

_target_uri = 'https://inventory.clarin.gr/oai_pmh/'
CMDI_BASE = os.environ.get('HDLPROXY_CMDI_TARGET_URI') or _target_uri
CMDI_URL = "{base}?verb=GetRecord&identifier={pid_suffix}?&metadataPrefix=cmdi"


@app.route('/<int:pid_prefix>/<string:pid_suffix>')
def handle_pid(pid_prefix, pid_suffix):
    pid = '{}/{}'.format(pid_prefix, pid_suffix)
    app.logger.info("Handle PID {pid}".format(pid=pid))

    accept_header = request.headers.get('Accept') or ''
    app.logger.debug("Accept header: {}".format(accept_header))

    if 'application/x-cmdi+xml' in accept_header:
        app.logger.debug('Handle as x-cdmi+xml')
        redirect_url = CMDI_URL.format(base=CMDI_BASE, pid_suffix=pid_suffix)
    else:
        app.logger.debug('Handle as text/html')
        redirect_url = urljoin(HDL_URI, pid)
    return 'Redirect to {}'.format(redirect_url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
