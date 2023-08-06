import json
from datetime import date, datetime

KEY_CODE = 'c'
KEY_MESSAGE = 'm'
KEY_DATA = 'd'

CODE_SUCCEED = 0
CODE_FAILED = -1


def app_response(code, msg, data):
    if code is None:
        return None
    if msg and data:
        return {KEY_CODE: code, KEY_MESSAGE: msg, KEY_DATA: data}
    if msg and not data:
        return {KEY_CODE: code, KEY_MESSAGE: msg}
    if not msg and data:
        return {KEY_CODE: code, KEY_DATA: data}
    if not msg and not data:
        return {KEY_CODE: code}


def app_succeed(data):
    return app_response(CODE_SUCCEED, None, data)


def app_failed(msg, data=None):
    return app_response(CODE_FAILED, msg, data)


def response_code(p):
    return p[KEY_CODE]


def response_msg(p):
    return p[KEY_MESSAGE]


def response_data(p):
    return p[KEY_DATA]


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def response_json(result, headers=None):
    result = json.dumps(result, cls=ComplexEncoder)
    content_length = len(result.encode('utf-8'))
    return {'headers': append_headers([
            ('Content-Type', 'application/json;charset=utf-8'),
            ('Content-Length', str(content_length))
            ], headers),
            'status': '200 OK',
            'content': result}


def append_headers(response_headers, headers):
    return response_headers + \
        list(headers.items()) if headers else response_headers


def response_raw(result, headers=None):
    content_length = len(result.encode('utf-8'))
    return {'headers': append_headers(
        [('Content-Type', 'text/plain;charset=utf-8'),
         ('Content-Length', str(content_length))], headers),
        'status': '200 OK',
        'content': result}


def response_404():
    return {'headers': [('Content-Type', 'text/html;charset=utf-8'),
                        ('Content-Length', '0')],
            'status': '404 Not Found',
            'content': ''}


def response_400():
    return {'headers': [
        ('Content-Type', 'text/html;charset=utf-8'),
        ('Content-Length', '0')],
        'status': '400 Bad Request',
        'content': ''}


def response_500():
    return {'headers': [
        ('Content-Type', 'text/html;charset=utf-8'),
        ('Content-Length', '0')],
        'status': '500 Internal Server Error',
        'content': ''}
