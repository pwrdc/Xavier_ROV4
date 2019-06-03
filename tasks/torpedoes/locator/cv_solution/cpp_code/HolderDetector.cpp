#include "HolderDetector.hpp"
#include <iostream>
#include <math.h>
#include <numeric>


using namespace std;
using namespace cv;

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

void HolderDetector::createControlWindow()
{
    cv::namedWindow("Control Window", WINDOW_NORMAL);
}


cv::Mat HolderDetector::prepareImage(cv::Mat &frame)
{
    cv::cvtColor(frame, frame, COLOR_BGR2HSV);
    
    thresholdImage(frame);
    
    doMorphOperations(frame);
    
    blurrImage(frame);
    
    cannyEdges(frame);
    
    imshow("canny", frame);
    
    return frame;
}

void HolderDetector::cannyEdges(cv::Mat &blurredImg)
{
    const int lowTreshCanny = 0;
    const int highTreshCanny = 255 * 2;
    const int kernelSize = 7;
    Canny(blurredImg, blurredImg, lowTreshCanny, highTreshCanny, kernelSize);
    
    
}

void HolderDetector::blurrImage(cv::Mat &imgThresholded)
{
    const int kernelWidth = 9;
    const int kernelHeight = 9;
    const int sigmaX = 0; //The standard deviation in x
    const int sigmaY = 0; //The standard deviation in y
    cv::Mat blurredImg;
    
    cv::GaussianBlur(imgThresholded, imgThresholded, cv::Size(kernelWidth, kernelHeight), sigmaX, sigmaY);
}

void HolderDetector::thresholdImage(cv::Mat &imgHSV)
{
    inRange(imgHSV, cv::Scalar(lowTreshH, lowTreshS, lowTreshV),
            cv::Scalar(highTreshH, highTreshS, highTreshV), imgHSV);
    bitwise_not(imgHSV, imgHSV);
}

void HolderDetector::doMorphOperations(cv::Mat &imgThresholded)
{
    const int kernelWidth = 3;
    const int kernelHeight = 3;
    
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
}

vector<cv::Vec4i> HolderDetector::detectLines(cv::Mat &image)
{
    const int rho = 1; //The resolution of the parameter \rho in pixels
    const int tresh = 40; //The minimum number of intersections to “detect” a line
    const double theta = CV_PI / 180; //The resolution of the parameter \theta in radians.
    const int minLinLength = 50, maxLinLength = 10;
    
    vector<cv::Vec4i> lines;
    
    cv::Mat clonedImage = image.clone();
    
    cv:Mat cannyImg = prepareImage(clonedImage);
    
    HoughLinesP(cannyImg, lines, rho, theta, tresh, minLinLength, maxLinLength);
    
    return lines;
}

vector<cv::Vec4i> HolderDetector::findLinesParameters(cv::Mat frame)
{
    vector<cv::Vec4i>lines = detectLines(frame);
    
    return lines;
}

map<string, double> HolderDetector::getLeverCoordinates(Mat frame)
{
    Mat clonedFrame = frame.clone();
    vector<cv::Vec4i>lines = detectLines(clonedFrame);
    
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
    
    normalizeCoordinates(x, y, frame);
    
    map<string, double> coordinates;
    
    coordinates["x"] = x;
    coordinates["y"] = y;
    
    Point point(x,y);
    drawMarker(image, point, 200);
    imshow("swegewg", image);
    waitKey(0);
    
    return coordinates;
}

void HolderDetector::normalizeCoordinates(double& x, double& y, cv::Mat frame)
{
    x = (abs(x) - (frame.size().width/2))/(frame.size().width/2);
    y = ((frame.size().height/2) - abs(y))/(frame.size().height/2);
}
