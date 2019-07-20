#include "VampireLeverDetector.hpp"
#include <iostream>

using namespace std;
using namespace cv;

int main()
{
    const std::string pathImage = "Vampire.png";
    cv::Mat image = cv::imread(pathImage);
    
    VampireLeverDetector detector(pathImage);
    detector.getLeverCoordinates(image);
    
    return 0;
}
