#define _CRT_SECURE_NO_WARNINGS
#include "logger.hpp"
#include <ctime>
#include <iostream>
#include <string>
#include <vector>


Logger::Logger()
{
	std::cout << "Nazwa: " << createFileName() << std::endl;
    plik.open(createFileName(), ios::app);
    if(!plik.is_open())
    {
        cerr << "Plik jebnal";
        exit(-1);
    }
}

Logger::~Logger()
{
    plik.close();
}

string Logger::getData()
{
    time_t tp = time(NULL);
    tm *ts = localtime(&tp);
    string data = to_string(ts->tm_mday) + '-' + to_string(ts->tm_mon + 1) + '-' + to_string(ts->tm_year + 1900) + '_' + to_string(ts->tm_hour) + '-' + to_string(ts->tm_min);
    
    return data;
}

string Logger::createFileName()
{
    return "Logs/" + getData() + ".txt";
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
