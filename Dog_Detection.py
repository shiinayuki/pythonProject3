import cv2 as cv
import numpy as np
import pyrealsense2 as rs
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

max_x = 0
max_center = 0
while(1):
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    # Convert images to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())
    
    hsvFrame = cv.cvtColor(color_image, cv.COLOR_BGR2HSV)
    
    # 61, 158, 145
    green_lower = np.array([55, 150, 140], np.uint8) 
    green_upper = np.array([65, 165, 155], np.uint8) 
    green_mask = cv.inRange(hsvFrame, green_lower, green_upper) 
	
	# Morphological Transform, Dilation 
	# for each color and bitwise_and operator 
	# between imageFrame and mask determines 
	# to detect only that particular color 
    kernal = np.ones((5, 5), "uint8") 
	
	# For red color 
    green_mask = cv.dilate(green_mask, kernal) 
    res_green = cv.bitwise_and(color_image, color_image, mask = green_mask) 

	# Creating contour to track red color 
    contours, hierarchy = cv.findContours(green_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.circle(color_image,(320, 240), 10, (0,0,255), 1)
    for pic, contour in enumerate(contours): 
        area = cv.contourArea(contour) 
        if(area > 200): 
            x, y, w, h = cv.boundingRect(contour)
            max_x = max(x, max_x)
            max_center = x + (int)(0.5 * w)
            cv.circle(color_image,(x + (int)(0.5 * w), y + (int)(0.5 * h)), 1, (0,0,255), -1)
            color_image = cv.rectangle(color_image, (x, y), 
									(x + w, y + h), 
									(0, 0, 255), 2)	 

    print(max_center)
    #udp_socket.sendto(max_center, (ip_remote, port_remote))
    cv.imshow("Color Detection in Real-Time", color_image)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
