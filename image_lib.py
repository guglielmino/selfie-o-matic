# coding=utf-8

# Progetto	: Unknown
# Note		: Image manipulation


import cv2
from cv2 import VideoCapture
import numpy as np

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    pass

from PIL import Image

__author__ = "Fabrizio Guglielmino"


def overlay_image_old(original, mark):
	orig_h, orig_w = original.shape[:2]
	mark_h, mark_w = mark.shape[:2]

	overlay = np.zeros_like(original, "uint16")

	mark_y = (orig_h - mark_h) / 2
	mark_x = (orig_w - mark_w) / 2

	overlay[mark_y:mark_h+mark_y, mark_x:mark_w+mark_x] = mark

	return np.array(np.clip(original + overlay, 0, 255), "uint8")

def overlay_pil_image_pi(camera, mask):
	pad = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))

	pad.paste(img, (0, 0))

	o = camera.add_overlay(pad.tostring(), size=img.size)
	o.alpha = 255
	o.layer = 3

def overlay_np_image_pi(camera, mask):
	camera.add_overlay(np.getbuffer(mask), layer=3, alpha=128)


def overlay_image(original, mark):
	orig_h, orig_w = original.shape[:2]
	# Region of interest
	mark_h, mark_w,channels = mark.shape

	mark_y = (orig_h - mark_h) / 2
	mark_x = (orig_w - mark_w) / 2

	#roi = original[0:mark_h, 0:mark_w ]
	roi = original[mark_y:mark_h+mark_y, mark_x:mark_w+mark_x]

	img2gray = cv2.cvtColor(mark,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)
	# Black della ROI
	img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
	# Estrazione della parte interessare
	img2_fg = cv2.bitwise_and(mark,mark,mask = mask)

	# Creazione dell'immagine da sovraimporre
	dst = cv2.add(img1_bg,img2_fg)

	original[mark_y:mark_h+mark_y, mark_x:mark_w+mark_x] = dst

	return original


def fadein(img1, img2, fade_value): 
	fadein = fade_value/10.0
	return cv2.addWeighted(img1, fadein, img2, fadein, 0)


def create_empty_image(height, width, color):
	blank_image = np.zeros((height,width,3), np.uint8)
	blank_image[:] = color

	return blank_image
