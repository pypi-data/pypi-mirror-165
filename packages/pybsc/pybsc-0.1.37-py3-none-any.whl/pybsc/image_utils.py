from __future__ import division

import base64

import cv2
import numpy as np
import PIL

from pybsc.tile import squared_tile


try:
    from turbojpeg import TurboJPEG
    jpeg = TurboJPEG()
except Exception:
    jpeg = None


def pil_to_cv2_interpolation(interpolation):
    if isinstance(interpolation, str):
        interpolation = interpolation.lower()
        if interpolation == 'nearest':
            cv_interpolation = cv2.INTER_NEAREST
        elif interpolation == 'bilinear':
            cv_interpolation = cv2.INTER_LINEAR
        elif interpolation == 'bicubic':
            cv_interpolation = cv2.INTER_CUBIC
        elif interpolation == 'lanczos':
            cv_interpolation = cv2.INTER_LANCZOS4
        else:
            raise ValueError(
                'Not valid Interpolation. '
                'Valid interpolation methods are '
                'nearest, bilinear, bicubic and lanczos.')
    else:
        if interpolation == PIL.Image.NEAREST:
            cv_interpolation = cv2.INTER_NEAREST
        elif interpolation == PIL.Image.BILINEAR:
            cv_interpolation = cv2.INTER_LINEAR
        elif interpolation == PIL.Image.BICUBIC:
            cv_interpolation = cv2.INTER_CUBIC
        elif interpolation == PIL.Image.LANCZOS:
            cv_interpolation = cv2.INTER_LANCZOS4
        else:
            raise ValueError(
                'Not valid Interpolation. '
                'Valid interpolation methods are '
                'PIL.Image.NEAREST, PIL.Image.BILINEAR, '
                'PIL.Image.BICUBIC and PIL.Image.LANCZOS.')
    return cv_interpolation


def decode_image_cv2(b64encoded):
    bin = b64encoded.split(",")[-1]
    bin = base64.b64decode(bin)
    bin = np.frombuffer(bin, np.uint8)
    img = cv2.imdecode(bin, cv2.IMREAD_COLOR)
    return img


def decode_image_turbojpeg(b64encoded):
    bin = b64encoded.split(",")[-1]
    bin = base64.b64decode(bin)
    img = jpeg.decode(bin)
    return img


def decode_image(b64encoded):
    if jpeg is not None:
        img = decode_image_turbojpeg(b64encoded)
    else:
        img = decode_image_cv2(b64encoded)
    return img


def encode_image_turbojpeg(img):
    bin = jpeg.encode(img)
    b64encoded = base64.b64encode(bin).decode('ascii')
    return b64encoded


def encode_image_cv2(img, quality=90):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', img, encode_param)
    b64encoded = base64.b64encode(encimg).decode('ascii')
    return b64encoded


def encode_image(img):
    if jpeg is not None:
        img = encode_image_turbojpeg(img)
    else:
        img = encode_image_cv2(img)
    return img


def resize_keeping_aspect_ratio(img, width=None, height=None,
                                interpolation='bilinear'):
    if (width and height) or (width is None and height is None):
        raise ValueError('Only width or height should be specified.')
    if width == img.shape[1] and height == img.shape[0]:
        return img
    if width:
        height = width * img.shape[0] / img.shape[1]
    else:
        width = height * img.shape[1] / img.shape[0]
    height = int(height)
    width = int(width)
    cv_interpolation = pil_to_cv2_interpolation(interpolation)
    return cv2.resize(img, (width, height),
                      interpolation=cv_interpolation)


def resize_keeping_aspect_ratio_wrt_longside(img, length,
                                             interpolation='bilinear'):
    H, W = img.shape[:2]
    aspect = W / H
    cv_interpolation = pil_to_cv2_interpolation(interpolation)
    if H > W:
        width = length * aspect
        return cv2.resize(img, (int(width), int(length)),
                          interpolation=cv_interpolation)
    else:
        height = length / aspect
        return cv2.resize(img, (int(length), int(height)),
                          interpolation=cv_interpolation)


def resize_keeping_aspect_ratio_wrt_target_size(
        img, width, height, interpolation='bilinear',
        background_color=(0, 0, 0)):
    if width == img.shape[1] and height == img.shape[0]:
        return img
    H, W, _ = img.shape
    ratio = min(float(height) / H, float(width) / W)
    M = np.array([[ratio, 0, 0],
                  [0, ratio, 0]], dtype=np.float32)
    dst = np.zeros((int(height), int(width), 3), dtype=img.dtype)
    return cv2.warpAffine(
        img, M,
        (int(width), int(height)),
        dst,
        cv2.INTER_CUBIC, cv2.BORDER_CONSTANT,
        background_color)


def squared_padding_image(img, length=None):
    H, W = img.shape[:2]
    if H > W:
        if length is not None:
            img = resize_keeping_aspect_ratio_wrt_longside(img, length)
        margin = img.shape[0] - img.shape[1]
        img = np.pad(img,
                     [(0, 0),
                      (margin // 2, margin - margin // 2),
                      (0, 0)], 'constant')
    else:
        if length is not None:
            img = resize_keeping_aspect_ratio_wrt_longside(img, length)
        margin = img.shape[1] - img.shape[0]
        img = np.pad(img,
                     [(margin // 2, margin - margin // 2),
                      (0, 0), (0, 0)], 'constant')
    return img


def concat_with_keeping_aspect(
        imgs, width, height,
        tile_shape=None):
    if len(imgs) == 0:
        raise ValueError
    if tile_shape is None:
        tile_x, tile_y = squared_tile(len(imgs))
    else:
        tile_x, tile_y = tile_shape

    w = width // tile_x
    h = height // tile_y

    ret = []
    max_height = h
    max_width = w
    for img in imgs:
        if img.shape[1] / w > img.shape[0] / h:
            tmp_img = resize_keeping_aspect_ratio(img, width=w, height=None)
        else:
            tmp_img = resize_keeping_aspect_ratio(img, width=None, height=h)
        ret.append(tmp_img)

    canvas = np.zeros((height, width, 3),
                      dtype=np.uint8)

    i = 0
    for y in range(tile_y):
        for x in range(tile_x):
            lh = (max_height - ret[i].shape[0]) // 2
            rh = (max_height - ret[i].shape[0]) - lh
            lw = (max_width - ret[i].shape[1]) // 2
            rw = (max_width - ret[i].shape[1]) - lw
            img = np.pad(ret[i],
                         [(lh, rh),
                          (lw, rw),
                          (0, 0)], 'constant')
            canvas[y * max_height:(y + 1) * max_height,
                   x * max_width:(x + 1) * max_width] = img
            i += 1
            if i >= len(imgs):
                break
        if i >= len(imgs):
            break
    return canvas


def masks_to_bboxes(mask):
    R, _, _ = mask.shape
    instance_index, ys, xs = np.nonzero(mask)
    bboxes = np.zeros((R, 4), dtype=np.float32)
    for i in range(R):
        ys_i = ys[instance_index == i]
        xs_i = xs[instance_index == i]
        if len(ys_i) == 0:
            continue
        y_min = ys_i.min()
        x_min = xs_i.min()
        y_max = ys_i.max() + 1
        x_max = xs_i.max() + 1
        bboxes[i] = np.array(
            [x_min, y_min, x_max, y_max],
            dtype=np.float32)
    return bboxes
