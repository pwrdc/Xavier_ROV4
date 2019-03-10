#include "path.hpp"
#include <iostream>
#include <math.h>
#include <numeric>
#include <string>
#include <map>

using namespace std;
using namespace cv;

PathDetector::PathDetector()
{
}

PathDetector::PathDetector(std::string fileName) :
actualParameters (4),
angleDifference(2),
frameNumber(1),
isRunning {false},
isAssigned {false},
isVideo {true},
momentumPercent {0.4},
logger()
{
    size_t found = fileName.find("mp4");
    
    if (found != string::npos)
    {
        videoCap = *new VideoCapture(fileName);
        if (videoCap.isOpened() == false)
        {
            std::cerr << "Cannot open the video file. Press any key..." << std::endl;
            std::cin.get();
            exit(-1);
        }
    }
    else
    {
        image = imread(fileName);
        if (image.empty())
        {
            std::cerr << "Cannot open the image. Press any key..." << std::endl;
            std::cin.get();
            exit(-1);
        }
        isVideo = false;
    }
    logger.makeHeader(momentumPercent);
}
        
        
PathDetector::~PathDetector()
{
   if(isVideo) videoCap.release();
}

void PathDetector::run()
{
    isRunning = true;
    
    createControlWindow();
    
    while (isRunning) {
        cv::Mat frame = captureSingleFrame();
        
        std::vector<double> tempVector = findLinesParameters(frame);
        
        updateParameters(tempVector);
        
        printParameters("ActualAfter", actualParameters);
        
        countAngleDifference();
        
        cout << "rotationAngle:" << getRotationAngle() << "\n";
        
        getIntersectionCoordinates(actualParameters);
        
        printFrame(frame);
        
        frameNumber++;
        
        checkESC();
        
    }
}

void PathDetector::createControlWindow()
{
    cv::namedWindow("Control Window", CV_WINDOW_NORMAL);
}

void PathDetector::checkESC()
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

std::vector<double> PathDetector::findLinesParameters(cv::Mat frame)
{
    std::vector<std::vector<double>> tempParameters(4);
    std::vector<double> averageParameters(4);
    
    std::vector<cv::Vec2f> lines = detectLines(frame);
    
    if (!lines.empty())
    {
        tempParameters = sortParameters(lines);
        
        averageParameters = countAverage(tempParameters);
        
    }
    
    assignFirstParameters(averageParameters);
    
    logger.saveLog(frameNumber, tempParameters, averageParameters);
    
    return averageParameters;
    
}

std::vector<std::vector<double>> PathDetector::sortParameters(std::vector<cv::Vec2f> &lines)
{
    assignLineOrder(lines);
    
    std::vector<std::vector<double>> tempParameters(4);
    
    for (size_t i = 1; i < lines.size(); i++)
    {
        assignLines(lines, i, tempParameters);
    }
    
    return tempParameters;
}

void PathDetector::assignLineOrder(std::vector<cv::Vec2f> &lines)
{
    if (!isAssigned) {
        actualParameters[0] = lines[0][1];
    }
}

void PathDetector::assignLines(std::vector<cv::Vec2f> &lines, size_t &i, std::vector<std::vector<double>> &tempParameters)
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

bool PathDetector::isFirstLine(std::vector<cv::Vec2f> & lines, const size_t &i)
{
    return (lines[i][1] >= 0.8*actualParameters[0]) && (lines[i][1] < 1.2*actualParameters[0]);
}

void PathDetector::assignFirstParameters(std::vector<double> &vector)
{
    if (!isAssigned) {
        actualParameters[0] = vector[0];
        actualParameters[1] = vector[1];
        actualParameters[2] = vector[2];
        actualParameters[3] = vector[3];
        isAssigned = true;
    }
}

std::vector<double>PathDetector::countAverage(std::vector<std::vector<double>> &tempParameters)
{
    std::vector<double> averageParameters(4);
    
    for (int i = 0; i < 4; i++) {
        averageParameters[i] = std::accumulate(tempParameters[i].begin(), tempParameters[i].end(), 0.0) / tempParameters[i].size();
    }
    
    return averageParameters;
}

std::vector<cv::Vec2f> PathDetector::detectLines(cv::Mat &frame)
{
    std::vector<cv::Vec2f> lines;
    std::vector<std::vector<cv::Point> > contours;
    std::vector<cv::Vec4i> hierarchy;
    
    cv::Mat cannyImg = prepareImage(frame);
    
    HoughLines(cannyImg, lines, 1, CV_PI / 180, 50, 0, 0);
    
    return lines;
}

cv::Mat PathDetector::prepareImage(cv::Mat & frame)
{
    cv::Mat preparedImg;
    cv::cvtColor(frame, preparedImg, CV_BGR2HSV);
    
    preparedImg = thresholdImage(preparedImg);
    
    doMorphOperations(preparedImg);
    
    preparedImg = blurrImage(preparedImg);
    
    preparedImg = cannyEdges(preparedImg);
    
    return preparedImg;
}

cv::Mat PathDetector::cannyEdges(cv::Mat &blurredImg)
{
    int lowTreshCanny = 0;
    int highTreshCanny = 255 * 2;
    int kernelSize = 7;
    cv::Mat cannyImg;
    Canny(blurredImg, cannyImg, lowTreshCanny, highTreshCanny, kernelSize);
    
    //imshow("canny", cannyImg);
    
    return cannyImg;
}

cv::Mat PathDetector::blurrImage(cv::Mat &imgThresholded)
{
    cv::Mat blurredImg;
    cv::GaussianBlur(imgThresholded, blurredImg, cv::Size(9, 9), 0, 0);
    
    //imshow("blurred", blurredImg);
    
    return blurredImg;
}

cv::Mat PathDetector::thresholdImage(cv::Mat &imgHSV)
{
    cv::Mat imgThresholded;
    inRange(imgHSV, cv::Scalar(60, 120, 0), cv::Scalar(179, 255, 255), imgThresholded);
    bitwise_not(imgThresholded, imgThresholded);
    
    imshow("tresh", imgThresholded);
    
    return imgThresholded;
}

void PathDetector::doMorphOperations(cv::Mat &imgThresholded)
{
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(19, 19)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(19, 19)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(19, 19)));
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(19, 19)));
}

void PathDetector::printParameters(std::string name, std::vector<double> vector)
{
    for (auto Element : vector) {
        std::cout << name << ": " << Element << std::endl;
    }
    
    std::cout << std::endl << std::endl;
}

void PathDetector::updateParameters(std::vector<double> vector)
{
    for (int i = 0; i < 4; i++) {
        actualParameters[i] += momentumPercent * (vector[i] - actualParameters[i]);
    }
}

void PathDetector::printFrame(cv::Mat printedFrame)
{
    countCoordinates(printedFrame);
    
    cv::imshow("Path", printedFrame);
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
    
    /*x0 = cos(180 * M_PI / 180) * 100;
    y0 = sin(180 * M_PI / 180) * 100;
    pt1.x = cvRound(x0 + 1000 * -sin(180 * M_PI / 180));
    pt1.y = cvRound(y0 + 1000 * cos(180 * M_PI / 180));
    pt2.x = cvRound(x0 - 1000 * -sin(180 * M_PI / 180));
    pt2.y = cvRound(y0 - 1000 * cos(180 * M_PI / 180));
    line(printedFrame, pt1, pt2, cv::Scalar(0, 255, 0), 3, CV_AA);*/ 
}

void PathDetector::countAngleDifference()
{
    if (actualParameters[0] <= M_PI/2) angleDifference[0] = actualParameters[0] * 180 / M_PI;
    else angleDifference[0] = actualParameters[0] * 180 / M_PI - 180;
    if (actualParameters[2] <= M_PI/2) angleDifference[1] = actualParameters[2] * 180 / M_PI;
    else angleDifference[1] = actualParameters[2] * 180 / M_PI;
    //cout << "angle1: " << angleDifference[0] << " angle2: " << angleDifference[1] << "\n";
}

int PathDetector::getRotationAngle()
{
    if(abs(angleDifference[0]) < abs(angleDifference[1])) return int(angleDifference[1]);
    else return int(angleDifference[0]);
}

map<string,int> PathDetector::getIntersectionCoordinates(std::vector<double> actualParameters)
{
    map<string, int> coordinates;
    double a1,a2,b1,b2,x,y;
    
    a1 = 1/(atan(actualParameters[0])); //theta1
    a2 = 1/(atan(actualParameters[2])); //theta2
    b1 = actualParameters[1]; //rho1
    b2 = actualParameters[3]; //rho2
    
    x = (b2 - b1)/(a1 - a2);
    y = (a1*b2 - a2*b1)/(a1 - a2);
    cout << "X: " << x << endl;
    cout << "Y: " << y << endl;
    
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
            std::cout << "Found the end of the video. Pres any key..." << std::endl;
            std::cin.get();
            exit(0);
        }
    }
    else capFrame = image;
    
    return capFrame;
}
