#include "VampireLeverDetector.hpp"
#include "imageProcessing.h"
#include <iostream>
#include <math.h>
#include <numeric>

using namespace std;
using namespace cv;
using namespace image;

VampireLeverDetector::VampireLeverDetector(string fileName)
{
    image = cv::imread(fileName);
    
    if (image.empty())
    {
        cerr << "Cannot open the image. Press any key..." << endl;
        cin.get();
        exit(-1);
    }
}

void VampireLeverDetector::run()
{
    findLinesParameters(image);
    waitKey(0);
}

void VampireLeverDetector::setLowHSV(int H, int S, int V)
{
    lowTreshH = H;
    lowTreshS = S;
    lowTreshV = V;
}

void VampireLeverDetector::setHighHSV(int H, int S, int V)
{
    highTreshH = H;
    highTreshS = S;
    highTreshV = V;
}

vector<cv::Vec4i> VampireLeverDetector::findLinesParameters(cv::Mat frame)
{
    vector<cv::Vec4i>lines = imageProcessing::detectLinesP(frame, lowTreshH, lowTreshS, lowTreshV, highTreshH, highTreshS, highTreshV, minLineLength);
    return lines;
}

map<string, double> VampireLeverDetector::getLeverCoordinates(Mat frame)
{
	Mat clonedFrame = frame.clone();

    vector<cv::Vec4i>lines = findLinesParameters(clonedFrame);

	for (size_t i = 0; i < lines.size(); i++)
	{
		Vec4i l = lines[i];
		line(image, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 3, CV_AA);
	}

	imshow("iamge", image);
	waitKey(0);
    
    double x1 = 0, y1 = 0, x2 = 0, y2 = 0;
    int counter = 0;
    
    for (auto line : lines)
    {
		x1 += line[0];
		y1 += line[1];
		x2 += line[2];
		y2 += line[3];
		counter++;
	};

	x1 /= counter;
	y1 /= counter;
	x2 /= counter;
	y2 /= counter;

	normalizeCoordinates(x1, y1, frame);
	normalizeCoordinates(x2, y2, frame);

    map<string, double> coordinates;
    
    coordinates["x1"] = x1;
    coordinates["y1"] = y1;
	coordinates["x2"] = x2;
	coordinates["y2"] = y2;

    return coordinates;
}

void VampireLeverDetector::normalizeCoordinates(double& x, double& y, cv::Mat frame)
{
    x = (abs(x) - (frame.size().width/2))/(frame.size().width/2);
    y = ((frame.size().height/2) - abs(y))/(frame.size().height/2);
}
