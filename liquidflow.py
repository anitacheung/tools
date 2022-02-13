"""
Liquidflow

References
- 
"""
from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
import cv2
import jenkspy
import pandas as pd

def parse_argument():
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
	#default=[0.5,0.85,0.45,0.8]
	ap.add_argument("-d", "--dims", action="append", help="factors to apply to x1, x2, y1, y2")
	ap.add_argument("-t", "--threshold", default=25, help="lower limit of threshold")
	args = vars(ap.parse_args())
	args = vars(ap.parse_args())
	# if the video argument is None, then we are reading from webcam
	if args.get("video", None) is None:
		vs = VideoStream(src=0).start()
		time.sleep(2.0)
	else:
		vs = cv2.VideoCapture(args["video"])
	return vs, args["min_area"], args["dims"], args["threshold"]

def process_video(vs, min_area, dims, threshold):
	firstFrame = None
	kernel_size = 21
	return vs, args["min_area"]

def process_video(vs, min_area):
	firstFrame = None
	kernel_size = 5
	minLineLength = 50
	maxLineGap = 35
	flowWidth = 25
	breaks = np.array([i for i in range(0,900,96)]) - flowWidth
	threshold = int(threshold)

	while True:
		frame = vs.read()
		frame = frame[1]
		text = "0"

		# Error Handling
		if frame is None:
			break

		# Truncate to location of interest
		y = vs.get(cv2.CAP_PROP_FRAME_WIDTH)
		x = vs.get(cv2.CAP_PROP_FRAME_HEIGHT)
		frame = frame[int(x/2):int(x*0.85), int(y*0.45):int(y * 0.8)]

		# Color Corrections
		frame = imutils.resize(frame, width=1000)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
		if firstFrame is None:
			firstFrame = gray
			continue

		# Track Movement
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)		# fill in holes
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# Get lines
		this_frame = thresh
		present_frame = frame
		cannyed = cv2.Canny(this_frame, 200, 300)
		lines = cv2.HoughLinesP(cannyed,
								rho = 6,
								theta=np.pi/180,
								threshold=20,
								lines=np.array([]),
								minLineLength=minLineLength,
								maxLineGap=maxLineGap)

		try:
			otherlines = lines[(lines[:,0,2]-lines[:,0,0]>=flowWidth) &
								(lines[:,0,1]-lines[:,0,3]>=minLineLength)]
			lines = lines[np.absolute(lines[:,0,2]-lines[:,0,0])<flowWidth]
			if (len(lines) > 1):
				lines[lines[:,0,0]>x*2,0,0] = x*2
				lines[lines[:,0,2]>x*2,0,2] = x*2
				
				# Jenks Natural Breaks - Need to Fix
				#startpoint = np.array(lines[:,0,0])
				#breaks = np.array(jenkspy.jenks_breaks(startpoint, nb_class=min(7, lines.size)))
				#totalBreaks = np.vstack([totalBreaks,breaks])
				#breaks = totalBreaks.mean(axis=0).astype(int)

				# Manual Natural Breaks
				lines[:,0,0] = breaks[np.digitize(lines[:,0,0],breaks,right=False)-1] + flowWidth
				lines[:,0,2] = breaks[np.digitize(lines[:,0,2],breaks,right=False)-1] + flowWidth
				text = np.count_nonzero(np.unique(lines[:,0,0]))

			# Show fluid flow
			for line in lines:
				for x1, y1, x2, y2 in line:
					cv2.line(img=present_frame, pt1=(x1,y1), pt2=(x2,y2), color=(255,0,0), thickness=3, lineType=8)

			for line in otherlines:
				for x1, y1, x2, y2 in line:
					cv2.line(img=present_frame, pt1=(x1,y1), pt2=(x2,y2), color=(0,0,255), thickness=3, lineType=8)
		except:
			pass

		# Show movement
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < min_area:
				continue
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			w = int(w/2)
			h = int(h/2)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			
			# draw the text and timestamp on the frame
			cv2.putText(frame, "Channels Detected: {}".format(text), (10, 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
				(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
			# show the frame and record if the user presses a key
			cv2.imshow("Security Feed", frame)
			#cv2.imshow("Thresh", thresh)
			#cv2.imshow("Frame Delta", frameDelta)
			key = cv2.waitKey(1) & 0xFF
			# if the `q` key is pressed, break from the loop
			if key == ord("q"):
				break

	vs.release()
	cv2.destroyAllWindows()

def main():
	vs, min_area, dims, threshold = parse_argument()
	process_video(vs, min_area, dims, threshold)

if __name__ == "__main__":
	main()