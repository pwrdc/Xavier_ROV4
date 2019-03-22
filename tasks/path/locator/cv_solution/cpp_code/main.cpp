#include "path.hpp"

int main()
{
    string video = "a.mp4", image = "f.png";
    PathDetector detector(image);
    detector.run();
    
    return 0;
}
