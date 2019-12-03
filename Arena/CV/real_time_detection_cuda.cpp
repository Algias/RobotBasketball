// #include <opencv2/gpu.hpp>  // GPU structures and methods
#include <iostream>
#include <opencv2/videoio.hpp>
#include <cmath>
#include <opencv2/video/background_segm.hpp>
#include <opencv2/highgui.hpp>
#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/core/cuda.hpp>
using namespace cv;
using namespace cv::cuda;
// using namespace std;

// Compile with -lopencv_core -lopencv_highgui -lopencv_imgproc

int main()
{
    Mat mGr ;
    GpuMat grGpu(mGr);
    // // cap = cv.VideoCapture(0)
    // Mat frame;
    // VideoCapture cap;
    // cap.open(0 + cv::CAP_ANY);

    // // cap.set(6,cv.VideoWriter_fourcc('M','J','P','G'))
    // // cap.set(cv.CAP_PROP_FPS,30)
    // if (!cap.isOpened())
    // {
    //     cout << "Cannot open camera\n";
    //     return -1;
    // }

    // // fgbg = cv.createBackgroundSubtractorMOG2(history = 30, varThreshold = 50, detectShadows = True)
    // Ptr<BackgroundSubtractorMOG2> fgbg = createBackgroundSubtractorMOG2();
    // fgbg->setVarThreshold(50);
    // fgbg->history(30);
    // fgbg->detectShadows(true);



    // for i in range(0,10):
    //     ret, frame1 = cap.read()
    //     fgbg.apply(frame1)
    // cv.namedWindow('frame', cv.WINDOW_NORMAL)
    // while(True)
    //     ret, frame = cap.read()
    //     frame = frame[:, 100:700, :]
    //     if not ret:
    //         print("Can't receive frame (stream end?). Exiting ...")
    //         return
    //     fgmask = fgbg.apply(frame, learningRate = 0)
    //     output_backsub = cv.bitwise_and(frame, frame, mask = fgmask)
    //     frame_hsv = cv.cvtColor(output_backsub, cv.COLOR_RGB2HSV)
    //     pink_square = detection_pink(frame_hsv)
    //     blue_square = detection_blue(frame_hsv) 
    //     if pink_square.any():
    //         frame = draw(frame, pink_square, 'green')
    //     if blue_square.any():
    //         frame = draw(frame, blue_square, 'red')
    //     cv.imshow('frame', frame)
    //     if cv.waitKey(1) == ord('q'):
    //         cap.release()
    //         cv.destroyAllWindows()
    //         break
}

// detection_pink(frame_hsv)
// {
//     // Declare boundary colors for detection in HSV
//     lower_pink = np.array([(115,50,160)], dtype = "uint8")
//     upper_pink = np.array([([160,255,255])], dtype = "uint8")

//     // Check for the color pink between a certain scope of all pinks
//     mask_pink = cv.inRange(frame_hsv,lower_pink,upper_pink)
//     output_pink = cv.bitwise_and(frame_hsv, frame_hsv, mask = mask_pink)

//     // Turn the frame gray
//     gray_pink = cv.cvtColor(output_pink, cv.COLOR_BGR2GRAY) # Turns the frame from BGR to Grayscale

//     // Find Contours
//     // Set the threshhold to detect contours
//     ret_pink, thresh_pink = cv.threshold(gray_pink, 100, 255, 0)
//     contours_pink = cv.findContours(thresh_pink, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]
//     cv.drawContours(output_pink, contours_pink, -1, (0,255,0), 3)

//     // Label the contours for the pink square
//     for c in contours_pink:
//         // Find contours with edges of similar lengths
//         peri = cv.arcLength(c, True)
//         approx = cv.approxPolyDP(c, 0.04 * peri, True)

//         //print(peri)
//         // Only look at contours with 4 edges and perimeters greater than 200
//         if(len(approx) == 4) and (peri > 65):
//             pink_square = c
//             // cv.drawContours(output_pink, [c], -1, (0,255,0), 2)
//             // Find the center of the contours
//             // M = cv.moments(c)
//             // if M["m00"] != 0:
//             //  cX = int((M["m10"] / M["m00"]))
//             //  cY = int((M["m01"] / M["m00"]))
//             //  cv.imshow('frame',output_pink)
//             //  cv.putText(output_pink, "middle", (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
//             //  cv.imshow('frame',output_pink)
//             //  print(cX,",",cY)
//             // return cX, cY, False
//             return pink_square
//             // return pink_square

//     return np.array([], dtype = "uint8")
// }

// detection_blue(frame_hsv)
// {
//     // Declare boundary colors for detection in HSV
//     lower_blue = np.array([(10,170,100)], dtype = "uint8")
//     upper_blue = np.array([([20,255,255])], dtype = "uint8")

//     // Check for the color blue between a certain scope of all blues
//     mask_blue = cv.inRange(frame_hsv,lower_blue,upper_blue)
//     output_blue = cv.bitwise_and(frame_hsv, frame_hsv, mask = mask_blue)

//     // Turn the frame gray
//     gray_blue = cv.cvtColor(output_blue, cv.COLOR_BGR2GRAY)

//     // Find Contours
//     // Set the threshhold to detect contours
//     ret_blue, thresh_blue = cv.threshold(gray_blue, 100, 255, 0)
//     contours_blue = cv.findContours(thresh_blue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2]

    
//     // Label the contours for the blue square
//     for d in contours_blue:
//         // Find contours with edges of similar lengths
//         peri = cv.arcLength(d, True)
//         approx = cv.approxPolyDP(d, 0.04 * peri, True)

//         // Only look at contours with 4 edges and perimeters greater than 200
//         if (len(approx) == 4) and (peri > 45):
//             // print(d)
//             blue_square = d
//             // M = cv.moments(d)
//             // if M["m00"] != 0:
//             //     cX = int((M["m10"] / M["m00"]))
//             //     cY = int((M["m01"] / M["m00"]))
//             //     cv.drawContours(gray_blue,d,-1,(0,255,0), 3)
//             //     cv.putText(frame, "middle", (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
//             // return cX, cY, False
//             return blue_square
    
//     // return -1,-1,True
//     return np.array([],dtype = "uint8")
// }

// detection_orange(frame_hsv)
// {

// }

// draw(frame, contour_array, color)
// {
//     if color == 'green':
//         b = 0
//         g = 255
//         r = 0
//     if color == 'red':
//         b = 0
//         g = 0
//         r = 255
//     if color == 'blue':
//         b = 255
//         g = 0
//         r = 0
//     cv.drawContours(frame, [contour_array], -1, (r,g,b), 1)
//         // Find the center of the contours
//     M = cv.moments(contour_array)
//     if M["m00"] != 0:
//         cX = int((M["m10"] / M["m00"]))
//         cY = int((M["m01"] / M["m00"]))
//         cv.putText(frame, "middle", (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
//     return frame
// }