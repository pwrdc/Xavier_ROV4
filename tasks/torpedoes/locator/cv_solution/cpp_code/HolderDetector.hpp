#pragma once

#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <vector>
#include <iostream>
#include <map>


class HolderDetector
{
public:
    HolderDetector();
    HolderDetector(std::string fileName);
    ~HolderDetector();
    
    void run();
    std::map<std::string, double> getLeverCoordinates(cv::Mat frame);
    
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
    
    void createControlWindow();
    
    cv::Mat prepareImage(cv::Mat &frame);
    void cannyEdges(cv::Mat &blurredImg);
    void blurrImage(cv::Mat &imgThresholded);
    void thresholdImage(cv::Mat &imgHSV);
    void doMorphOperations(cv::Mat &imgThresholded);
    
    std::vector<cv::Vec4i> detectLines(cv::Mat &image);
    std::vector<cv::Vec4i> findLinesParameters(cv::Mat frame);
    
    void normalizeCoordinates(double& x, double& y, cv::Mat frame);
};