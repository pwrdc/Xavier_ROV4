//
//  logger.hpp
//  ObjectDetect
//
//  Created by Bartosz Stucke on 29/12/2018.
//  Copyright © 2018 Bartosz Stucke. All rights reserved.
//

#pragma once

#include <fstream>

using namespace std;

class Logger
{
public:
    Logger();
    Logger(double momentumPercent);
    ~Logger();
    void saveLog(int frameNumber, vector<vector<double>> linesValues, vector<double> lineAverage);
    
private:
    void makeHeader(double momentumPercent);
    fstream plik;
    string createFileName();
    string getDate();
};
