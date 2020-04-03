from bottle import run, route, response, request
from json import dumps

#================================ SERVER ==========================================

all_ids = []

def allow_cors(func):
    """ this is a decorator which enable CORS for specified endpoint """
    def wrapper(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return func(*args, **kwargs)
    return wrapper


@route('/test', method='GET')
@route('/test', method='POST')
@allow_cors
def get_new_session_id():
    print('SERVER: Connected')
    answer = {'result': True, 'test_field': 154}
    response.content_type = 'application/json'
    return dumps(answer)


# http://178.140.250.54:8080/test
# run(host='192.168.0.103', port=8080, debug=True, reloader=True)
run(host='0.0.0.0', port=8080, debug=True, reloader=True)