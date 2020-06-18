import os
from urllib.parse import urljoin

from flask import Flask, redirect, request

app = Flask(__name__)

# Fish environment variables
_hdl_uri = 'http://hdl.grnet.gr'
HDL_URI = os.environ.get('HDLPROXY_HDL_URI') or _hdl_uri

REDIRECT_SUFFIX = '?verb=GetRecord&identifier={pid_url}&metadataPrefix=cmdi'


def get_pid_url_prefices():
    """
    Analyze and extract info for prefices string of the form
    "12345 http://hdl.grnet.gr/,23456 http://clarin.gr/"
    :return: {"12345": "http://hdl.grnet.gr/", "23456": "http://clarin.gr/"}
    """
    prefices = dict()
    prefices_str = os.environ.get('HDLPROXY_PID_URL_PREFICES') or ""
    for prefix_str in prefices_str.split(','):
        if prefix_str:
            pid_prefix, fqdn = prefix_str.split(' ')
            prefices[pid_prefix.strip()] = fqdn.strip()
    return prefices


def get_cmdi_fqdns():
    fqdns = dict()
    fqdns_str = os.environ.get('HDLPROXY_CMDI_URLS') or ""
    for fqdn_str in fqdns_str.split(','):
        if fqdn_str:
            pid_prefix, fqdn = fqdn_str.split(' ')
            fqdns[pid_prefix.strip()] = fqdn.strip()
    return fqdns


@app.route('/<int:pid_prefix>/<string:pid_suffix>')
def handle_pid(pid_prefix, pid_suffix):
    pid = '{}/{}'.format(pid_prefix, pid_suffix)
    app.logger.info("Handle PID {pid}".format(pid=pid))
    accept_header = request.headers.get('Accept') or ''
    app.logger.debug("Accept header: {}".format(accept_header))

    redirect_url = urljoin(HDL_URI, pid)
    if 'application/x-cmdi+xml' in accept_header:
        # Negociate
        app.logger.debug("Reuqest for X-CDMI redirect")
        cmdi_redirect_url = get_cmdi_fqdns().get(str(pid_prefix))
        if cmdi_redirect_url:
            pid_url_prefix = get_pid_url_prefices().get(str(pid_prefix))
            if pid_url_prefix:
                app.logger.debug('Handle as x-cdmi+xml')
                pid_url = urljoin(pid_url_prefix, pid)
                redirect_suffix = REDIRECT_SUFFIX.format(pid_url=pid_url)
                redirect_url = urljoin(cmdi_redirect_url, redirect_suffix)
            else:
                app.logger.debug(
                    "No url prefix for PID prefix {}, redirect as text".format(
                        pid_prefix))
        else:
            app.logger.debug(
                "No redirect url for PID prefix {}, redirect as text".format(
                    pid_prefix))

    app.logger.info('Redirect to {}'.format(redirect_url))
    return redirect(redirect_url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
