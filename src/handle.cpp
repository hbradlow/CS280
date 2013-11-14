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
    int max_components = 200;
    int equivalent[max_components];
    int size[max_components];
    int id = 1;
    for(int i = 0; i<max_components; i++){
        equivalent[i] = i;
        size[i] = 0;
    }

    int rows = frame.rows;
    int cols = frame.cols;
    Mat components = Mat::zeros( rows, cols, CV_8UC3 );
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
                int west = 0;
                int north = 0;
                if(i>0)
                    west = components.at<cv::Vec3b>(i-1,j)[0];
                if(j>0)
                    north = components.at<cv::Vec3b>(i,j-1)[0];

                if(west != 0 and north != 0 and west != north){
                    if(west<north){
                        components.at<cv::Vec3b>(i,j) = west;
                        equivalent[north] = west;
                    }
                    else{
                        components.at<cv::Vec3b>(i,j) = north;
                        equivalent[west] = north;
                    }
                }
                else if(west != 0){
                    components.at<cv::Vec3b>(i,j) = west;
                }
                else if(north != 0){
                    components.at<cv::Vec3b>(i,j) = north;
                }
                else{
                    components.at<cv::Vec3b>(i,j) = id;
                    if(id<max_components-1)
                        id++;
                }
            }
            else{
                components.at<cv::Vec3b>(i,j)[0] = 0;
#endif
            }
        }
    }
    int num = 0;
    for(int i = 0; i<id; i++){
        if(equivalent[i] == i){
            //cout << "New component " << i << endl;
            num++;
        }
        if(equivalent[i] > max_components)
            cout << "Weird " << i << endl;
    }
    cout << "Num components " << num << endl;

    for(int j = 0; j<cols; j++){
        for(int i = 0; i<rows; i++){
            int current = components.at<cv::Vec3b>(i,j)[0];
            int count = 0;
            while(current != equivalent[current] and count < 30){
                current = equivalent[current];
                count ++;
            }
            components.at<cv::Vec3b>(i,j)[0] = current*(255/num);
            size[current] += 1;
        }
    }
#if !ARM
    return components;
#endif
}

#endif
