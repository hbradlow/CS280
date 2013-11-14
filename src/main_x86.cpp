#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <highgui.h>
#include <cv.h>
#include "handle.cpp"
#include <iostream>

#define CAM 1

using namespace cv;
using namespace std;

int main(){
    //set up capture device
    VideoCapture stream(0);
    stream.set(CV_CAP_PROP_FRAME_WIDTH,320);
    stream.set(CV_CAP_PROP_FRAME_HEIGHT,240);

    //set up debug windows
    namedWindow("Output", CV_WINDOW_AUTOSIZE);

    while(1){
        Mat frame;
        //extract a frame
        stream.read(frame);

        cvtColor(frame,frame,CV_BGR2YCrCb);

        frame = threshold_frame(frame);


        //display the frame
        imshow("Output",frame);

        //Wait 10mS
        int c = cvWaitKey(10);
        //If 'ESC' is pressed, break the loop
        if((char)c==27 ) break;      
    }

    return 0;
}
