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

Logger::Logger()
{
    plik.open(createFileName(), ios::app);
    if(!plik.is_open())
    {
        cerr << "Cannot open log file";
        exit(-1);
    }
}

Logger::Logger(double momentumPercent)
{
    plik.open(createFileName(), ios::app);
    if(!plik.is_open())
    {
        cerr << "Cannot open log file";
        exit(-1);
    }
    makeHeader(momentumPercent);
}

Logger::~Logger()
{
    plik.close();
}

string Logger::getDate()
{
    time_t tp = time(NULL);
    tm *ts = localtime(&tp);
    string date = to_string(ts->tm_mday) + '-' + to_string(ts->tm_mon + 1) + '-' + to_string(ts->tm_year + 1900) + '_' + to_string(ts->tm_hour) + '-' + to_string(ts->tm_min);
    
    return date;
}

string Logger::createFileName()
{
    return "Logs/" + getDate() + ".txt";
}

void Logger::saveLog(int frameNumber, vector<vector<double>> lineValues, vector<double> lineAverage)
{
    plik << "Frame: " << frameNumber << "\n";
    plik << "Theta1 wartosci: " ;
    for (auto log : lineValues[0])
    {
        plik << log << " ";
    }
    plik << '\n';
    plik << "Rho1 wartosci: ";
    for (auto log : lineValues[1])
    {
        plik << log << " ";
    }
    plik << '\n';
    plik << "Theta2 wartosci: " ;
    for (auto log : lineValues[2])
    {
        plik << log << " ";
    }
    plik << '\n';
    plik << "Rho2 wartosci: ";
    for (auto log : lineValues[3])
    {
        plik << log << " ";
    }
    plik << "\n\n";
    plik << "Theta1: " << lineAverage[0] << '\n';
    plik << "Rho1: " << lineAverage[1] << '\n';
    plik << "Theta2: " << lineAverage[2] << '\n';
    plik << "Rho2: " << lineAverage[3] << "\n\n";
}

void Logger::makeHeader(double momentumPercent)
{
    plik << "Moment: " << to_string(momentumPercent) << '\n';
}
