#include <opencv2/opencv.hpp>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>

using namespace std;
using namespace cv;

int main() {

	// 处理text
	vector<string> dates;
	vector<int> frame_nums;
	ifstream fin("E:\\_SpatialData\\GIS-Q4\\Q4-光谷和老校区-20191229_133445\\data2frame.txt", std::ios::in);
	char line[1024] = { 0 };
	string date = "";
	int frame_num = 0;
	while (fin.getline(line, sizeof(line)))
	{
		stringstream word(line);
		word >> date >> date >> frame_num;
		std::replace(date.begin(), date.end(), ':', '_');
		std::replace(date.begin(), date.end(), '.', '_');
		dates.push_back(date);
		frame_nums.push_back(frame_num);
	}
	fin.clear();
	fin.close();
	frame_nums.push_back(INT_MAX);

	VideoCapture capture;
	// 打开本地的视频文件
	capture.open("E:\\_SpatialData\\GIS-Q4\\Q4-光谷和老校区-20191229_133445\\VID_20191229_133445.mp4");

	if (!capture.isOpened()) {
		cout << "could not open this capture.." << endl;
		return -1;
	}

	int width = static_cast<int>(capture.get(CAP_PROP_FRAME_WIDTH));
	int height = static_cast<int>(capture.get(CAP_PROP_FRAME_HEIGHT));
	int count = static_cast<int>(capture.get(CAP_PROP_FRAME_COUNT));
	int fps = static_cast<int>(capture.get(CAP_PROP_FPS));
	cout << "分辨率：(" << width << "x" << height << ") " << endl;
	cout << "总帧数：" << capture.get(CAP_PROP_FRAME_COUNT) << endl;
	cout << "帧率：" << capture.get(CAP_PROP_FPS) << endl;

	VideoWriter writer("E:\\_SpatialData\\GIS-Q4\\Q4-光谷和老校区-20191229_133445\\video.mp4", 6, 5, Size(480, 640), true);

	Mat frame, roi, temp, temp2, dst;
	//Rect rect(0, 0, 720 - 80, 480);
	//string outPath = "E:\\_SpatialData\\GIS-Q4\\Q4-东湖绿道-20200102_150503\\images\\";
	//string filename;
	int i = 0;
	int real_num = 0;
	frame_num = frame_nums[0];
	while (capture.read(frame)) {
		i++;
		/*if (i == 1000) {
			break;
		}*/
		if (i == frame_num) {
			// 提取roi
			//roi = frame(rect);
			// 图像转置
			transpose(frame, temp);
			// 图像镜像
			flip(temp, dst, 1);
			// 缩放
			//resize(temp2, dst, Size(480, 640));
			// 显示
			//imshow("capture_video", dst);
			// 保存
			/*filename = outPath + dates[real_num] + ".jpg";
			imwrite(filename, dst);*/
			writer.write(dst);
			real_num++;
			frame_num = frame_nums[real_num];
			cout << real_num << endl;
		}
		
		// 监听键盘事件，按Esc退出
		//char c = waitKey(50);
		//if (c == 27) {
		//	break;
		//}
	}
	cout << "i: " << i << endl;
	cout << "real_num: " << real_num << endl;
	// 释放资源
	capture.release();
	return 0;

}