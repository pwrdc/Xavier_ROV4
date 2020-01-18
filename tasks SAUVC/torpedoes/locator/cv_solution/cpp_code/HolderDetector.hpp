#pragma once

#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <vector>
#include <iostream>
#include <map>


class HolderDetector
{
public:
    HolderDetector(std::string fileName);
    
    void run();
    std::map<std::string, double> getLeverCoordinates(cv::Mat frame);
    void setLowHSV(int H, int S, int V);
    void setHighHSV(int H, int S, int V);
    
private:
    int lowTreshH = 75;
    int lowTreshS = 0;
    int lowTreshV = 118;
    int highTreshH = 179;
    int highTreshS = 255;
    int highTreshV = 255;
    int minLineLength = 50;
    
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
    std::vector<cv::Vec4i> findLinesParameters(cv::Mat frame);
    
    void normalizeCoordinates(double& x, double& y, cv::Mat frame);
};
