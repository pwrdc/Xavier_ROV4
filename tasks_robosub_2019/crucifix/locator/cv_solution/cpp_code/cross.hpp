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
    void setLowHSV(int H, int S, int V);
    void setHighHSV(int H, int S, int V);
    
private:
    
    int lowTreshH = 35;
    int lowTreshS = 0;
    int lowTreshV = 63;
    int highTreshH = 75;
    int highTreshS = 255;
    int highTreshV = 110;
    
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

    void findLinesParameters(cv::Mat frame);
    vector<vector<double>> sortParameters(vector<cv::Vec2f> lines);
    void isVertical(vector<cv::Vec2f> lines, vector<vector<double>> &tempParameters);
    vector<double>countVerticalAverage(vector<vector<double>> tempParameters);
    vector<double>countAverage(vector<vector<double>> tempParameters);
    vector<double>checkIfPerpendicular(vector<vector<double>> &tempParameters);
    void normalizeCoordinates(double& x, double& y, cv::Mat frame);
};

