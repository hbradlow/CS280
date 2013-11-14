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
    int max_components = 200; //maximum number of connected components to find
    int equivalent[max_components]; //data structure to handle merging connected components
    int size[max_components]; //count the size of each components
    int id = 1; //increasing id to assign to new components
    //initialize the two data structures
    for(int i = 0; i<max_components; i++){
        equivalent[i] = i; //equivalent starts out with each cell pointing to itself
        size[i] = 0; //sizes all start at 0
    }

    int rows = frame.rows;
    int cols = frame.cols;
    Mat components = Mat::zeros( rows, cols, CV_8UC3 ); //stores the connected component labels
    Mat output = Mat::zeros( rows, cols, CV_8UC3 ); //stores the thresholded image
#endif

    //keep track of the previous iteration min/max
    int prev_max = max_sum;
    int prev_min = min_sum;

    //loop through the image
    for(int j = 0; j<cols; j++){
        for(int i = 0; i<rows; i++){
            //extract the u and v components of a pixel
#if ARM
            int u = U_ARM(frame,i,j);
            int v = V_ARM(frame,i,j);
#else
            int u = U_X86(frame,i,j);
            int v = V_X86(frame,i,j);
#endif

            //calculate the inverse of the sum of the channels
            int sum = 255 - (u + v)/2;
            //keep track of the min/max
            if(sum>max_sum)
                max_sum = sum;
            if(sum<min_sum)
                min_sum = sum;
            //scale the sum to fill the range (0-255)
            sum = (sum-prev_min)*(255/(prev_max-prev_min));

            //threshold the image
            if(sum > 150){
                //compute connected components
                //http://en.wikipedia.org/wiki/Connected-component_labeling#Two-pass
#if !ARM
                output.at<cv::Vec3b>(i,j)[0] = 255; //turn on thresholded pixel in output

                //find labels of pixels to the north and west
                int west = 0;
                int north = 0;
                if(i>0)
                    west = components.at<cv::Vec3b>(i-1,j)[0];
                if(j>0)
                    north = components.at<cv::Vec3b>(i,j-1)[0];

                //consider all cases
                if(west != 0 and north != 0 and west != north){
                    //merge the two components
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
                    //make a new component
                    components.at<cv::Vec3b>(i,j) = id;
                    if(id<max_components-1)
                        id++;
                }
            }
            else{
                //turn the pixel off in output
                components.at<cv::Vec3b>(i,j)[0] = 0;
#endif
            }
        }
    }
    //count the number of components
    int num = 0;
    for(int i = 0; i<id; i++){
        if(equivalent[i] == i){
            num++;
        }
    }
    cout << "Num components " << num << endl;

    //merge components
    for(int j = 0; j<cols; j++){
        for(int i = 0; i<rows; i++){
            //loop down the equivalent structure until the source is found
            int current = components.at<cv::Vec3b>(i,j)[0];
            int count = 0;
            while(current != equivalent[current] and count < 30){
                current = equivalent[current];
                count ++;
            }
            //set the label to the source value
            components.at<cv::Vec3b>(i,j)[0] = current*(255/num);
            size[current] += 1; //keep track of the size of the component
        }
    }
#if !ARM
    return components;
#endif
}

#endif
