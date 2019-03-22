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
    int getRotationAngle();
    map<string,int> getIntersectionCoordinates();
    
private:
    bool isRunning = false;
    bool isAssigned = false;
    bool isVideo = true;
    int frameNumber = 1;
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
    //
    // Description:
    // Vector containing 2 parameters:
    //
    // [0] -> first line's angle
    // [1] -> second line's angle
    //
    // both measured relative to vertical
    std::vector<double> angleDifference;
    double momentumPercent = 0.4;
    cv::VideoCapture videoCap;
    cv::Mat frame;
    cv::Mat image;
    Logger logger;
    
    void createControlWindow();
    void printFrame(cv::Mat printedFrame);
    cv::Mat captureSingleFrame();
    void printParameters(std::string name, std::vector<double> vector);
    
    void countCoordinates(cv::Mat &printedFrame);
    void updateParameters(std::vector<double> vector);
    void countAngleDifference();
    void normalizeCoordinates(double& x, double& y);
    std::vector<double> countAverage(std::vector<std::vector<double>> &tempParameters);
    
    std::vector<double> findLinesParameters(cv::Mat frame);
    std::vector<std::vector<double>> sortParameters(std::vector<cv::Vec2f> &lines);
    void assignLineOrder(std::vector<cv::Vec2f> &lines);
    void assignLines(std::vector<cv::Vec2f> &lines, size_t &i, std::vector<std::vector<double>> &tempParameters);
    bool isFirstLine(std::vector<cv::Vec2f> &lines, const size_t &i);
    void assignFirstParameters(std::vector<double> & vector);
    std::vector<cv::Vec2f> detectLines(cv::Mat &frame);
    
    cv::Mat prepareImage(cv::Mat &frame);
    cv::Mat cannyEdges(cv::Mat &blurredImg);
    cv::Mat blurrImage(cv::Mat &imgThresholded);
    cv::Mat thresholdImage(cv::Mat &imgHSV);
    void doMorphOperations(cv::Mat &imgThresholded);
    
    void checkIsRunning();
};

