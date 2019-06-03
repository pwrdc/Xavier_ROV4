#pragma once

#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include <map>

using namespace std;

class CrossDetector
{
public:
    CrossDetector(std::string fileName);
    
    void run();
    map<string,double> getIntersectionCoordinates(const cv::Mat& frame);
    
private:
    
    cv::Mat image;
    //
    // Description:
    //  Vector containing ? parameters:
    //
    //  [0] -> theta1
    //  [1] -> rho1
    //  [2] -> theta2
    //  [3] -> rho2
    //  ...
    //
    std::vector<double> averageParameters;
    
    cv::Mat prepareImage(cv::Mat &frame);
    void cannyEdges(cv::Mat &blurredImg);
    void blurrImage(cv::Mat &imgThresholded);
    void thresholdImage(cv::Mat &imgHSV);
    void doMorphOperations(cv::Mat &imgThresholded);
    
    vector<cv::Vec2f> detectLines(cv::Mat &image);
    void findLinesParameters(cv::Mat frame);
    vector<vector<double>> sortParameters(vector<cv::Vec2f> &lines);
    void isVertical(vector<cv::Vec2f> &lines, vector<vector<double>> &tempParameters);
    vector<double>countVerticalAverage(vector<vector<double>> &tempParameters);
    vector<double>countAverage(vector<vector<double>> &tempParameters);
    vector<double>checkIfPerpendicular(vector<vector<double>> &tempParameters);
    double countVectorAverage (vector<double> tempCoordinates, size_t size);
    void normalizeCoordinates(double& x, double& y, cv::Mat frame);
};

