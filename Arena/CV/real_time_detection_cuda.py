import numpy as np
import cv2 as cv
import time
import socket
import math
import time


def detection_pink(frame_hsv):
    pass

def detection_blue(frame_hsv):
    pass

def detection_orange(frame_hsv):
    pass

def draw(frame, contour_array, color):
    pass

def main():
    start = time.time()
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS,30)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    cuMat = cv.cuda_GpuMat()

    fgbg = cv.cuda.createBackgroundSubtractorMOG2(history = 30, varThreshold = 50, detectShadows = True)
    retval = cv.cuda.Stream_Null()
    for i in range(0,10):
        ret, frame1 = cap.read()
        frame1 = frame1[:, 100:700, :]
        cuMat.upload(frame1)
        fgbg.apply(cuMat, learningRate=.5, stream=retval)
    print("ready")
    end = time.time()
    print(end - start)

    cuMat2 = cv.cuda_GpuMat()
    # cuMat.upload()
    while(True):
        ret, frame = cap.read()
        frame = frame[:, 100:700, :]
        # cv.namedWindow('frame', cv.WINDOW_NORMAL)
        
        cuMat.upload(frame)

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return

        fgmask = fgbg.apply(cuMat, learningRate = 0, stream=retval)
        # print(fgmask)
        # print(fgmask.size(),",",cuMat.size()) # Frame Size
        print(fgmask.shape(),",",cuMat.shape())
        output_backsub = cv.cuda.bitwise_and(cuMat, cuMat, mask=[fgmask, fgmask, fgmask])
        # output_backsub1 = cv.cuda_GpuMat.download(output_backsub)
        # cuMat2.upload(output_backsub)
        # frame_hsv = cv.cuda.cvtColor(output_backsub, cv.COLOR_RGB2HSV)
        # cXp, cYp = detection_pink(frame_hsv)
        # cXb, cYb = detection_blue(frame_hsv)

        # cv.imshow('frame', output_backsub1)
        # if cv.waitKey(1) == ord('q'):
        #     # When everything done, release the capture
        #     cap.release()
        #     cv.destroyAllWindows()
        #     break

main()

# setDevice()
# if not cv.cuda.getCudaEnabledDeviceCount():
#     self.skipTest("No CUDA-capable device is detected")

# Base storage class for GPU memory with reference counting
# Doesn't require any arguments?
# cuMat = cv.cuda_GpuMat()

# Performs data upload to GpuMat
# void upload(InputArray arr)	
    # This function copies data from host memory to device memory.
    # As being a blocking call, it is guaranteed that the copy operation
    # is finished when this function returns.
# void 	upload(InputArray arr, Stream &stream)
    # This function copies data from host memory to device memory.
    # As being a non-blocking call, this function may return even if the copy
    # operation is not finished. The copy operation may be overlapped with operations
    # in other non-default streams if stream is not the default stream and dst
    # is HostMem allocated with HostMem::PAGE_LOCKED option.
# cuMat.upload()

# Same as without CUDA
# cv.cuda.createBackgroundSubtractorMOG2 (int history=500, double varThreshold=16, bool detectShadows=true)
# bgsub = cv.cuda.createBackgroundSubtractorMOG2()

# Same as without CUDA
# cuMat2 = cv.cuda.cvtColor(cuMat2, cv.COLOR_RGB2GRAY)

