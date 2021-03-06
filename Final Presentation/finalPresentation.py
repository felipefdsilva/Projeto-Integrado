# import the necessary packages
from collections import deque
import numpy as np
import imutils
import math
import serial
import time
import cv2

# Field Settings --------------------

class Mic(object):
    def __init__(self, wing, x, y):
        self.wing = wing.upper();
        self.x = x;
        self.y = y;

    angle = 0;

def GetMicAngle (xTarget, yTarget, wing, xMic, yMic):

    if (wing == "SOUTH"):
        if (xTarget == xMic):
            return 90;
        elif (xTarget > xMic):
            angle = math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);
        else:
            angle = 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);

    elif (wing == "NORTH"):
        if (xTarget == xMic):
            return 90;
        elif (xTarget > xMic):
            angle = 180-math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);
        else:
            angle = math.fabs(math.degrees(math.atan((yTarget-yMic)/(xTarget-xMic))));
            return math.trunc(angle);

    elif (wing == "EAST"):
        if (yTarget == yMic):
            return 90;
        angle = GetMicAngle (yTarget, xTarget, "NORTH", yMic, xMic);
        return angle;

    elif (wing == "WEST"):
        if (yTarget == yMic):
            return 90;
        angle = 180-GetMicAngle (yTarget, xTarget, "NORTH", yMic, xMic);
        return angle;

    else:
        return "Error";

northMic = Mic ('North', 310, 0);
eastMic = Mic ('East', 593, 208);
southMic = Mic ('South', 298, 447);
westMic = Mic ('West', 0, 207);


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# Hint: use the "rangeDetector.py" program to set the color range

#Red_1 in HSV
redLower = (113, 88, 245);
redUpper = (255, 255, 255);
#Red_2 in HSV
#redLower = (113, 88, 245);
#redUpper = (255, 255, 122);

pts = deque(maxlen=64);

camera = cv2.VideoCapture(1);

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read();
		#grabbed == boolean

	# resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600);
	blurred = cv2.GaussianBlur(frame, (11, 11), 0); #reduce high frequency noise
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV);

	# construct a mask for the color "red", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, redLower, redUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2];
	center = None;

	(x,y) = (0,0);
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)

		# To print current ball position
		#print ((x,y));

		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

		# Set Mic Angles
		(xTarget,yTarget) = (x, y);
		northMic.angle = GetMicAngle (xTarget, yTarget, northMic.wing, northMic.x, northMic.y);
		eastMic.angle = GetMicAngle (xTarget, yTarget, eastMic.wing, eastMic.x, eastMic.y);
		southMic.angle = GetMicAngle (xTarget, yTarget, southMic.wing, southMic.x, southMic.y);
		westMic.angle = GetMicAngle (xTarget, yTarget, westMic.wing, westMic.x, westMic.y);

		text = str(northMic.angle) + ';' + str(eastMic.angle) + ';' + str(southMic.angle) + ';' + str(westMic.angle) + ';';
		textToPrint = "["+str(int(x))+";"+str(int(y))+"]"+ "  " + text;

	else:
		text = "90;90;90;90";
		textToPrint = "No points to center. " + text;

	# update the points queue
	pts.appendleft(center)


	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	#cv2.putText(target, text, coordinates, font, font_size, text_color, text_thickness, type_of_line)
	cv2.putText(frame,textToPrint, (10,25), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1);

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break;
	if key == ord("s"):
		print "Saving frame...";
		cv2.imwrite('finalPresentation.png',frame);
		print "Frame Saved";

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
