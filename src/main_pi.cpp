#include <stdio.h>
#include <boost/python.hpp>
#include <unistd.h>
#include <ctime>
#include "picam/camera.h"
#include "picam/graphics.h"
#include "handle.cpp"

#define WIDTH 256
#define HEIGHT 256

using namespace std;

char tmpbuff[WIDTH*HEIGHT*4];
int max_sum = 0;
int min_sum = 255;
CCamera* cam;
bool do_argb_conversion = true;
int num_levels = 1;
Component found;
GfxTexture texture;

void init_main_pi(){
	printf("Starting\n");
	cam = StartCamera(WIDTH, HEIGHT,30,num_levels,do_argb_conversion);

}
float process_frame(){
	time_t start = time(NULL);
	cam->ReadFrame(0,tmpbuff,sizeof(tmpbuff));

	found = threshold_frame(tmpbuff,HEIGHT,WIDTH);

	return found.y;
}
void stop_main_pi(){
	StopCamera();
}

//entry point
int main(int argc, const char **argv)
{
	init_main_pi();
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
	stop_main_pi();
}


BOOST_PYTHON_MODULE(libmain_py){
	using namespace boost::python;
	def("init_main_pi",init_main_pi);
	def("process_frame",process_frame);
	def("stop_main_pi",stop_main_pi);
}
