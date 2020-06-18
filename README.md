# clarinel-hdlproxy
A thin HDL proxy for clarin.gr

## Setup for development
```
$ pip install -r requirements.txt
```

To just run the service (in port 5000) :
```
$ python hdlproxy/app.py
```

To run it with gunicorn
```
$ gunicorn --bind 0.0.0.0:5001 hdlproxy.app:app
```

To run it in a devs container:
```
docker-compose up hdlproxy_dev
```

## Setup for production
Use the following container:
```
$ docker-compose build hdlproxy_dev
```

To test the container:
```
docker-compose up hdlproxy_dev
```

See `docker-compose.yml` for an example setup.

### host and port
The default host is 0.0.0.0 and the default port is 8000.
Typically, keep them as they are and use a proxy or an ingress to access them.

### The PID
The PID we handle here has the form PID-PREFIX/PID-SUFFIX.
e.g. for PID 11239/ATHENA-0000-0000-0001-2B-2, the PID prefix is 11239 and the suffix is ATHENA-0000-0000-0001-2B-2

### Environment variables
```
HDLPROXY_HDL_URI: 'https://hdl.grnet.gr/'
HDLPROXY_PID_URL_PREFICES: '11500 http://hdl.grnet.gr/,11239 http://hdl.grnet.gr/'
HDLPROXY_CMDI_URLS: '11500 https://inventory.clarin.gr/oai_pmh/,11239 https://test.clarin.gr/oai_pmh/'
```

- HDLPROXY_HDL_URI is the URI of the HDL server we use as default (aka, non-CMDI flow). E.g.:
`https://hdl.grnet.gr/11239/ATHENA-0000-0000-0001-2B-2`

- HDLPROXY_PID_URL_PREFICES is a comma-separated list of 'pid_prefix URL' values. Each pair contains a PID prefix and a URL. The URL is the base for the PID URL e.g., an example of PID url could be `http://hdl.grnet.gr/11239/ATHENA-0000-0000-0001-2B-2`.
  This is not something we redirect to. We use it to contruct CMDI redirects.

- HDLPROXY_CMDI_URLS is a comma-separated list of 'pid_prefix URL' values. Each pair contains a PID prefix (see above) and a URL. The URL is where we redirect to in the CMDI case.
The application appends this to the url:
`?verb=GetRecord&identifier=PID-URL&metadataPrefix=cmdi`

So a redirect URL is constructed, for instance:
`https://inventory.clarin.gr/oai_pmh/?verb=GetRecord&identifier=http://hdl.grnet.gr/11239/ATHENA-0000-0000-0001-2B-2&metadataPrefix=cmdi`
