#ifndef _HANDLE
#define _HANDLE
#define ARM 0
#define DEBUG 1

#if ARM
#else
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#endif

#include <iostream>

#define U_ARM(input,i,j) input[((int)(j / 2)) * width + ((int)(i / 2)) * 2];
#define V_ARM(input,i,j) input[((int)(j / 2)) * width + ((int)(i / 2)) * 2 + 1];

#define U_X86(input,i,j) input.at<cv::Vec3b>(i,j)[1]
#define V_X86(input,i,j) input.at<cv::Vec3b>(i,j)[2]

using namespace cv;
using namespace std;

int max_sum = 0;
int min_sum = 255;

#if ARM
void set_image_value(char* input, int i, int j, int channel, int width, int value){
    input[j * width + i] = value;

}
#else
void set_image_value(Mat input, int i, int j, int channel, int width, int value){
    input.at<cv::Vec3b>(i,j)[channel] = value;
}
#endif
#if ARM
int image_value(char* input, int i, int j, int channel, int width){
    return input[j * width + i];

}
#else
int image_value(Mat input, int i, int j, int channel, int width){
    return input.at<cv::Vec3b>(i,j)[channel];
}
#endif

struct Component
{
    float x;
    float y;
    int area;
#if !ARM
    Mat image;
#endif
};

#if ARM
Component threshold_frame(char* frame,int rows, int cols){
    char* components = (char*)malloc(sizeof(char)*rows*cols);
#else
Component threshold_frame(Mat frame){
    int rows = frame.rows;
    int cols = frame.cols;
    Mat components = Mat::zeros( rows, cols, CV_8UC3 ); //stores the connected component labels
#endif
    int max_components = 200; //maximum number of connected components to find
    int equivalent[max_components]; //data structure to handle merging connected components
    int size[max_components]; //count the size of each components
    int moment_x[max_components]; //calculate the moment x of each component
    int moment_y[max_components]; //calculate the moment y of each component
    int id = 1; //increasing id to assign to new components
    //initialize the two data structures
    for(int i = 0; i<max_components; i++){
        equivalent[i] = i; //equivalent starts out with each cell pointing to itself
        size[i] = 0; //sizes all start at 0
        moment_x[i] = 0; //moments start at 0
        moment_y[i] = 0; //moments start at 0
    }

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
                //find labels of pixels to the north and west
                int west = 0;
                int north = 0;
                if(i>0)
                    west = image_value(components,i-1,j,0,cols);
                if(j>0)
                    north = image_value(components,i,j-1,0,cols);

                //consider all cases
                if(west != 0 and north != 0 and west != north){
                    //merge the two components
                    if(west<north){
                        set_image_value(components,i,j,0,cols,west);
                        equivalent[north] = west;
                    }
                    else{
                        set_image_value(components,i,j,0,cols,north);
                        equivalent[west] = north;
                    }
                }
                else if(west != 0){
                    set_image_value(components,i,j,0,cols,west);
                }
                else if(north != 0){
                    set_image_value(components,i,j,0,cols,north);
                }
                else{
                    //make a new component
                    set_image_value(components,i,j,0,cols,id);
                    if(id<max_components-1)
                        id++;
                }
            }
            else{
                //turn the pixel off in output
                set_image_value(components,i,j,0,cols,0);
            }
        }
    }
#if DEBUG
    //count the number of components
    int num = 0;
    for(int i = 0; i<id; i++){
        if(equivalent[i] == i){
            num++;
        }
    }
    cout << "Num components " << num << endl;
#endif

    //merge components
    int max_size = 0;
    int max_component = -1;
    for(int j = 0; j<cols; j++){
        for(int i = 0; i<rows; i++){
            //loop down the equivalent structure until the source is found
            int current = image_value(components,i,j,0,cols);
            int count = 0;
            while(current != equivalent[current] and count < 30){
                current = equivalent[current];
                count ++;
            }
#if DEBUG
            //set the label to the source value
            set_image_value(components,i,j,0,cols,current*(255/num));
#else
            set_image_value(components,i,j,0,cols,current);
#endif
            size[current] += 1; //keep track of the size of the component
            moment_x[current] += i;
            moment_y[current] += j;
            if(current != 0 && size[current] > max_size){
                max_size = size[current];
                max_component = current;
            }
        }
    }
#if DEBUG
    cout << "Max component size " << max_size << endl;
#endif
    Component found_component;
    found_component.x = moment_x[max_component]/(float)max_size;
    found_component.y = moment_y[max_component]/(float)max_size;
    found_component.area = max_size;
#if !ARM
    for(int j = 0; j<cols; j++){
        for(int i = 0; i<rows; i++){
#if DEBUG
            if(components.at<cv::Vec3b>(i,j)[0] == max_component*(255/num)){
#else
            if(components.at<cv::Vec3b>(i,j)[0] == max_component){
#endif
                components.at<cv::Vec3b>(i,j)[0] = 255;
            }
            else{
                components.at<cv::Vec3b>(i,j)[0] = 0;
            }
        }
    }
    found_component.image = components;
    return found_component;
#endif
}
#endif
