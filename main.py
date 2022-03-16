#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bottle import route, run, error, response, hook, request
from util import *

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers\


@route('/')
def m3u8():
    url = request.query.url
    if not url:
        return fail("url is empty")
    data = get_m3u8(url)
    return success(data)


@error(404)
def error404(error):
    return fail("404")


@error(405)
def error404(error):
    return fail("405")


run(host='localhost', port=8078, debug=True)
