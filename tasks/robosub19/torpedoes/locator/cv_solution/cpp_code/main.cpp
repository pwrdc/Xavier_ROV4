#include "HolderDetector.hpp"
#include <iostream>

using namespace cv;

int main()
{
    const std::string pathImage = "zdj1.png";
    cv::Mat image = cv::imread(pathImage);
    
    HolderDetector detector(pathImage);
    detector.getLeverCoordinates(image);
    
    return 0;
}
