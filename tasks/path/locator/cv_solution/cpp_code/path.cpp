#include "path.hpp"
#include <iostream>
#include <math.h>
#include <numeric>
#include <string>
#include <map>

using namespace std;
using namespace cv;

PathDetector::PathDetector():
actualParameters(4),
angleDifference(2),
logger(momentumPercent)
{
}

PathDetector::PathDetector(string fileName) :
actualParameters(4),
angleDifference(2),
logger(momentumPercent)
{
    size_t fileFormat = fileName.find("mp4");
    
    if (fileFormat != string::npos)
    {
        videoCap = *new cv::VideoCapture(fileName);
        if (videoCap.isOpened() == false)
        {
            cerr << "Cannot open the video file. Press any key..." << endl;
            cin.get();
            exit(-1);
        }
    }
    else
    {
        image = cv::imread(fileName);
        if (image.empty())
        {
            cerr << "Cannot open the image. Press any key..." << endl;
            cin.get();
            exit(-1);
        }
        isVideo = false;
    }
}
        
        
PathDetector::~PathDetector()
{
   if(isVideo)
   {
       videoCap.release();
   }
}

void PathDetector::run()
{
    
}

void PathDetector::createControlWindow()
{
    cv::namedWindow("Control Window", CV_WINDOW_NORMAL);
}

void PathDetector::checkIfRunning()
{
    if (cv::waitKey(10) == 27)
    {
        isRunning = false;
    }
    if (!isVideo)
    {
        isRunning = false;
    }
}

vector<double> PathDetector::findLinesParameters(cv::Mat frame)
{
    vector<vector<double>> tempParameters(4);
    vector<double> averageParameters(4);

    vector<cv::Vec2f> lines = detectLines(frame);

    if (!lines.empty())
    {
        tempParameters = sortParameters(lines);
        averageParameters = countAverage(tempParameters);
    }
    
    assignFirstParameters(averageParameters);
    
    logger.saveLog(frameNumber, tempParameters, averageParameters);
    
    return averageParameters;
}

vector<vector<double>> PathDetector::sortParameters(vector<cv::Vec2f> &lines)
{
    assignLineOrder(lines);
    
    vector<vector<double>> tempParameters(4);
    
    for (size_t i = 1; i < lines.size(); i++)
    {
        assignLines(lines, i, tempParameters);
    }
    
    return tempParameters;
}

void PathDetector::assignLineOrder(vector<cv::Vec2f> &lines)
{
    if (!isAssigned)
    {
        actualParameters[0] = lines[0][1];
    }
}

void PathDetector::assignLines(vector<cv::Vec2f> &lines, size_t &i, vector<vector<double>> &tempParameters)
{
    if (isFirstLine(lines, i))
    {
        tempParameters[0].push_back(lines[i][1]);
        tempParameters[1].push_back(lines[i][0]);
    }
    else
    {
        tempParameters[2].push_back(lines[i][1]);
        tempParameters[3].push_back(lines[i][0]);
    }
}

bool PathDetector::isFirstLine(vector<cv::Vec2f> & lines, const size_t &i)
{
    const double treshBottom = 0.8;
    const double treshTop = 1.2;
    
    return (lines[i][1] >= treshBottom * actualParameters[0]) && (lines[i][1] < treshTop * actualParameters[0]);
}

void PathDetector::assignFirstParameters(vector<double> &vector)
{
    if (!isAssigned) {
        actualParameters[0] = vector[0];
        actualParameters[1] = vector[1];
        actualParameters[2] = vector[2];
        actualParameters[3] = vector[3];
        isAssigned = true;
    }
}

vector<double>PathDetector::countAverage(vector<vector<double>> &tempParameters)
{
    vector<double> averageParameters(4);
    
    for (int i = 0; i < 4; i++)
    {
        averageParameters[i] = accumulate(tempParameters[i].begin(),
                                          tempParameters[i].end(), 0.0) / tempParameters[i].size();
    }
    return averageParameters;
}

vector<cv::Vec2f> PathDetector::detectLines(cv::Mat frame)
{
    const int rho = 1; //The resolution of the parameter \rho in pixels
    const int tresh = 50; //The minimum number of intersections to “detect” a line
    const int srn = 0, stn = 0; //Default parameters to zero
    const double theta = CV_PI / 180; //The resolution of the parameter \theta in radians.
    
    vector<cv::Vec2f> lines;
    
    prepareImage(frame);

    HoughLines(frame, lines, rho, theta, tresh, srn, stn);
    
    return lines;
}

void PathDetector::prepareImage(cv::Mat &frame)
{
    cv::cvtColor(frame, frame, CV_BGR2HSV);
    
    thresholdImage(frame);
    
    doMorphOperations(frame);
    
    blurrImage(frame);
    
    cannyEdges(frame);
    
}

void PathDetector::cannyEdges(cv::Mat &blurredImg)
{
    const int lowTreshCanny = 0;
    const int highTreshCanny = 255 * 2;
    const int kernelSize = 7;
    Canny(blurredImg, blurredImg, lowTreshCanny, highTreshCanny, kernelSize);
}

void PathDetector::blurrImage(cv::Mat &imgThresholded)
{
    const int kernelWidth = 9;
    const int kernelHeight = 9;
    const int sigmaX = 0; //The standard deviation in x
    const int sigmaY = 0; //The standard deviation in y
    cv::Mat blurredImg;
    
    cv::GaussianBlur(imgThresholded, imgThresholded, cv::Size(kernelWidth, kernelHeight), sigmaX, sigmaY);
}

void PathDetector::thresholdImage(cv::Mat &imgHSV)
{
    const int lowTreshH = 60;
    const int lowTreshS = 120;
    const int lowTreshV = 0;
    const int highTreshH = 179;
    const int highTreshS = 255;
    const int highTreshV = 255;
    
    inRange(imgHSV, cv::Scalar(lowTreshH, lowTreshS, lowTreshV),
            cv::Scalar(highTreshH, highTreshS, highTreshV), imgHSV);
    bitwise_not(imgHSV, imgHSV);
}

void PathDetector::doMorphOperations(cv::Mat &imgThresholded)
{
    const int kernelWidth = 19;
    const int kernelHeight = 19;
    
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
}

void PathDetector::printParameters(string name, vector<double> vector)
{
    for (auto value : vector) {
        cout << name << ": " << value << endl;
    }
}

void PathDetector::updateParameters(vector<double> vector)
{
    for (int i = 0; i < vector.size(); i++)
    {
        actualParameters[i] += momentumPercent * (vector[i] - actualParameters[i]);
    }
}

void PathDetector::printFrame(cv::Mat printedFrame)
{
    countCoordinates(printedFrame);
}

void PathDetector::countCoordinates(cv::Mat &printedFrame)
{
    cv::Point pt1, pt2;
    double x0{ 0 }, y0{ 0 };
    
    x0 = cos(actualParameters[0]) * actualParameters[1];
    y0 = sin(actualParameters[0]) * actualParameters[1];
    pt1.x = cvRound(x0 + 1000 * -sin(actualParameters[0]));
    pt1.y = cvRound(y0 + 1000 * cos(actualParameters[0]));
    pt2.x = cvRound(x0 - 1000 * -sin(actualParameters[0]));
    pt2.y = cvRound(y0 - 1000 * cos(actualParameters[0]));
    line(printedFrame, pt1, pt2, cv::Scalar(0, 0, 255), 3, CV_AA);
    
    
    x0 = cos(actualParameters[2]) * actualParameters[3];
    y0 = sin(actualParameters[2]) * actualParameters[3];
    pt1.x = cvRound(x0 + 1000 * -sin(actualParameters[2]));
    pt1.y = cvRound(y0 + 1000 * cos(actualParameters[2]));
    pt2.x = cvRound(x0 - 1000 * -sin(actualParameters[2]));
    pt2.y = cvRound(y0 - 1000 * cos(actualParameters[2]));
    line(printedFrame, pt1, pt2, cv::Scalar(0, 0, 255), 3, CV_AA);
}

void PathDetector::countAngleDifference()
{
    if (actualParameters[0] <= M_PI/2)
    {
        angleDifference[0] = actualParameters[0] * 180 / M_PI;
    }
    else
    {
        angleDifference[0] = actualParameters[0] * 180 / M_PI - 180;
    }
    if (actualParameters[2] <= M_PI/2)
    {
        angleDifference[1] = actualParameters[2] * 180 / M_PI;
    }
    else
    {
        angleDifference[1] = actualParameters[2] * 180 / M_PI - 180;
    }
}

int PathDetector::getRotationAngle(const cv::Mat& frame)
{
	cv::Mat cloned_frame = frame.clone();
    vector<double> tempVector = findLinesParameters(cloned_frame);

    updateParameters(tempVector);

    //printParameters("ActualAfter", actualParameters);
    
    countAngleDifference();
    
    printFrame(cloned_frame);
    
    return abs(angleDifference[0]) < abs(angleDifference[1]) ? int(angleDifference[1]) : int(angleDifference[0]);
}

void PathDetector::normalizeCoordinates(double& x, double& y, cv::Mat frame)
{
    x = (x - (frame.size().width/2))/(frame.size().width/2);
    y = ((frame.size().height/2) - y)/(frame.size().height/2);
}

map<string,double> PathDetector::getIntersectionCoordinates(const cv::Mat& frame)
{
	cv::Mat cloned_frame = frame.clone();
    vector<double> tempVector = findLinesParameters(cloned_frame);

    updateParameters(tempVector);

    //printParameters("ActualAfter", actualParameters);
    
    /*
    A1*x + B1*y + C1 = 0, A2*x + B2*y + C2 = 0
    A = cosTheta, B = sinTheta, C = Rho
     
    X = (B1 * C1 - B2 * C2) / D
    Y = (A1 * C2 - A2 * C1) / D
    where D = A1 * B2 - A2 * B2
    */
    map<string, double> coordinates;
    double d,x,y;
    
    d = cos(actualParameters[0])*sin(actualParameters[2]) - cos(actualParameters[2])*sin(actualParameters[0]);
    x = (sin(actualParameters[0]) * actualParameters[1] - sin(actualParameters[2])*actualParameters[3])/d;
    y = (cos(actualParameters[0])*actualParameters[3] - cos(actualParameters[2])*actualParameters[1])/d;
    
    normalizeCoordinates(x, y, cloned_frame);
    
    printFrame(cloned_frame);

    coordinates["x"] = x;
    coordinates["y"] = y;

    return coordinates;
}

cv::Mat PathDetector::captureSingleFrame()
{
    cv::Mat capFrame;
    
    if (isVideo)
    {
        bool isSuccess = videoCap.read(capFrame);
        
        if (isSuccess == false)
        {
            cout << "Found the end of the video. Pres any key..." << endl;
            cin.get();
            exit(0);
        }
    }
    else
    {
        capFrame = image;
    }
    
    return capFrame;
}
