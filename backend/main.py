# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
# img = cv.imread('test.jpg')
# dst = cv.fastNlMeansDenoisingColored(img,None,10,10,7,21)
# plt.subplot(121),plt.imshow(img)
# plt.subplot(122),plt.imshow(dst)
# plt.show()

from bottle import run, route, response, request, static_file
import json
from json import dumps
from UserData import *

global_working_directory = './data'
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


@route('/upload-file', method='POST')
@route('/upload-file', method='OPTIONS')
@allow_cors
def upload_file():
    user_id = str(request.forms.get('user_id'))
    print('upload-file -> ID:' + user_id)

    image_data = request.files.get('file')

    result = upload_user_image(user_id, image_data)
    is_success = True if result is not None else False
    if not is_success:
        answer = {'is_success': is_success, 'content': {}, 'errors': ["Can't load user data."]}
    else:
        answer = {'is_success': is_success, 'content': {}, 'errors': []}
    return dumps(answer)


@route('/get-original-file', method='GET')
@allow_cors
def get_original_file():
    user_id = request.query.user_id

    print('get-original-file -> ID: ' + user_id)

    user = get_user_data(user_id)
    answer = {}
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)
    image_path = user.get_current_image().path
    if image_path is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    serv_path = to_server_path(image_path)
    print(serv_path)

    answer = {'is_success': True, 'content': {"file_path" : serv_path}, 'errors': []}
    return dumps(answer)

@route('/use-filters', method='POST')
@allow_cors
def use_filters(self):
    print('Success!!!')
    answer = {'result': 'Ok!'}
    return dumps(answer)
    js_res = ''
    return js_res


@route('/get-filtered-file', method='POST')
@allow_cors
def get_filtered_file(self):
    print('Success!!!')
    answer = {'result': 'Ok!'}
    return dumps(answer)
    js_res = ''
    return js_res


@route('/get-preview-filters', method='POST')
@allow_cors
def get_preview_filters(self):
    print('Success!!!')
    answer = {'result': 'Ok!'}
    return dumps(answer)
    js_res = ''
    return js_res


@route('/save-description', method='POST')
@allow_cors
def save_description(self):
    print('Success!!!')
    answer = {'result': 'Ok!'}
    return dumps(answer)
    js_res = ''
    return js_res


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./data/')




# http://178.140.250.54:8080/test
# run(host='192.168.0.103', port=8080, debug=True, reloader=True)
run(host='0.0.0.0', port=8080, debug=True, reloader=True)