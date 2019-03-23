#include "path.hpp"

int main()
{
    const string video = "a.mp4";
    const string image = "f.png";
    PathDetector detector{video};
    detector.run();
    
    return 0;
}
