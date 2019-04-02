#include "path.hpp"
#include <iostream>

int main()
{
    const string pathVideo = "a.mp4";
    const string pathImage = "f.png";
    cv::Mat image = cv::imread(pathImage);
    
    PathDetector detector; 
	std::cout << detector.getRotationAngle(image) << std::endl;
	map<std::string, double> myMap = detector.getIntersectionCoordinates(image);

	for (auto elem : myMap)
	{
		std::cout << elem.first << " " << elem.second << "\n";
	}

    return 0;
}
