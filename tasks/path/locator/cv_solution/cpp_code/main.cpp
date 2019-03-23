#include "path.hpp"

int main()
{
    const string video = "a.mp4";
    const string image = "f.png";
    
    PathDetector detector{image};
    detector.run();
    
    return 0;
}
