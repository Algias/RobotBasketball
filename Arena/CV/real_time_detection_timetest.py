import numpy as np
import cv2 as cv
import time
import socket
import math

def main():
    # start = time.time()
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS,30)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    fgbg = cv.createBackgroundSubtractorMOG2(history = 30, varThreshold = 50, detectShadows = True)
    for i in range(0,10):
        ret, frame1 = cap.read()
        fgbg.apply(frame1, learningRate=.5)
    print("ready")
    # end = time.time()
    # print(end - start)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Crop the sides of the frame 
        frame = frame[:, 100:700, :]
        cv.namedWindow('frame', cv.WINDOW_NORMAL)

        # print(frame.shape)
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return
        
        # Our operations on the frame come here
        fgmask = fgbg.apply(frame, learningRate = 0)
        output_backsub = cv.bitwise_and(frame, frame, mask = fgmask)

        cv.imshow('frame', output_backsub)
        if cv.waitKey(1) == ord('q'):
            # When everything done, release the capture
            cap.release()
            cv.destroyAllWindows()
            break

main()