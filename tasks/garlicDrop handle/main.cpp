#include "GarlicDropLeverDetector.hpp"
#include <iostream>

using namespace std;
using namespace cv;

int main()
{
    const std::string pathImage = "1.png";
    cv::Mat image = cv::imread(pathImage);
    
    GarlicDropLeverDetector detector(pathImage);
    detector.getLeverCoordinates(image);

    return 0;
}
