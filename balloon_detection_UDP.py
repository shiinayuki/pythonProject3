from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import pyrealsense2 as rs
from pyzbar import pyzbar
import socket

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

ip_remote = '127.0.0.1'
port_remote = 32000
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# define the lower and upper boundaries of the "green"
# balloon in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=64)
time.sleep(2.0)

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = ""
    for barcode in barcodes:
        #x, y , w, h = barcode.rect

        barcode_info = barcode.data.decode('utf-8')
        #print(barcode_info)
        #cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

        # with open("barcode_result.txt", mode ='w') as file:
        #     file.write("Recognized Barcode:" + barcode_info)
    return barcode_info


while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()

    frame = np.asanyarray(color_frame.get_data())

	# resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
 	# find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
    	c = max(cnts, key=cv2.contourArea)
    	((x, y), radius) = cv2.minEnclosingCircle(c)
    	M = cv2.moments(c)
    	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
    	if radius > 10:
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
	    	
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # print(center)
            # print(int(x), int(y))
    pts.appendleft(center)
    for i in range(1, len(pts)):    
        if pts[i - 1] is None or pts[i] is None:
            continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        
    qrcode = read_barcodes(frame)
    if qrcode:
        print("QRcode: ", qrcode)
        udp_socket.sendto(bytes(qrcode, "utf-8"), (ip_remote, port_remote))
    elif center:
        print("Center: ", center)
        udp_socket.sendto(bytes(str(center[0]), "utf-8"), (ip_remote, port_remote))
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()