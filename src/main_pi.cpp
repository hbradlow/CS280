#include <stdio.h>
#include <boost/python.hpp>
#include <unistd.h>
#include <string>
#include <time.h>
#include "picam/camera.h"
#include "picam/graphics.h"
#include "handle.cpp"

#include <cv.h>
#include <highgui.h>

#define WIDTH 256
#define HEIGHT 256

using namespace std;
using namespace cv;

char tmpbuff[WIDTH*HEIGHT*4];
int max_sum = 0;
int min_sum = 255;
CCamera* cam;
bool do_argb_conversion = true;
int num_levels = 1;
Component found;
GfxTexture texture;

int counter = 0;
int log_period = 5;

char *txt_log_filename = "logs/data.txt";
FILE *txt_log;

void start(){
	printf("Starting\n");
	cam = StartCamera(WIDTH, HEIGHT,30,num_levels,do_argb_conversion);

	txt_log = fopen(txt_log_filename,"a");
	fprintf(txt_log,"START----------------------------------\n");
	fclose(txt_log);
}
void log_string(string value){
	txt_log = fopen(txt_log_filename,"a");
	fprintf(txt_log,value.c_str());
	fclose(txt_log);
}
void set_log_period(int p){
	log_period = p;
}
float process_frame(){
	cam->ReadFrame(0,tmpbuff,sizeof(tmpbuff));


	found = threshold_frame(tmpbuff,HEIGHT,WIDTH);

	// log the image, the found data, and the timestamp
	if(counter%log_period == 0){
		int num = (int)counter/log_period;
		char filename[50];
		sprintf(filename,"logs/image_%d.jpg",num);

		Mat m = Mat(HEIGHT,WIDTH,CV_8UC4,tmpbuff);
		Mat rgb;
		cvtColor(m,rgb,CV_BGR2RGB);
		imwrite(filename,rgb);
	
		clock_t c = clock();
		float t = (float)c/CLOCKS_PER_SEC;

		txt_log = fopen(txt_log_filename,"a");
		fprintf(txt_log,"NUM: %d, X: %f, Y: %f, AREA: %f, TIME: %f\n",
				num,found.x,found.y,found.area,t);
		fclose(txt_log);
	}
	counter += 1;

	return found.y;
}
void stop(){
	StopCamera();
}

int main(int argc, const char **argv)
{
	start();
	InitGraphics();
	texture.Create(WIDTH,HEIGHT);
	printf("Running frame loop\n");
	for(int i = 0; i < 3000; i++)
	{
		process_frame();
		cout << "HERE" << endl;
		texture.SetPixels(found.image);

		BeginFrame();
		float aspect_ratio = float(WIDTH)/float(HEIGHT);
		float screen_aspect_ratio = 1280.f/720.f;
		DrawTextureRect(&texture,-aspect_ratio/screen_aspect_ratio,-1.0f,aspect_ratio/screen_aspect_ratio,1.0f);
		EndFrame();
	}
	stop();
}


BOOST_PYTHON_MODULE(libmain_py){
	using namespace boost::python;
	def("start",start);
	def("log_string",log_string);
	def("process_frame",process_frame);
	def("stop",stop);
}
