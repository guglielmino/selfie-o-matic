# coding=utf-8

# Progetto	: Unknown
# Note		: Image manipulation


import cv2
from cv2 import VideoCapture
import numpy as np

__author__ = "Fabrizio Guglielmino"


def overlay_image(original, mark):
	orig_h, orig_w = original.shape[:2]
	mark_h, mark_w = mark.shape[:2]

	overlay = np.zeros_like(original, "uint16")

	mark_y = (orig_h - mark_h) / 2
	mark_x = (orig_w - mark_w) / 2

	overlay[mark_y:mark_h+mark_y, mark_x:mark_w+mark_x] = mark

	return np.array(np.clip(original + overlay, 0, 255), "uint8")

def fadein_images(img1, img2): 
	for IN in range(0,10):
		fadein = IN/10.0
		dst = cv2.addWeighted( img1, fadein, img2, fadein, 0)
		ime.sleep(0.05)
		if fadein == 1.0: #blendmode mover
			fadein = 1.0
		return dst

def fadein(img1, img2, fade_value): 
	fadein = fade_value/10.0
	return cv2.addWeighted(img1, fadein, img2, fadein, 0)


def create_empty_image(height, width, color):
	blank_image = np.zeros((height,width,3), np.uint8)
	blank_image[:] = color

	return blank_image
