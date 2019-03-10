#include "path.hpp"
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

int main( int argc, char** argv )
{
    //PathDetector detector("a.mp4");
    PathDetector detector("f.png");
    detector.run();
    
   
    
    
    return 0;
}
