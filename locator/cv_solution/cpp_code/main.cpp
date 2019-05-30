#include "path.hpp"
#include <iostream>

using namespace cv;

int main()
{
    const string pathImage = "green2.jpg";
    cv::Mat image = cv::imread(pathImage);
    
    PathDetector detector(pathImage);
    detector.getIntersectionCoordinates(image);

    return 0;
}
