#include "path.hpp"
#include <iostream>

using namespace cv;

int main()
{
    const string pathImage = "";
    cv::Mat image = cv::imread(pathImage);
    
    PathDetector detector(pathImage);
    detector.run();

    return 0;
}
