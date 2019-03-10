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
    ~Logger();
    void saveLog(int frameNumber, vector<vector<double>> linesValues, vector<double> lineAverage);
    void makeHeader(double momentumPercent);
    
private:
    fstream plik;
    string createFileName();
    string getData();
   
};




