# https://docs.opencv.org/4.x/da/d13/tutorial_aruco_calibration.html
# data: https://drive.google.com/file/d/12IWsHiERr0xGrcAPe9VCkWNMrqEmI3fF/view?usp=drive_link
import cv2 as cv
import os

aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_100)
board = cv.aruco.CharucoBoard((5, 7),
                              squareLength=110,
                              markerLength=72,
                              dictionary=aruco_dict)
detector = cv.aruco.CharucoDetector(board)

obj_points = []
img_points = []
for path in os.listdir("images"):
    img = cv.imread(f"images\\{path}")

    corners, charucoIds, _, _ = detector.detectBoard(img)

    #cv.aruco.drawDetectedCornersCharuco(img, corners, charucoIds=charucoIds)
    #cv.imwrite(f"debug\\{path}.jpg", img)

    if corners is not None and len(corners) > 0:
        frame_obj_points, frame_img_points = board.matchImagePoints(corners, charucoIds)
        if len(frame_obj_points) > 4:
            obj_points.append(frame_obj_points)
            img_points.append(frame_img_points)

print("Start calibration")
rms, camera_matrix, dist_coefs, _, _ = cv.calibrateCamera(obj_points,
                                                          img_points,
                                                          (960, 1280),
                                                          None,
                                                          None)
print(rms)
print(camera_matrix)
print(dist_coefs)