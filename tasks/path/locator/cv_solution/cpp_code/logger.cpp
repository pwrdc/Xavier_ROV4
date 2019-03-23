//
//  logger.cpp
//  ObjectDetect
//
//  Created by Bartosz Stucke on 29/12/2018.
//  Copyright © 2018 Bartosz Stucke. All rights reserved.
//

#include "logger.hpp"
#include <ctime>
#include <iostream>
#include <string>
#include <vector>
#include <sys/time.h>

Logger::Logger()
{
    file.open(createFileName(), ios::app);
    if(!file.is_open())
    {
        cerr << "Cannot open log file";
        exit(-1);
    }
}

Logger::Logger(double momentumPercent)
{
    file.open(createFileName(), ios::app);
    if(!file.is_open())
    {
        cerr << "Cannot open log file";
        exit(-1);
    }
    makeHeader(momentumPercent);
}

Logger::~Logger()
{
    file.close();
}

string Logger::getDate()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    time_t tp = time(NULL);
    tm *ts = localtime(&tp);
    
    string date = "[" + to_string(ts->tm_year + 1900) + "-" + to_string(ts->tm_mon + 1) + "-" + to_string(ts->tm_mday)
    + " | " + to_string(ts->tm_hour) + ":" + to_string(ts->tm_min) + ":" + to_string(ts->tm_sec) + "." + to_string(tv.tv_usec) + "]";
    
    return date;
}

string Logger::createFileName()
{
    return "Logs/PathDetection " + getDate() + ".txt";
}

void Logger::saveLog(int frameNumber, vector<vector<double>> lineValues, vector<double> lineAverage)
{
    file << "Frame: " << frameNumber << "\n";
    file << "Theta1 wartosci: " ;
    for (auto log : lineValues[0])
    {
        file << log << " ";
    }
    file << '\n';
    file << "Rho1 wartosci: ";
    for (auto log : lineValues[1])
    {
        file << log << " ";
    }
    file << '\n';
    file << "Theta2 wartosci: " ;
    for (auto log : lineValues[2])
    {
        file << log << " ";
    }
    file << '\n';
    file << "Rho2 wartosci: ";
    for (auto log : lineValues[3])
    {
        file << log << " ";
    }
    file << "\n\n";
    file << "Theta1: " << lineAverage[0] << '\n';
    file << "Rho1: " << lineAverage[1] << '\n';
    file << "Theta2: " << lineAverage[2] << '\n';
    file << "Rho2: " << lineAverage[3] << "\n\n";
}

void Logger::makeHeader(double momentumPercent)
{
    file << "Moment: " << to_string(momentumPercent) << '\n';
}
