#include <opencv2/opencv.hpp>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>

using namespace std;
using namespace cv;

void 图像合成为视频() {

	// 处理text
	vector<string> dates;
	ifstream fin("E:\\_SpatialData\\GIS-Q4\\Q4-东湖绿道-20200102_150503\\data2frame.txt", std::ios::in);
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
	}
	fin.clear();
	fin.close();

	VideoWriter writer("E:\\_SpatialData\\GIS-Q4\\Q4-东湖绿道-20200102_150503\\video.mp4", 6, 5, Size(480, 640), true);

	string inputPath = "E:\\_SpatialData\\GIS-Q4\\Q4-东湖绿道-20200102_150503\\images\\";
	for (int i = 0; i < dates.size(); i++) {
		Mat src = imread(inputPath + dates[i] + ".jpg");
		writer.write(src);
		cout << i << endl;
	}

	// 释放资源
	writer.release();

}