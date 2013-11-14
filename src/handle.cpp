#ifndef _HANDLE
#define _HANDLE
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

#define ARM 0

#define U_ARM(input,i,j) input[((int)(j / 2)) * width + ((int)(i / 2)) * 2];
#define V_ARM(input,i,j) input[((int)(j / 2)) * width + ((int)(i / 2)) * 2 + 1];

#define U_X86(input,i,j) input.at<cv::Vec3b>(i,j)[1]
#define V_X86(input,i,j) input.at<cv::Vec3b>(i,j)[2]

using namespace cv;
using namespace std;

int max_sum = 0;
int min_sum = 255;

#if ARM
void threshold_frame(char* frame,int rows, int cols){
#else
Mat threshold_frame(Mat frame){
    int rows = frame.rows;
    int cols = frame.cols;
    Mat output = Mat::zeros( rows, cols, CV_8UC3 );
#endif

    int prev_max = max_sum;
    int prev_min = min_sum;
    for(int j = 0; j<cols; j++){
        for(int i = 0; i<rows; i++){

#if ARM
            int u = U_ARM(frame,i,j);
            int v = V_ARM(frame,i,j);
#else
            int u = U_X86(frame,i,j);
            int v = V_X86(frame,i,j);
#endif

            int sum = 255 - (u + v)/2;
            if(sum>max_sum)
                max_sum = sum;
            if(sum<min_sum)
                min_sum = sum;
            sum = (sum-prev_min)*(255/(prev_max-prev_min));

            //threshold the image
            if(sum > 150){
#if !ARM
                output.at<cv::Vec3b>(i,j)[0] = 255;
#endif
            }
        }
    }
#if !ARM
    return output;
#endif
}

#endif
