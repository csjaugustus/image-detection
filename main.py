import cv2
import numpy as np
import pyautogui
from random import choice
from win32gui import GetForegroundWindow, GetWindowRect
import time
import os

def base_detect_image(template_file_name, threshold = 0.9):
	"""
	A base detection algorithm that detects images through template matching.
	Takes an image file name, a threshold value specifiying detection accuracy,
	and returns the (x_min, x_max, y_min, y_max) of the nearest detected image.
	Does not distinguish between colours.
	"""
	if not os.path.exists(template_file_name):
		raise FileNotFoundError

	ss = pyautogui.screenshot()
	img_rgb = cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread(template_file_name, 0)

	# Store width and height of template in w and h
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	loc = np.where( res >= threshold )
	if len(loc[0]) > 0:
		ranges = [] # (x_min, x_max, y_min, y_max)
		for pt in zip(*loc[::-1]):
			ranges.append((pt[0], pt[0] + w, pt[1], pt[1]+h))
		current_x = list(pyautogui.position())[0]
		current_y = list(pyautogui.position())[1]
		return sorted(ranges, key = lambda i: min(abs(i[0]-current_x),abs(i[2]-current_y)))[0] #return the closest detection

	else:
		return False

def detect_image(template_file_name, delay=3, threshold=0.9):
	"""
	Takes an image file name, a delay (if a wait time may be needed for image to appear) a threshold value specifying detection accuracy,
	and returns the center coords of the nearest detected image.
	Returns False if image is undetected.
	"""
	t = 0
	while not base_detect_image(template_file_name, threshold=threshold):
		time.sleep(0.1)
		t += 0.1
		if t >= delay:
			print(f"{template_file_name} undetected.")
			return
	x1, x2, y1, y2 = base_detect_image(template_file_name, threshold=threshold)
	center_x = (x1 + x2)/2
	center_y = (y1 + y2)/2
	return (center_x, center_y)

def click_image(template_file_name, delay=3, double=False, threshold=0.9):
	"""
	Takes an image file name, a delay (if a wait time may be needed for image to appear) a threshold value specifying detection accuracy,
	clicks (optionally double clicks) the center of detected image, and returns the center coords of the nearest detected image.
	Returns False if image is undetected.
	"""
	try:
		center_x, center_y = detect_image(template_file_name, delay=delay, threshold=threshold)
	except TypeError:
		return False
	pyautogui.moveTo(center_x, center_y)
	if double:
		pyautogui.doubleClick()
	else:
		pyautogui.click()

	return (center_x, center_y)

def move_to_image(template_file_name, delay=3, threshold=0.9):
	"""
	Takes an image file name, a delay (if a wait time may be needed for image to appear) a threshold value specifying detection accuracy,
	moves cursor to the center of detected image, and returns the center coords of the nearest detected image.
	Returns False if image is undetected.
	"""
	try:
		center_x, center_y = detect_image(template_file_name, delay=delay, threshold=threshold)
	except TypeError:
		return False
	pyautogui.moveTo(center_x, center_y)

	return (center_x, center_y)

def crop_full(detected, left, right, top, bottom):
	"""
	Takes a detected image (returned result of a detection), and returns a larger screenshot which includes image surrounding detected image.
	The left right top bottom values specify how large the surrounding image should be.
	"""
	x_min, x_max, y_min, y_max = detected
	ss = pyautogui.screenshot()
	cropped = ss.crop((x_min-80, y_min-50, x_max+100, y_max+15))
	return cropped

def main():
	move_to_image("example.png")

if __name__ == "__main__":
	main()
