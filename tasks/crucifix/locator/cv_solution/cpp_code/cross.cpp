#define _USE_MATH_DEFINES
#include <cmath>
#include "cross.hpp"
#include <iostream>
#include <math.h>
#include <numeric>
#include <execution>
#include "imageProcessing.h"

using namespace std;
using namespace cv;
using namespace image;

CrossDetector::CrossDetector(string fileName)
{
    image = cv::imread(fileName);
    if (image.empty())
    {
        cerr << "Cannot open the image. Press any key..." << endl;
        cin.get();
        exit(-1);
    }
}

void CrossDetector::run()
{
    findLinesParameters(image);
    imshow("lines", image);
    waitKey(0);
}

void CrossDetector::setLowHSV(int H, int S, int V)
{
    lowTreshH = H;
    lowTreshS = S;
    lowTreshV = V;
}

void CrossDetector::setHighHSV(int H, int S, int V)
{
    highTreshH = H;
    highTreshS = S;
    highTreshV = V;
}

void CrossDetector::findLinesParameters(cv::Mat frame)
{
    vector<vector<double>> tempParameters;
    
	vector<cv::Vec2f>lines = imageProcessing::detectLines(frame, lowTreshH, lowTreshS, lowTreshV, highTreshH, highTreshS, highTreshV);
    
    if (!lines.empty())
    {
        tempParameters = sortParameters(lines);
        averageParameters = checkIfPerpendicular(tempParameters);
    }
    else
    {
        cout << "No lines detected" << endl;
    }
}

vector<vector<double>> CrossDetector::sortParameters(vector<cv::Vec2f> lines)
{
    vector<vector<double>> tempParameters;
    
    vector<double> v1;
    tempParameters.push_back(v1);
    
    isVertical(lines, tempParameters);
    
    return tempParameters;
}

void CrossDetector::isVertical(vector<cv::Vec2f> lines, vector<vector<double>> &tempParameters)
{
    vector<vector<double>> vertical;
    double theta, rho;
    vector<vector<double>> nonVertical;
    vector<double> temp;
    
    vector<double> v1;
    vertical.push_back(v1);
    nonVertical.push_back(v1);
    
    for_each(execution::par, lines.begin(), lines.end(), [&vertical, &nonVertical](cv::Vec2f x){
        vector<double> v1;
        if (sin(x[1]) < 0.05)
        {
            vertical[vertical.size()-1].push_back(x[1]);
            vertical[vertical.size()-1].push_back(x[0]);
            vertical.push_back(v1);
        }
        else
        {
            nonVertical[nonVertical.size()-1].push_back(x[1]);
            nonVertical[nonVertical.size()-1].push_back(x[0]);
            nonVertical.push_back(v1);
        }
    });
    
    temp = countVerticalAverage(vertical);
    
    theta = temp[0];
    rho = temp[1];
    
    tempParameters = nonVertical;
    
    tempParameters.push_back(v1);
    tempParameters[tempParameters.size()-1].push_back(theta);
    tempParameters[tempParameters.size()-1].push_back(rho);
}

vector<double> CrossDetector::checkIfPerpendicular(vector<vector<double>> &tempParameters)
{
    vector<vector<double>> perpendicularParams;
    vector<double> v1;
    vector<double> temp;
    double theta, rho;
    
        perpendicularParams.push_back(v1);
    
    vector<double> finalParams;
    
    for_each(execution::par, tempParameters.begin(), tempParameters.end()-2, [&perpendicularParams](vector<double> x){
        vector<double> v1;
        if(!x.empty())
        {
            if(sin(x[0]) > 0.995)
            {
                perpendicularParams[perpendicularParams.size()-1].push_back(x[0]);
                perpendicularParams[perpendicularParams.size()-1].push_back(x[1]);
                perpendicularParams.push_back(v1);
            }
        }
    });
    
    temp = countAverage(perpendicularParams);
    
    theta = temp[0];
    rho = temp[1];
    
    finalParams.push_back(tempParameters[tempParameters.size()-1][0]);
    finalParams.push_back(tempParameters[tempParameters.size()-1][1]);
    finalParams.push_back(theta);
    finalParams.push_back(rho);
    
    return finalParams;
}


vector<double> CrossDetector::countVerticalAverage(vector<vector<double>> tempParameters)
{
    vector<double> tempParams(2);
    double sumRho = 0;
    int counter = 0;
    
    for_each(execution::par, tempParameters.begin(), tempParameters.end()-1, [&sumRho, &counter](vector<double> x){
        if(x[0])
        {
            sumRho += abs(x[1]);
            counter++;
        }
    });
    
    tempParams[0] = M_PI - 3.14; //way to approach problem that some nearly-vertical lines' theta ~ 3,14, others' ~0
    tempParams[1] = sumRho/counter;
    
    return tempParams;
}

vector<double> CrossDetector::countAverage(vector<vector<double>> tempParameters)
{
    vector<double> tempParams(2);
    double sumRho = 0, sumTheta = 0;
    int counter = 0;
    
    for_each(execution::par, tempParameters.begin(), tempParameters.end()-1, [&sumTheta, &counter](vector<double> x){
        if(x[0])
        {
            sumTheta += abs(x[0]);
            counter++;
        }
    });
    
    for_each(execution::par, tempParameters.begin(), tempParameters.end()-1, [&sumRho](vector<double> x){
        if(x[0])
        {
            sumRho += abs(x[1]);
        }
    });
    
    tempParams[0] = sumTheta/counter;
    tempParams[1] = sumRho/counter;
    
    return tempParams;
}


map<string,double> CrossDetector::getIntersectionCoordinates(const cv::Mat& frame)
{
    cv::Mat cloned_frame = frame.clone();
    findLinesParameters(cloned_frame);
    
    /*
     A1*x + B1*y + C1 = 0, A2*x + B2*y + C2 = 0
     A = cosTheta, B = sinTheta, C = Rho
     
     X = (B1 * C2 - B2 * C1) / D
     Y = (A1 * C2 - A2 * C1) / D
     where D = A1 * B2 - A2 * B1
     */
    map<string, double> coordinates;
    double d,x,y;
    
    d = cos(averageParameters[0])*sin(averageParameters[2]) - cos(averageParameters[2])*sin(averageParameters[0]);
    x = (sin(averageParameters[0]) * averageParameters[3] - sin(averageParameters[2])*averageParameters[1])/d;
    y = (cos(averageParameters[0]) * averageParameters[3] - cos(averageParameters[2])*averageParameters[1])/d;
	
    normalizeCoordinates(x, y, cloned_frame);
    
    coordinates["x"] = x;
    coordinates["y"] = y;

    return coordinates;
}

void CrossDetector::normalizeCoordinates(double& x, double& y, cv::Mat frame)
{
    x = (abs(x) - (frame.size().width/2))/(frame.size().width/2);
    y = ((frame.size().height/2) - abs(y))/(frame.size().height/2);
}



