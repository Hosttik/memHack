import os
import json

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
        if dir is not None:
            self.create_from_data(dir, name, data, description)

    def create_from_data(self, dir, name, data, description=None):
        self.dir = dir
        self.name = name
        if dir is not None:
            if not os.path.isdir(dir):
                os.mkdir(dir)
                if not os.path.isdir(dir):
                    return False
            self.path = dir + '/' + name + '.png'
            self.description_path = os.path.normpath(dir + '/' + name + '_description.json')
            data.save(self.path)
            return True

    def load_from_dir(self, dir, name):
        self.dir = dir
        entries = os.scandir(self.dir)
        for entry in entries:
            if entry.is_file() and entry.name == 'description.json':
                self.description_path = entry
            elif entry.is_file() and entry.path.endswith(('.jpg', '.png')):
                self.path = entry.path


def get_user_data(user_id):
    entries = [str(entry.name) for entry in os.scandir(global_working_directory)]
    if user_id not in entries:
        return None
    user = UserData()
    user.load_user_data(os.path.normpath(os.path.abspath(global_working_directory + '/' + user_id)))
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
