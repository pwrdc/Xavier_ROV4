#include "GarlicDropLeverDetector.hpp"
#include "imageProcessing.h"
#include <iostream>
#include <math.h>
#include <numeric>

using namespace std;
using namespace cv;
using namespace image;

GarlicDropLeverDetector::GarlicDropLeverDetector(string fileName)
{
    image = cv::imread(fileName);
    
    if (image.empty())
    {
        cerr << "Cannot open the image. Press any key..." << endl;
        cin.get();
        exit(-1);
    }
}

void GarlicDropLeverDetector::run()
{
    findLinesParameters(image);
    waitKey(0);
}

void GarlicDropLeverDetector::setLowHSV(int H, int S, int V)
{
    lowTreshH = H;
    lowTreshS = S;
    lowTreshV = V;
}

void GarlicDropLeverDetector::setHighHSV(int H, int S, int V)
{
    highTreshH = H;
    highTreshS = S;
    highTreshV = V;
}

vector<cv::Vec4i> GarlicDropLeverDetector::findLinesParameters(cv::Mat frame)
{
    vector<cv::Vec4i>lines = imageProcessing::detectLinesP(frame, lowTreshH, lowTreshS, lowTreshV, highTreshH, highTreshS, highTreshV, minLineLength);
    return lines;
}

map<string, double> GarlicDropLeverDetector::getLeverCoordinates(Mat frame)
{
	Mat clonedFrame = frame.clone();

    vector<cv::Vec4i>lines = findLinesParameters(clonedFrame);

	for (size_t i = 0; i < lines.size(); i++)
	{
		Vec4i l = lines[i];
		line(image, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 3);
	}


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

	Point p1(x1, y1);
	Point p2(x2, y2);
	drawMarker(image, p1, 255);
	drawMarker(image, p2, 255);
	imshow("points", image);
	waitKey(0);

	normalizeCoordinates(x1, y1, frame);
	normalizeCoordinates(x2, y2, frame);

    map<string, double> coordinates;
    
    coordinates["x1"] = x1;
    coordinates["y1"] = y1;
	coordinates["x2"] = x2;
	coordinates["y2"] = y2;

    return coordinates;
}

void GarlicDropLeverDetector::normalizeCoordinates(double& x, double& y, cv::Mat frame)
{
    x = (abs(x) - (frame.size().width/2))/(frame.size().width/2);
    y = ((frame.size().height/2) - abs(y))/(frame.size().height/2);
}
