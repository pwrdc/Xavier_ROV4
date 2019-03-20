#pragma once

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <vector>
#include "logger.hpp"
#include <iostream>
#include <map>


class PathDetector
{
public:
    PathDetector();
    PathDetector(std::string fileName);
    ~PathDetector();
    
    void run();
    int getRotationAngle(); //calculating an value of angle to turn around
    map<string,int> getIntersectionCoordinates(); //counting intersection point
    
private:
    bool isRunning;
    bool isAssigned;
    int frameNumber;
    bool isVideo;
    //
    // Description:
    //  Vector containing 4 parameters:
    //
    //  [0] -> theta1
    //  [1] -> rho1
    //  [2] -> theta2
    //  [3] -> rho2
    //
    std::vector<double> actualParameters;
    std::vector<double> angleDifference;
    double momentumPercent;
    cv::VideoCapture videoCap;
    cv::Mat frame;
    cv::Mat image;
    Logger logger;
    
    void printFrame(cv::Mat printedFrame); //showing original frame
    void countCoordinates(cv::Mat &printedFrame); //counting Hough lines coordinates
    cv::Mat captureSingleFrame(); //taking single frame of a video file
    void createControlWindow(); //creating window
    void checkESC(); //waiting for ESC to change isRunning flag
    std::vector<double> findLinesParameters(cv::Mat frame);
    std::vector<std::vector<double>> sortParameters(std::vector<cv::Vec2f> &lines);
    void assignLineOrder(std::vector<cv::Vec2f> &lines);
    void assignLines(std::vector<cv::Vec2f> &lines, size_t &i, std::vector<std::vector<double>> &tempParameters);
    bool isFirstLine(std::vector<cv::Vec2f> &lines, const size_t &i);
    void assignFirstParameters(std::vector<double> & vector);
    std::vector<double> countAverage(std::vector<std::vector<double>> &tempParameters);
    std::vector<cv::Vec2f> detectLines(cv::Mat &frame);
    cv::Mat prepareImage(cv::Mat &frame);
    cv::Mat cannyEdges(cv::Mat &blurredImg);
    cv::Mat blurrImage(cv::Mat &imgThresholded);
    cv::Mat thresholdImage(cv::Mat &imgHSV);
    void doMorphOperations(cv::Mat &imgThresholded);
    void printParameters(std::string name, std::vector<double> vector);
    void updateParameters(std::vector<double> vector); //momentum 
    void countAngleDifference(); //adjust proper angles values
    void normalizeCoordinates(double& x, double& y);
};

