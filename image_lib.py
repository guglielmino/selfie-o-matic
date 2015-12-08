# coding=utf-8

# Progetto	: Self-O-Matic
# Note		: Image manipulation


import numpy as np
import logging

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

from PIL import Image

__author__ = "Fabrizio Guglielmino"


def overlay_pil_image_pi(camera, mask):
    pad = Image.new('RGB', (
        ((camera.resolution[0] + 31) // 32) * 32,
        ((camera.resolution[1] + 15) // 16) * 16,
    ), "#fff")

    x_pos = (camera.resolution[0] - mask.size[0]) // 2
    y_pos = (camera.resolution[1] - mask.size[1]) // 2
    pad.paste(mask, (x_pos, y_pos))

    return camera.add_overlay(pad.tobytes(), size=camera.resolution, layer=3, alpha=255)


def overlay_np_image_pi(camera, mask):
    camera.add_overlay(np.getbuffer(mask), layer=3, alpha=128)


def create_empty_image_pil(height, width, color):
    return Image.new('RGB', (height, width), color)


def watermark_image(image_original, watermark_image):
    if image_original.mode != 'RGBA':
        image_original = image_original.convert('RGBA')

    layer = Image.new('RGBA', image_original.size, (0, 0, 0, 0))
    layer.paste(watermark_image, (0, 0))

    return Image.composite(layer, image_original, layer)


def resize_image_height(image_file, output_file, height):
    baseheight = height
    img = Image.open(image_file)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)

    img.save(output_file)
