def mappathf(path):
    p = path + 'mapped'
    return p

def translate_ciao(response):
    response.body = response.body.replace(b"ciao", b"hello")

def bar_to_foo(response):
    response.body = response.body.replace(b"bar", b"foo")

def rewrite_headers(response, request, orig_response, host, port, path):
    # make up a header and arbitrarily set it to one of the kwargs
    response.headers['X-Rewrite-Headers'] = path

def rewrite_status(response):
    response.code = 202
    response.reason = 'i have my reasons'

c.ServerProxy.servers = {
    'python-http': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
    },
    'python-http-abs': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'absolute_url': True
    },
    'python-http-port54321': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'port': 54321,
    },
    'python-http-mappath': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'mappath': {
            '/': '/index.html',
        }
    },
    'python-http-mappathf': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'mappath': mappathf,
    },
    'python-websocket' : {
        'command': ['python3', './tests/resources/websocket.py', '--port={port}'],
        'request_headers_override': {
            'X-Custom-Header': 'pytest-23456',
        }
    },
    'python-request-headers': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'request_headers_override': {
            'X-Custom-Header': 'pytest-23456',
        }
    },
    'python-gzipserver': {
        'command': ['python3', './tests/resources/gzipserver.py', '{port}'],
    },
    'python-http-rewrite-response': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'rewrite_response': translate_ciao,
    },
    'python-http-rewrite-response-more': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'rewrite_response': [rewrite_headers, rewrite_status],
    },
}

c.ServerProxy.non_service_rewrite_response = bar_to_foo

import sys
sys.path.append('./tests/resources')
c.ServerApp.jpserver_extensions = { 'proxyextension': True }
c.NotebookApp.nbserver_extensions = { 'proxyextension': True }
#c.Application.log_level = 'DEBUG'
