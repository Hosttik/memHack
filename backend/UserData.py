import os
import json
from simple_filters import *
import simple_filters

global_working_directory = './data'

class UserData:
    def __init__(self, user_dir=None):
        self.email = ''
        self.images = []
        self.working_dir = user_dir

        if self.working_dir is not None:
            self.load_user_data(self.working_dir)

    def load_user_data(self, dir):
        self.working_dir = dir
        entries = os.scandir(self.working_dir)
        for entry in entries:
            image = UserImageData(None, None)
            image.load_from_dir(os.path.normpath(self.working_dir + "/" + entry.name), entry.name)
            self.images.append(image)

    def add_image(self, image_data, description=None):
        image = UserImageData()
        name = str(len(os.listdir(self.working_dir)) + 1)
        idir = os.path.normpath(self.working_dir + '/' + name)
        if not image.create_from_data(idir, name, image_data, description):
            return False
        self.images.append(image)
        return True

    def get_current_image(self):
        if len(self.images):
            return self.images[-1]
        return None


class UserImageData:
    def __init__(self, dir = None, name = None, data = None, description = None):
        self.dir = None
        self.name = None
        self.path = None
        self.description_path = None
        self.previews_dir = None
        self.release_dir = None
        self.previews_paths = {}
        self.release_path = None
        if dir is not None:
            self.create_from_data(dir, name, data, description)

    def create_from_data(self, dir, name, data, description=None):
        self.dir = dir
        self.name = name
        if dir is not None:
            if not os.path.exists(dir):
                os.mkdir(dir)
                if not os.path.exists(dir):
                    return False
            self.path = dir + '/' + name + '.png'
            self.description_path = os.path.normpath(dir + '/' + name + '_description.json')
            self.previews_dir = os.path.normpath(dir + '/previews')
            self.release_dir = os.path.normpath(dir + '/release')
            self.release_path = os.path.normpath(self.release_dir + '/' + self.name + '_release.png')
            os.mkdir(self.previews_dir)
            os.mkdir(self.release_dir)

            data.save(self.path)

            self.update_previews(filters_list)

            return True

    def load_from_dir(self, dir, name):
        self.dir = dir
        entries = os.scandir(self.dir)
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.json'):
                self.description_path = entry.path
            elif entry.is_file() and entry.path.endswith(('.jpg', '.png')):
                self.path = entry.path
                self.name = str(entry.name).split('.')[0]
            elif entry.name == 'previews':
                self.previews_dir = entry.path
            elif entry.name == 'release':
                self.release_dir = entry.path
                self.release_path = os.path.normpath(self.release_dir + '/' + self.name + '_release.png')

        entries = os.scandir(self.previews_dir)
        for entry in entries:
            for filter in filters_list:
                if filter in entry.name:
                    self.previews_paths.update({filter : entry.path})
                    break

    def set_description(self, description):
        if self.description_path is None:
            if self.dir is not None and self.name is not None:
                self.description_path = self.dir + '/' + self.name + '_description.json'
            else:
                print("Error: Image: Description: description path is empty")
                return False

        with open(self.description_path, 'w') as outfile:
            json.dump(description, outfile)
        # fd = os.open(self.description_path, os.O_RDWR | os.O_CREAT | os.O_TRUNC)
        # if not os.path.exists(self.description_path):
        #     os.close(fd)
        #     print("Error: Image: Description: file not created")
        #     return False
        #
        # print(description)
        # os.write(fd, description)
        #
        # os.close(fd)

        self.update_previews(['immortal_regiment'])

        return True

    def update_previews(self, filters):
        for filter in filters:
            image = None
            if filter == 'immortal_regiment':
                print('path: ' + self.description_path)
                if self.description_path is not None and os.path.exists(self.description_path):
                    with open(self.description_path) as json_file:
                        descr = json.load(json_file)
                        fname = descr['first_name']
                        lname = descr['last_name']
                        mname = descr['last_name']
                        rank = descr['rank']
                        info = descr['info']
                        image = getattr(simple_filters, filter)(self.path, fname, lname, mname, rank)
                else:
                    image = getattr(simple_filters, filter)(self.path)
            else:
                image = getattr(simple_filters, filter)(self.path)
            image = resize_image_for_preview(image)
            path = self.previews_dir + "/" + self.name + '_' + filter + '.png'
            save_image(image, os.path.normpath(path))
            self.previews_paths.update({filter: path})

    def apply_filters(self, filters):
        if self.path is None or not os.path.exists(self.path):
            return False
        image = load_image(self.path)
        for filter in filters:
            if filter in filters_list:
                if filter == 'immortal_regiment':
                    if self.description_path is not None and os.path.exists(self.description_path):
                        with open(self.description_path) as json_file:
                            descr = json.load(json_file)
                            fname = descr['first_name']
                            lname = descr['last_name']
                            mname = descr['last_name']
                            rank = descr['rank']
                            info = descr['info']
                            image = getattr(simple_filters, filter)(image, fname, lname, mname, rank)
                    else:
                        image = getattr(simple_filters, filter)(image)
                else:
                    image = getattr(simple_filters, filter)(image)
        if image is None:
            return False

        save_image(image, self.release_path)

        return True

    def get_release_path(self):
        if self.release_path is None or not os.path.exists(self.release_path):
            return None
        return self.release_path



def get_user_data(user_id):
    entries = [str(entry.name) for entry in os.scandir(global_working_directory)]
    if user_id not in entries:
        return None
    user = UserData()
    path = os.path.normpath(os.path.abspath(global_working_directory + '/' + user_id))
    user.load_user_data(path)
    return user

def upload_user_image(user_id, image_data):
    user = get_user_data(user_id)
    if user is None:
        user = create_user(user_id)
    if user is None:
        return None
    if not user.add_image(image_data):
        return None
    return user

def create_user(user_id):
    os.mkdir(global_working_directory + '/' + user_id)
    if not os.path.isdir(os.path.normpath(global_working_directory + '/' + user_id)):
        return None
    user = UserData()
    user.load_user_data(os.path.normpath(os.path.abspath(global_working_directory + '/' + user_id)))
    return user

def to_server_path(path):
    new_path = os.path.normpath('/static/' + os.path.relpath(path, global_working_directory)).replace('\\', '/')
    return new_path
