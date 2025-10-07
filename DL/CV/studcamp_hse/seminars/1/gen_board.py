# https://docs.opencv.org/4.x/df/d4a/tutorial_charuco_detection.html
import cv2 as cv

cols = 5
rows = 7
squareLength = 100
markerLength = 65
margin = squareLength - markerLength

aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_100)
board = cv.aruco.CharucoBoard((cols, rows), squareLength=squareLength, markerLength=markerLength, dictionary=aruco_dict)
img = board.generateImage((cols*squareLength + 2 * margin, rows*squareLength + 2 * margin), margin)
cv.imwrite("img.png", img)