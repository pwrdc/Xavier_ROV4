#pragma once

#include <fstream>
#include <vector>

using namespace std;

class Logger
{
public:
    Logger();
    ~Logger();
    void saveLog(int frameNumber, vector<vector<double>> linesValues, vector<double> lineAverage);
    void makeHeader(double momentumPercent);
    
private:
    fstream plik;
    string createFileName();
    string getData();
   
};




