#include "path.hpp"

int main()
{
    const string pathVideo = "a.mp4";
    const string pathImage = "f.png";
    cv::Mat image = cv::imread(pathImage);
    
    PathDetector detector;
    cout << detector.getRotationAngle(image) << endl;
    detector.getIntersectionCoordinates(image);
    
    return 0;
}
