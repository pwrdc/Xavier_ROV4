#include "path.hpp"
#include <iostream>
#include <math.h>
#include <numeric>


using namespace std;
using namespace cv;

PathDetector::PathDetector()
{
}

PathDetector::PathDetector(string fileName)
{
    image = cv::imread(fileName);
    if (image.empty())
    {
        cerr << "Cannot open the image. Press any key..." << endl;
        cin.get();
        exit(-1);
    }
}
        
        
PathDetector::~PathDetector()
{

}

void PathDetector::run()
{
    findLinesParameters(image);
    imshow("lines", image);
    waitKey(0);
}

void PathDetector::createControlWindow()
{
    cv::namedWindow("Control Window", WINDOW_NORMAL);
}


cv::Mat PathDetector::prepareImage(cv::Mat &frame)
{
    cv::cvtColor(frame, frame, COLOR_BGR2HSV);
    
    thresholdImage(frame);
    
    doMorphOperations(frame);
    
    blurrImage(frame);
    
    cannyEdges(frame);
    
    imshow("canny", frame);
    
    return frame;
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
    const int lowTreshH = 35;
    const int lowTreshS = 0;
    const int lowTreshV = 63;
    const int highTreshH = 75;
    const int highTreshS = 255;
    const int highTreshV = 110;
    
    inRange(imgHSV, cv::Scalar(lowTreshH, lowTreshS, lowTreshV),
            cv::Scalar(highTreshH, highTreshS, highTreshV), imgHSV);
    bitwise_not(imgHSV, imgHSV);
}

void PathDetector::doMorphOperations(cv::Mat &imgThresholded)
{
    const int kernelWidth = 3;
    const int kernelHeight = 3;
    
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
    erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(kernelWidth, kernelHeight)));
}

vector<cv::Vec2f> PathDetector::detectLines(cv::Mat &image)
{
    const int rho = 1; //The resolution of the parameter \rho in pixels
    const int tresh = 40; //The minimum number of intersections to “detect” a line
    const int srn = 0, stn = 0; //Default parameters to zero
    const double theta = CV_PI / 180; //The resolution of the parameter \theta in radians.
    
    vector<cv::Vec2f> lines;
    
    cv::Mat clonedImage = image.clone();
    
    cv:Mat cannyImg = prepareImage(clonedImage);
    
    HoughLines(cannyImg, lines, rho, theta, tresh, srn, stn);
    
    return lines;
}

void PathDetector::findLinesParameters(cv::Mat frame)
{
    vector<vector<double>> tempParameters;
    
    vector<cv::Vec2f>lines = detectLines(frame);
    
    if (!lines.empty())
    {
        tempParameters = sortParameters(lines);
        averageParameters = checkIfPerpendicular(tempParameters);
    }
    else
    {
        cout << "No lines detected" << endl;
    }
    
    countLinesCoordinates(frame);
    /*for( size_t i = 0; i < lines.size(); i++ )
    {
        float rho = lines[i][0], theta = lines[i][1];
        Point pt1, pt2;
        double a = cos(theta), b = sin(theta);
        double x0 = a*rho, y0 = b*rho;
        pt1.x = cvRound(x0 + 1000*(-b));
        pt1.y = cvRound(y0 + 1000*(a));
        pt2.x = cvRound(x0 - 1000*(-b));
        pt2.y = cvRound(y0 - 1000*(a));
        if (sin(theta) < 0.05)
        {
            cout << "Vertical :" << sin(theta) << endl;
            line( frame, pt1, pt2, Scalar(0,0,255), 3);
        }
        else if (sin(theta) > 0.995)
        {
            cout << "Horizontal :" << sin(theta) << endl;
            line( frame, pt1, pt2, Scalar(0,255,0), 3);
        }
    }*/
}

vector<vector<double>> PathDetector::sortParameters(vector<cv::Vec2f> &lines)
{
    vector<vector<double>> tempParameters;
    
    vector<double> v1;
    tempParameters.push_back(v1);
    tempParameters.push_back(v1);
    
    isVertical(lines, tempParameters);
    
    return tempParameters;
}

void PathDetector::isVertical(vector<cv::Vec2f> &lines, vector<vector<double>> &tempParameters)
{
    vector<vector<double>> vertical;
    double theta, rho;
    vector<vector<double>> nonVertical;
    vector<double> temp;
    
    vector<double> v1;
    vertical.push_back(v1);
    nonVertical.push_back(v1);
    
    for (size_t i = 0; i < lines.size(); i++)
    {
        if (sin(lines[i][1]) < 0.05)
        {
            vertical[vertical.size()-1].push_back(lines[i][1]);
            vertical[vertical.size()-1].push_back(lines[i][0]);
            vertical.push_back(v1);
        }
        else
        {
            nonVertical[nonVertical.size()-1].push_back(lines[i][1]);
            nonVertical[nonVertical.size()-1].push_back(lines[i][0]);
            nonVertical.push_back(v1);
        }
    }
    
    temp = countVerticalAverage(vertical);
    
    theta = temp[0];
    rho = temp[1];
    
    tempParameters = nonVertical;
    
    tempParameters.push_back(v1);
    tempParameters[tempParameters.size()-1].push_back(theta);
    tempParameters[tempParameters.size()-1].push_back(rho);
}

vector<double>PathDetector::checkIfPerpendicular(vector<vector<double>> &tempParameters)
{
    vector<vector<double>> perpendicularParams;
    vector<double> v1;
    perpendicularParams.push_back(v1);
    vector<double> temp;
    double theta, rho;
    
    vector<double> finalParams;
    
    for (int i = 0; i < tempParameters.size()-2; i++)
    {
        if(!tempParameters[i].empty())
        {
            if(sin(tempParameters[i][0]) > 0.995)
            {
                perpendicularParams[perpendicularParams.size()-1].push_back(tempParameters[i][0]);
                perpendicularParams[perpendicularParams.size()-1].push_back(tempParameters[i][1]);
                perpendicularParams.push_back(v1);
            }
        }
    }
    
    temp = countAverage(perpendicularParams);
    
    theta = temp[0];
    rho = temp[1];
    
    finalParams.push_back(tempParameters[tempParameters.size()-1][0]);
    finalParams.push_back(tempParameters[tempParameters.size()-1][1]);
    finalParams.push_back(theta);
    finalParams.push_back(rho);
    
    return finalParams;
}


vector<double>PathDetector::countVerticalAverage(vector<vector<double>> &tempParameters)
{
    vector<double> tempParams(2);
    double sumRho = 0;
    int counter = 0;
    
    for (int i = 0; i < tempParameters.size()-1; i++)
    {
        if(tempParameters[i][0])
        {
            sumRho += abs(tempParameters[i][1]);
            counter++;
        }
    }
    
    tempParams[0] = M_PI - 3.14;
    tempParams[1] = sumRho/counter;
    
    return tempParams;
}

vector<double>PathDetector::countAverage(vector<vector<double>> &tempParameters)
{
    vector<double> tempParams(2);
    double sumRho = 0, sumTheta = 0;
    int counter = 0;
    
    for (int i = 0; i < tempParameters.size()-1; i++)
    {
        if(tempParameters[i][0])
        {
            sumTheta += abs(tempParameters[i][0]);
            counter++;
        }
    }
    
    for (int i = 0; i < tempParameters.size()-1; i++)
    {
        if(tempParameters[i][0])
        {
            sumRho += abs(tempParameters[i][1]);
        }
    }
    
    tempParams[0] = sumTheta/counter;
    tempParams[1] = sumRho/counter;
    
    return tempParams;
}

void PathDetector::countLinesCoordinates(cv::Mat &frame)
{
    cv::Point pt1, pt2;
    double x0{ 0 }, y0{ 0 };
    
    for (int i = 0 ; i < averageParameters.size(); i+=2)
    {
        x0 = cos(averageParameters[i]) * averageParameters[i+1];
        y0 = sin(averageParameters[i]) * averageParameters[i+1];
        pt1.x = cvRound(x0 + 1000 * -sin(averageParameters[i]));
        pt1.y = cvRound(y0 + 1000 * cos(averageParameters[i]));
        pt2.x = cvRound(x0 - 1000 * -sin(averageParameters[i]));
        pt2.y = cvRound(y0 - 1000 * cos(averageParameters[i]));
        line(frame, pt1, pt2, cv::Scalar(0, 0, 255), 3);
    }
}

double PathDetector::countVectorAverage (vector<double> tempCoordinates, size_t size)
{
    double sum = 0;
    for (int i = 0; i < size; i++)
    {
        sum += tempCoordinates[i];
    }
    return sum/size;
}


