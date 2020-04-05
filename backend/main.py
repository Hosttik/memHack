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
import ast

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

    medals = bool(int(str(request.forms.get('medals'))))
    print('upload-file -> medals:' + str(medals))

    image_data = request.files.get('file')

    result = upload_user_image(user_id, medals, image_data)
    is_success = True if result is not None else False
    if not is_success:
        answer = {'is_success': is_success, 'content': {}, 'errors': ["Can't load user data."]}

    user = get_user_data(user_id)
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)
    image = user.get_current_image()
    if image is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    image_path = image.path

    serv_path = to_server_path(image_path)

    if medals:
        answer = {'is_success': is_success, 'content': {'file_path': serv_path, 'medals': ['medal_1', 'medal_2', 'medal_3']}, 'errors': []}
    else:
        answer = {'is_success': is_success, 'content': {}, 'errors': []}
    return dumps(answer)


@route('/get-original-file', method='GET')
@allow_cors
def get_original_file():
    user_id = request.query.user_id

    print('get-original-file -> ID: ' + user_id)

    answer = {}
    user = get_user_data(user_id)
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)
    image = user.get_current_image()
    if image is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    image_path = image.path

    serv_path = to_server_path(image_path)

    answer = {'is_success': True, 'content': {"file_path" : serv_path}, 'errors': []}
    return dumps(answer)


@route('/use-filters', method='POST')
@allow_cors
def use_filters():
    data = json.loads(request.forms.get('params'))
    user_id = data['user_id']
    print('use-filters -> ID:' + user_id)

    filters = data['filters']
    answer = {}

    print('filters: ' + ' '.join(filters))

    user = get_user_data(user_id)
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)
    image = user.get_current_image()
    if image is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    res = image.apply_filters(filters)

    if not res:
        answer = {'is_success': False, 'content': {}, 'errors': ["Filters applying error."]}
        return dumps(answer)

    path = image.get_release_path()
    if path is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is no release file."]}
        return dumps(answer)

    serv_path = to_server_path(path)

    answer = {'is_success': True, 'content': {"file_path": serv_path}, 'errors': []}
    return dumps(answer)


@route('/get-filtered-file', method='POST')
@allow_cors
def get_filtered_file():
    user_id = request.query.user_id

    print('get-filtered-file -> ID: ' + user_id)

    answer = {}
    user = get_user_data(user_id)
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)
    image = user.get_current_image()
    if image is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    image_path = image.path

    path = image.get_release_path()
    if path is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is no release file."]}
        return dumps(answer)

    serv_path = to_server_path(path)

    answer = {'is_success': True, 'content': {"file_path": serv_path}, 'errors': []}
    return dumps(answer)


@route('/get-preview-filters', method='GET')
@allow_cors
def get_preview_filters():
    user_id = request.query.user_id

    print('get-original-file -> ID: ' + user_id)

    user = get_user_data(user_id)
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)
    image = user.get_current_image()
    if image is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    answer = []
    for p in list(image.previews_paths.keys()):
        ans = {'id' : p, 'name' : filters_names_dict[p], 'path' : to_server_path(image.previews_paths[p])}
        answer.append(ans)

    answer = {'is_success': True, 'content' : answer, 'errors': []}

    return dumps(answer)


@route('/save-description', method='GET')
@allow_cors
def save_description():
    user_id = request.query.user_id

    print('save-description -> ID: ' + user_id)

    fname = request.query.first_name
    lname = request.query.last_name
    mname = request.query.middle_name
    rank = request.query.rank
    info = request.query.info

    descr = {"user_id" : user_id, "first_name" : fname, "last_name" : lname, "middle_name" : mname, "rank" : rank, "info": info}

    answer = {}

    user = get_user_data(user_id)
    if user is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["Can't load user data."]}
        return dumps(answer)

    print ('userdata ok')

    image = user.get_current_image()
    if image is None:
        answer = {'is_success': False, 'content': {}, 'errors': ["There is now loaded images."]}
        return dumps(answer)

    print('image ok')

    is_success = image.set_description(descr)

    print('descrs ok')

    if not is_success:
        answer = {'is_success': is_success, 'content': {}, 'errors': ["Can't save description."]}
    else:
        answer = {'is_success': is_success, 'content': {}, 'errors': []}

    return dumps(answer)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./data/')




# http://178.140.250.54:8080/test
# run(host='192.168.0.103', port=8080, debug=True, reloader=True)
run(host='0.0.0.0', port=8080, debug=True, reloader=True)