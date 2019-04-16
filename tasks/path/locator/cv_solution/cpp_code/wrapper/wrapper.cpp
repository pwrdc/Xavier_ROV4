#define BOOST_PYTHON_STATIC_LIB
#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API
#include <boost/python.hpp>
#include <boost/python/dict.hpp>
#include <pyboostcvconverter/pyboostcvconverter.hpp>
#include <opencv2/opencv.hpp>
#include "path.hpp"

using namespace boost::python;

#if (PY_VERSION_HEX >= 0x03000000)
	static void *init_ar() {
#else
	static void init_ar() {
#endif
	Py_Initialize();

	import_array();
	return NUMPY_IMPORT_ARRAY_RETVAL;
	}

BOOST_PYTHON_MODULE (path_detection_cv) {
	init_ar();
    to_python_converter<cv::Mat,pbcvt::matToNDArrayBoostConverter>();
	pbcvt ::matFromNDArrayBoostConverter();

	class_<PathDetector>("path_detector", init<>())
		.def("get_path_cordinates", &PathDetector::getIntersectionCoordinates)
		.def("get_rotation_angle", &PathDetector::getRotationAngle)
		;
}
