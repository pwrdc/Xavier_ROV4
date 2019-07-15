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
#include <map>

namespace constants
{
    typedef const map<int, string> parameters_map_type;
    parameters_map_type param_map{{0, "Theta1: "},{1, "Rho1: "},{2, "Theta2: "}, {3, "Rho2: "}};
}

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
    return "Logs/PathDetection " + getDate() + ".log";
}

void Logger::saveLog(int frameNumber, vector<vector<double>> lineValues, vector<double> lineAverage)
{
    file << "Date: " << getDate() << "\n";
    file << "Frame: " << frameNumber << "\n";
    for (int i = 0; i < lineValues.size(); i ++)
    {
        file << constants::param_map.find(i)->second;
        for (auto log : lineValues[i])
        {
            file << log << " ";
        }
        file << '\n';
    }
    file << "\n";
    file << "Theta1 average: " << lineAverage[0] << '\n' << "Rho1 average: " << lineAverage[1] << '\n';
    file << "Theta2 average: " << lineAverage[2] << '\n' << "Rho2 average: " << lineAverage[3] << '\n';
}

void Logger::makeHeader(double momentumPercent)
{
    file << "Moment: " << to_string(momentumPercent) << '\n';
}
