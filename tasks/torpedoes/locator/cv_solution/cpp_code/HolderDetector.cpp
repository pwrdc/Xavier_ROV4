#include "HolderDetector.hpp"
#include "imageProcessing.h"
#include <iostream>
#include <math.h>
#include <numeric>


using namespace std;
using namespace cv;
using namespace image;

HolderDetector::HolderDetector(string fileName)
{
    image = cv::imread(fileName);
    
    if (image.empty())
    {
        cerr << "Cannot open the image. Press any key..." << endl;
        cin.get();
        exit(-1);
    }
}

void HolderDetector::run()
{
    findLinesParameters(image);
    waitKey(0);
}

void HolderDetector::setLowHSV(int H, int S, int V)
{
    lowTreshH = H;
    lowTreshS = S;
    lowTreshV = V;
}

void HolderDetector::setHighHSV(int H, int S, int V)
{
    highTreshH = H;
    highTreshS = S;
    highTreshV = V;
}

vector<cv::Vec4i> HolderDetector::findLinesParameters(cv::Mat frame)
{
    vector<cv::Vec4i>lines = imageProcessing::detectLinesP(frame, lowTreshH, lowTreshS, lowTreshV, highTreshH, highTreshS, highTreshV);
    return lines;
}

map<string, double> HolderDetector::getLeverCoordinates(Mat frame)
{
    Mat clonedFrame = frame.clone();
    vector<cv::Vec4i>lines = findLinesParameters(clonedFrame);
    
    double x = 0, y = 0;
    int counter = 0;
    
    for (auto line : lines)
    {
        y += abs(line[1] + line[3])/2;
        x += abs(line[0] + line[2])/2;
        counter++;
    }
    x /= counter;
    y /= counter;

    map<string, double> coordinates;
    
    coordinates["x"] = x;
    coordinates["y"] = y;
    
    return coordinates;
}

void HolderDetector::normalizeCoordinates(double& x, double& y, cv::Mat frame)
{
    x = (abs(x) - (frame.size().width/2))/(frame.size().width/2);
    y = ((frame.size().height/2) - abs(y))/(frame.size().height/2);
}
