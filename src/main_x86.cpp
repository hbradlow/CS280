#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <highgui.h>
#include <cv.h>
#include "handle.cpp"
#include <iostream>
#include <boost/python.hpp>

#define CAM 1

using namespace cv;
using namespace std;
VideoCapture stream(0);
Component found;
Mat current_frame;

void start(){
    //set up capture device
    stream.set(CV_CAP_PROP_FRAME_WIDTH,320);
    stream.set(CV_CAP_PROP_FRAME_HEIGHT,240);
}
void process_frame(){
    Mat frame;
    //extract a frame
    stream.read(frame);

    cvtColor(frame,frame,CV_BGR2YCrCb);

    found = threshold_frame(frame);
    current_frame = found.image;
    if(found.area>40)
        cout << found.x << " " << found.y << " " << found.area << endl;
    else
        cout << -1 << " " << -1 << " " << -1 << endl;
}
void stop(){
}

int main(){
    start();
    //set up debug windows
    namedWindow("Output", CV_WINDOW_AUTOSIZE);

    while(1){
        process_frame();
        //display the frame
        imshow("Output",current_frame);

        //Wait 10mS
        int c = cvWaitKey(10);
        //If 'ESC' is pressed, break the loop
        if((char)c==27 ) break;      
    }
    stop();
    return 0;
}

BOOST_PYTHON_MODULE(libmain_py){
	using namespace boost::python;
	def("start",start);
	def("process_frame",process_frame);
	def("stop",stop);
}
