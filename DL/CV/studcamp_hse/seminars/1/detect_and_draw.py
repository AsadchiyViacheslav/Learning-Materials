# https://github.com/opencv/opencv/blob/4.x/samples/python/aruco_detect_board_charuco.py
import numpy as np
import cv2 as cv

aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_100)
board = cv.aruco.CharucoBoard((5, 7), squareLength=0.035, markerLength=0.023, dictionary=aruco_dict)
detector = cv.aruco.CharucoDetector(board)

img = cv.imread("1\\images\\2.jpg")

corners, charucoIds, markerCorners, markerIds = detector.detectBoard(img)
cv.aruco.drawDetectedMarkers(img, markerCorners)
cv.aruco.drawDetectedCornersCharuco(img, corners)

frame_obj_points, frame_img_points = board.matchImagePoints(corners, charucoIds)

camera_matrix = np.array([[984.68630771,   0.,         479.32526648],
 [  0.,         985.07648021, 642.04072255],
 [  0.,           0.,           1.        ]])

dist_coeffs = np.array([[ 1.40327092e-01,-7.56241483e-01 ,1.12768928e-03,-4.88750897e-04, 1.31331599e+00]])
_, rvec, tvec = cv.solvePnP(frame_obj_points, frame_img_points, camera_matrix, dist_coeffs)

cv.drawFrameAxes(img, camera_matrix, dist_coeffs, rvec, tvec, length=0.035 * 3, thickness=3)

cv.imwrite("debug\\axes.jpg", img)