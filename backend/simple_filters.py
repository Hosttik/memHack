import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage.util import pad, crop

APIKEY = '01d374f9-62b3-49ef-84a1-27f6c81df358'

max_preview_size = 250

filters_list = ['upscale', 'colorize', 'immortal_regiment']
filters_names_dict = {'colorize' : "Наложение цвета", 'upscale': "Масштабирование", 'immortal_regiment': 'Бессмертный полк'}

def resize_image_for_preview(image):
    height = image.shape[0]
    width = image.shape[1]

    if height < max_preview_size and width < max_preview_size:
        return image

    ratio = max_preview_size/width if height < width else max_preview_size/height
    new_image = resize(image, (int(height*ratio), int(width*ratio)))

    return new_image

def create_img(width, height, color):
    if isinstance(color, tuple) or isinstance(color, list):
        if len(color) == 3:
            return Image.new('RGB', (width, height), color)
        else:
            return Image.new('RGBA', (width, height), color)
    return Image.new('RGB', (width, height), color)

def numpy2pil(image):
    if np.max(image) > 1:
        return Image.fromarray(np.uint8(image))
    return Image.fromarray(np.uint8(image * 255))

def load_image(filename, as_gray=False):
    return imread(filename, as_gray=as_gray)

def save_image(img, path):
    imsave(path, img)

def show_image(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def paste(img, img_back, offset):
    img = numpy2pil(img)
    img_back = numpy2pil(img_back)
    result = img_back.copy()
    result.paste(img, offset, img)
    return np.array(result)

def load_image_by_url(url, as_gray=False):
    return imread(url, as_gray=as_gray)

def colorize(image):
    if not isinstance(image, str):
        save_image(image, 'temp/temp.jpg')
        image = 'temp/temp.jpg'

    print('Colorizing image...')
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={
            'image': open(image, 'rb'),
        },
        headers={'api-key': APIKEY}
    )
    d = r.json()
    return load_image(d['output_url'])

def upscale(image):
    if not isinstance(image, str):
        save_image(image, 'temp/temp.jpg')
        image = 'temp/temp.jpg'

    print('Upscaling image...')
    r = requests.post(
        "https://api.deepai.org/api/torch-srgan",
        files={
            'image': open(image, 'rb'),
        },
        headers={'api-key': '01d374f9-62b3-49ef-84a1-27f6c81df358'}
    )
    d = r.json()
    return load_image(d['output_url'])

def to_square(image):
    width, height = image.shape[1], image.shape[0]
    min_size = min(width, height)
    dw_left = (width - min_size) // 2
    dw_right = width - min_size - dw_left
    dh_top = (height - min_size) // 2
    dh_bottom = height - min_size - dh_top
    if len(image.shape) == 2:
        return crop(image, ((dh_top, dh_bottom), (dw_left, dw_right)))
    return crop(image, ((dh_top, dh_bottom), (dw_left, dw_right), (0, 0)))

def draw_text(img, text, topleft, fontname='arial', fontsize=24, textcolor=(0, 0, 0)):
    img = numpy2pil(img)
    font = ImageFont.truetype(font=fontname, size=fontsize)
    draw = ImageDraw.Draw(img)
    draw.text(topleft, text, fill=textcolor, font=font)
    return np.array(img)

def img_text(text, fontname='arial', fontsize=24, textcolor=(0, 0, 0)):
    font = ImageFont.truetype(font=fontname, size=fontsize)
    w, h = font.getsize(text)
    img = create_img(2 * w, 2 * h, (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill=textcolor, font=font)

    data = 255 - np.array(img)
    left = 0
    for i in range(data.shape[1]):
        if np.sum(data[:, i, :]) > 0:
            left = i
            break
    right = data.shape[1] - 1
    for i in range(data.shape[1]):
        if np.sum(data[:, data.shape[1] - 1 - i, :]) > 0:
            right = data.shape[1] - 1 - i
            break
    top = 0
    for i in range(data.shape[0]):
        if np.sum(data[i, :, :]) > 0:
            top = i
            break
    bottom = data.shape[0] - 1
    for i in range(data.shape[0]):
        if np.sum(data[data.shape[0] - 1 - i, :, :]) > 0:
            bottom = data.shape[0] - 1 - i
            break

    data = 255 - data[top:bottom + 1, left:right + 1, :]
    return Image.fromarray(data)

def get_text_size(text, fontname='arial', fontsize=24):
    img = img_text(text, fontname=fontname, fontsize=fontsize)
    return img.size

# def crop_resize(image, size):
#     ratio_before = image.shape[1] / image.shape[0]
#     ratio_after = size[0] / size[1]


def immortal_regiment(image, first_name=None, last_name=None, middle_name=None, rank=None):
    if isinstance(image, str):
        image = load_image(image)

    template = imread('template/polk_1.png') # 3543 x 4724

    top_left = (446, 314)
    width, height = 2635, 3437
    text_start_1 = 3800
    text_start_2 = 4150
    text_start_3 = 4496
    margin = 300
    fontname = 'arial'
    fontsize = 300

    def add_text_to_line(img, text, ypos, font_size):
        delta = 0
        text_width = img.shape[1]
        left = 0
        while text_width + 2 * margin > img.shape[1]:
            text_size = get_text_size(text, fontname=fontname, fontsize=font_size - delta)
            text_width = text_size[0]
            left = (img.shape[1] - text_width - 2 * margin) // 2 + margin
            delta += 10
        return draw_text(img, text, (left, ypos), fontname=fontname, fontsize=font_size)

    image = upscale(image)

    if image.shape[1] > image.shape[0]:
        image = to_square(image)

    print('Resizing..')
    image = resize(image, (height, width)) * 255

    print('Adding borders..')
    border_left = top_left[0]
    border_right = template.shape[1] - width - border_left
    border_top = top_left[1]
    border_bottom = template.shape[0] - height - border_top
    image = pad(image, ((border_top, border_bottom), (border_left, border_right), (0, 0)), mode='constant', constant_values=255)

    print('Merging images..')
    image = paste(template, image, (0, 0))

    print('Adding text..')
    if last_name is not None:
        image = add_text_to_line(image, last_name.upper(), text_start_1, fontsize)
    s = ''
    if first_name is not None:
        s += first_name
    if middle_name is not None:
        s += ' {}'.format(middle_name)
    if len(s) > 0:
        image = add_text_to_line(image, s, text_start_2, fontsize)
    if rank is not None:
        image = add_text_to_line(image, 'Звание: {}'.format(rank), text_start_3, int(0.6 * fontsize))

    return image