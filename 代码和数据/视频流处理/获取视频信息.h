#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

void 获取视频信息() {

	VideoCapture capture;
	// 打开本地的视频文件
	capture.open("E:\\_SpatialData\\GIS-Q4\\Q4-东湖绿道-20200102_150503\\video.mp4");

	if (!capture.isOpened()) {
		cout << "could not open this capture.." << endl;
		return;
	}

	int width = static_cast<int>(capture.get(CAP_PROP_FRAME_WIDTH));
	int height = static_cast<int>(capture.get(CAP_PROP_FRAME_HEIGHT));
	int count = static_cast<int>(capture.get(CAP_PROP_FRAME_COUNT));
	int fps = static_cast<int>(capture.get(CAP_PROP_FPS));
	cout << "分辨率：(" << width << "x" << height << ") " << endl;
	cout << "总帧数：" << capture.get(CAP_PROP_FRAME_COUNT) << endl;
	cout << "帧率：" << capture.get(CAP_PROP_FPS) << endl;

	// 释放资源
	capture.release();

}