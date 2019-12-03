import numpy as np
import cv2 as cv
import time
import socket
import math

UDP_IP1 = "127.0.0.1"
UDP_PORT1 = 5000
sock = socket.socket(socket.AF_INET, # Internet
					socket.SOCK_DGRAM) # UDP

# WTF does retval do? and what does it mean?
# Get detection with cuda running
# recompile cv2 on this machine with cuda enabled
# already verified it doesnt currently have it

# trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def detection_pink(frame_hsv):
    # Declare boundary colors for detection
    #boundaries = [([17,15,100], [50,56,200])] BGR
    #lower = np.array([([4,4,240])], dtype = "uint8")
    #upper = np.array([([211,211,255])], dtype = "uint8")
    # HSV
    #  Pink Tape
    # lower_pink = np.array([(115,50,165)], dtype = "uint8")
    # upper_pink = np.array([([160,255,255])], dtype = "uint8")
    # Paper pink
    # lower_pink = np.array([(140,1,1)], dtype = "uint8")
    # upper_pink = np.array([([145,255,255])], dtype = "uint8")
    # Green Paper
    lower_pink = np.array([(78,75,100)], dtype = "uint8")
    upper_pink = np.array([([84,150,200])], dtype = "uint8") #200

    # Check for the color pink between a certain scope of all pinks
    mask_pink = cv.inRange(frame_hsv,lower_pink,upper_pink)
    # output_pink = cv.bitwise_and(frame_hsv, frame_hsv, mask = mask_pink)

    # Turn the frame gray
    # gray_pink = cv.cvtColor(output_pink, cv.COLOR_BGR2GRAY) # Turns the frame from BGR to Grayscale

    # Find Contours
    # Typically used with a gray or black/white image
    # Set the threshhold to detect contours
    ##ret, thresh = cv.threshold(gray, 127, 255, 0)
    # ret_pink, thresh_pink = cv.threshold(gray_pink, 100, 255, 0)

    #ret, thresh = cv.threshold(gray, 100, 255, 0) #RGB
    ## image, contours, hierarchy = cv.findContours(image, mode, method)
    contours_pink = cv.findContours(mask_pink, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]
    # cv.drawContours(output_pink, contours_pink, -1, (0,255,0), 3)

    # Label the contours for the pink square
    for c in contours_pink:
        # Find contours with edges of similar lengths
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.04 * peri, True)
        print(peri)
        # Only look at contours with 4 edges and perimeters greater than 200
        if(len(approx) == 4) and (peri > 15):
            # pink_square = c
            # cv.drawContours(output_pink, [c], -1, (0,255,0), 2)
            # Find the center of the contours
            M = cv.moments(c)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
            # #    cv.imshow('frame',output_pink)
            #    cv.putText(output_pink, "middle", (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            #    cv.imshow('frame',output_pink)
            #    print(cX,",",cY)
                return cX, cY
            # return pink_square
            # return pink_square

    return -1, -1


def detection_blue(frame_hsv):
    # Declare boundary colors for detection
    # HSV
    #  Blue Marker was 95
    # lower_blue = np.array([(10,170,95)], dtype = "uint8")
    # upper_blue = np.array([([20,255,255])], dtype = "uint8")
    lower_blue = np.array([(15,110,70)], dtype = "uint8")
    upper_blue = np.array([([20,255,255])], dtype = "uint8")

    # Check for the color blue between a certain scope of all blues
    mask_blue = cv.inRange(frame_hsv,lower_blue,upper_blue)
    # output_blue = cv.bitwise_and(frame_hsv, frame_hsv, mask = mask_blue)

    # Turn the frame gray
    # gray_blue = cv.cvtColor(output_blue, cv.COLOR_BGR2GRAY)

    # Find Contours
    # Typically used with a gray or black/white image
    # Set the threshhold to detect contours
    ##ret, thresh = cv.threshold(gray, 127, 255, 0)
    # ret_blue, thresh_blue = cv.threshold(gray_blue, 100, 255, 0)

    #ret, thresh = cv.threshold(gray, 100, 255, 0) #RGB
    ## image, contours, hierarchy = cv.findContours(image, mode, method)
    contours_blue = cv.findContours(mask_blue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]
    
    # Label the contours for the blue square
    for d in contours_blue:
        # Find contours with edges of similar lengths
        peri = cv.arcLength(d, True)
        approx = cv.approxPolyDP(d, 0.04 * peri, True)

        # Only look at contours with 4 edges and perimeters greater than 200
        if (len(approx) == 4) and (peri > 15): # Used to be 44
            # print(d)
            # blue_square = d
            M = cv.moments(d)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))

                # cv.drawContours(gray_blue,d,-1,(0,255,0), 3)
                # cv.putText(frame, "middle", (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                return cX, cY
            # return blue_square
    
    return -1,-1
    # return np.array([],dtype = "uint8")

def detection_orange(frame_hsv):
    # Declare boundary colors for detection
    # HSV
    #  Orange Ball
    lower_orange = np.array([(100,100,100)], dtype = "uint8")
    upper_orange = np.array([([110,255,255])], dtype = "uint8")

    # Check for the color orange between a certain scope of all oranges
    mask_orange = cv.inRange(frame_hsv,lower_orange,upper_orange)
    # output_orange = cv.bitwise_and(frame_hsv, frame_hsv, mask = mask_orange)
    # Turn the frame gray
    # gray_orange = cv.cvtColor(frame_hsv, cv.COLOR_BGR2GRAY)
    # return gray_orange
    edges = cv.Canny(mask_orange, 450, 1529)
    rows = edges.shape[0]
  
    # Find Contours
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, rows / 8, param1=15, param2=1, minRadius=8, maxRadius=9)

    # Typically used with a gray or black/white image
    # Set the threshhold to detect contours
    ##ret, thresh = cv.threshold(gray, 127, 255, 0)
    # ret_orange, thresh_orange = cv.threshold(gray_orange, 100, 255, 0)
    #ret, thresh = cv.threshold(gray, 100, 255, 0) #RGB
    ## image, contours, hierarchy = cv.findContours(image, mode, method)
    # contours_orange = cv.findContours(thresh_orange, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]
    # print(circles)
    # if circles is not None:
    #     return circles
    # return np.array([],dtype = "uint8")
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,0:]:
            center = (i[0], i[1])
            return center
            # Circle Center
            # cv.circle(black, center, 1, (0, 100, 100), 2)
            # Cirlce Outline
            # radius = i[2]
            # cv.circle(black, center, radius, (255, 0, 255), 2)
    return (-1,-1)
    # Label the contours for the pink square
    # for o in contours_orange:
    #     # Find contours with edges of similar lengths
    #     peri = cv.arcLength(o, True)
    #     approx = cv.approxPolyDP(o, 0.04 * peri, True)

    #     # Only look at contours with 4 edges and perimeters greater than 200
    #     if(len(approx) == 4) and (peri > 200):
    #         orange_square = o

    #         return orange_square, False

# def track_blue_meanshift(frame_hsv, cX,cY):
#     # Setup initial location of window
#     x, y, w, h = cX-150, cY-150, 300, 300
#     track_window = (x, y, w, h)

#     if(x < 0):
#         x = 0
#     if(y < 0):
#         y = 0
#     # Setup the ROI for tracking
#     roi = frame_hsv[y:y+h, x:x+w]
#     # hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
#     mask = cv.inRange(roi, np.array((0., 60., 32.)), np.array((100.,255.,255.)))
#     roi_hist = cv.calcHist([roi], [0], mask, [180], [0,180])
#     cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

#     #Setup the termination criteria either 10 iteration or move by atleast 1 pt
#     term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 100, 1)

    
#     #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#     dst = cv.calcBackProject([frame_hsv], [0], roi_hist, [0,180], 1)

#     # Apply meanshift to get the new location
#     ret, track_window = cv.meanShift(dst, track_window, term_crit)
#     # print('return= ',ret)
#     # Draw it on the frame
#     x, y, w, h = track_window
#     if ret == 10 or ret == 0:
#         return x, y, w, h, True
#     return x, y, w, h, False
#     # frame2 = cv.rectangle(frame, (x,y), (x+w, y+h), 255, 2)
#     # cv.imshow('frame2',frame2)

# def track_blue(frame_hsv, cX,cY):
#     pass
 
# def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    # if trackerType == trackerTypes[0]:
    #     tracker = cv.TrackerBoosting_create()
    # elif trackerType == trackerTypes[1]: 
    #     tracker = cv.TrackerMIL_create()
    # elif trackerType == trackerTypes[2]:
    #     tracker = cv.TrackerKCF_create()
    # elif trackerType == trackerTypes[3]:
    #     tracker = cv.TrackerTLD_create()
    # elif trackerType == trackerTypes[4]:
    #     tracker = cv.TrackerMedianFlow_create()
    # elif trackerType == trackerTypes[5]:
    #     tracker = cv.TrackerGOTURN_create()
    # elif trackerType == trackerTypes[6]:
    #     tracker = cv.TrackerMOSSE_create()
    # elif trackerType == trackerTypes[7]:
    #     tracker = cv.TrackerCSRT_create()
    # else:
    #     tracker = None
    #     print('Incorrect tracker name')
    #     print('Available trackers are:')
    #     for t in trackerTypes:
    #         print(t)
        
    # return tracker
    # pass

# def track_pink(frame_hsv, blue_square):
#     pass 
    # if M["m00"] != 0:
    #            cX = int((M["m10"] / M["m00"]))
    #            cY = int((M["m01"] / M["m00"]))
    #            cv.putT
# def track_orange(frame_hsv, orange_square):
#     pass

# def draw(frame, contour_array, color):
#     if color == 'green':
#         b = 0
#         g = 255
#         r = 0
#     if color == 'red':
#         b = 0
#         g = 0
#         r = 255
#     if color == 'blue':
#         b = 255
#         g = 0
#         r = 0
#     cv.drawContours(frame, [contour_array], -1, (r,g,b), 1)
#         # Find the center of the contours
#     M = cv.moments(contour_array)
#     if M["m00"] != 0:
#         cX = int((M["m10"] / M["m00"]))
#         cY = int((M["m01"] / M["m00"]))
#         cv.putText(frame, "middle", (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
#     return frame

def main():
    #def reject(data, m = 2):
    #   return data[abs(data-np.mean(data)) < m *np.std(data)]
    # Setup the trained file for the HAAR Detector
    #square_cascade = cv.CascadeClassifier('/home/corondo/Desktop/Arena_Detection_V4/data/cascade.xml')

    # Start the video capture device
    cap = cv.VideoCapture(0)

    
    cap.set(6,cv.VideoWriter_fourcc('M','J','P','G'))
    # cap.set(3, 1920); #width
    # cap.set(4, 1080); # height
    
    cap.set(cv.CAP_PROP_FPS,30) #cv.cap_prop_fps real number is 5
    # cap.open(1)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    # Creates an object for Background Subtraction
    #fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
    fgbg = cv.createBackgroundSubtractorMOG2(history = 30, varThreshold = 50, detectShadows = True)
    for i in range(0,30):
        ret, frame1 = cap.read()
        # Crop the sides of the frame 
        frame1 = frame1[:, 135:700, :]
        gaus_frame = cv.GaussianBlur(frame1, (5, 5), 0)
        fgbg.apply(gaus_frame)
    print("ready")

    # Get FPS
    # fps = cap.get(cv.CAP_PROP_FPS)
    # print("FPS 1st images: ", fps)

    # Make the window resizeable
    # cv.namedWindow('frame', cv.WINDOW_NORMAL)

    # Set the flags
    # pink_detect = True
    # blue_detect = True
    # orange_detect = True

    # Create the tracker
        # Create the boxes
    # bboxes = []
    # colors = []
    # multiTracker = cv.MultiTracker_create()
    # blue_kcf_tracker = createTrackerByName(trackerTypes[0])
    # for bbox in bboxes:
    #     multiTracker.add(createTrackerByName(trackerTypes[2]), frame, bbox)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Crop the sides of the frame 
        frame = frame[:, 135:700, :]

        # print(frame.shape)
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return
        
        # Smooth the image
        gaus_frame1 = cv.GaussianBlur(frame, (5, 5), 0)

        # Our operations on the frame come here
        fgmask = fgbg.apply(gaus_frame1, learningRate = 0)
        output_backsub = cv.bitwise_and(gaus_frame1, gaus_frame1, mask = fgmask)
        # Change the frame from RGB to HSV
        frame_hsv = cv.cvtColor(output_backsub, cv.COLOR_RGB2HSV)
        #print(frame_hsv)
        # cXb, cYb, blue_detect = detection_blue(frame_hsv)
        # pink_square = detection_pink(frame_hsv)
        # blue_square = detection_blue(frame_hsv)
        cXp, cYp = detection_pink(frame_hsv)
        cXb, cYb = detection_blue(frame_hsv)
        circles = detection_orange(frame_hsv)

        # Create the vector
        if (cXp != -1 and cXb != -1):
            ihat = cXb - cXp
            jhat = cYb - cYp
            v = math.sqrt(((ihat)*(ihat)) + ((jhat)*(jhat)))
            # Unit vector
            unit_vector_i = round((ihat/v),6)
            unit_vector_j = round((jhat/v),6)
            # Or an angle
            if ihat > 0 and -jhat >= 0: # Angle is in quadrant 1
                angle = abs(math.degrees(math.atan(jhat/ihat)))
            elif ihat == 0 and -jhat > .98:
                angle = 90
            

            elif ihat < 0 and -jhat >= 0: # Angle is in quadrant 2
                angle_neg = abs(math.degrees(math.atan(jhat/ihat)))
                angle = 180 - angle_neg 

            elif ihat < 0 and -jhat <= 0: # Angle is in quadrant 3
                angle_neg = abs(math.degrees(math.atan(jhat/ihat)))
                angle = angle_neg + 180
            elif ihat == 0 and -jhat < -.98:
                angle = 270

            elif ihat > 0 and -jhat <= 0: # Angle is in quadrant 4
                angle_neg = abs(math.degrees(math.atan(jhat/ihat)))
                angle = 360 - angle_neg
            
            output = f'{unit_vector_i},{unit_vector_j},{cXb},{cYb},{angle},{circles[0]},{circles[1]}'
            # print(output)
            sock.sendto(output.encode(), (UDP_IP1, UDP_PORT1))

        # print(circles)
        # if len(circles) > 0:
        #     circles = np.uint16(np.around(circles))
        #     for i in circles[0,0:]:
        #         center = (i[0], i[1])
        #         # Circle Center
        #         cv.circle(black, center, 1, (0, 100, 100), 2)
        #         # Cirlce Outline
        #         radius = i[2]
        #         cv.circle(black, center, radius, (255, 0, 255), 2)
        # Draw the boxes on the frame for detection
        # blue_square = detection_blue(frame_hsv)
        # if pink_square.any():
        #     frame = draw(frame, (cXp,cYp), 'green')
        # if blue_square.any():
        #     frame = draw(frame, (cXb,cYb), 'red')
        # for c in pink:
        #     peric = cv.arcLength(c, True)
        #     approxc = cv.approxPolyDP(c, 0.04 * peric, True)
        #     if(len(approxc) == 4) and (peric > 15):
        #         if cXp != -1 and cYp != -1:
        #             cv.drawContours(frame, [c], -1, (0,255,0), 2)
        #             cv.putText(frame, "middle_pink", (cXp, cYp), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        # for d in blue:
        #     perid = cv.arcLength(d, True)
        #     approxd = cv.approxPolyDP(d, 0.04 * perid, True)
        #     if(len(approxd) == 4) and (perid > 15):
        #         if cXb != -1 and cYb != -1:
        #             cv.drawContours(frame, [d], -1, (255,0,0), 2)
        #             cv.putText(frame, "middle_blue", (cXb, cYb), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        # # Use to draw circles
        # # print(orange)
        # if orange is not None:
        #     orange = np.uint16(np.around(orange))
        #     for i in orange[0,0:]:
        #         center = (i[0], i[1])
        #         # Circle Center
        #         cv.circle(frame, center, 1, (0, 100, 100), 2)
        #         # Cirlce Outline
        #         radius = i[2]
        #         cv.circle(frame, center, radius, (255, 0, 255), 2)
        # cv.imshow('frame', frame)
        # # Used to draw edges
        # if orange is not None:
        #     orange = np.uint16(np.around(orange))
        #     for i in orange[0,0:]:
        #         center = (i[0], i[1])
        #         # Circle Center
        #         cv.circle(frame, center, 1, (0, 100, 100), 2)
        #         # Cirlce Outline
        #         radius = i[2]
        #         cv.circle(frame, center, radius, (255, 0, 255), 2)
        # cv.imshow('frame', frame)
        # if hough is not None:
        #     for i in range(0, len(hough)):
        #         rho = hough[i][0][0]
        #         theta = hough[i][0][1]
        #         a = math.cos(theta)
        #         b = math.sin(theta)
        #         x0 = a *rho
        #         y0 = b * rho
        #         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        #         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

        #         if(i < 1):
        #             cv.line(frame, pt1, pt2, (0,255,0), 1, cv.LINE_AA)
        # cv.imshow('frame', frame)

        # Display the resulting frame
        
    # Waits for the 'q' key to be pressed and quits
        if cv.waitKey(1) == ord('q'):
            # When everything done, release the capture
            cap.release()
            cv.destroyAllWindows()
            break

    
main()