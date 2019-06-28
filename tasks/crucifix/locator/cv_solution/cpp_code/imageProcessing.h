#pragma once
#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;

namespace image
{

	class imageProcessing
	{
	private:
		static __declspec(dllexport) cv::Mat prepareImage(cv::Mat &frame, int lTH, int lTS, int lTV, int hTH, int hTS, int hTV);
		static __declspec(dllexport) void cannyEdges(cv::Mat &blurredImg);
		static __declspec(dllexport) void blurrImage(cv::Mat &imgThresholded);
		static __declspec(dllexport) void thresholdImage(cv::Mat &imgHSV, int lTH, int lTS, int lTV, int hTH, int hTS, int hTV);
		static __declspec(dllexport) void doMorphOperations(cv::Mat &imgThresholded);

	public:
		static __declspec(dllexport) vector<cv::Vec2f> detectLines(cv::Mat &image, int lTH, int lTS, int lTV, int hTH, int hTS, int hTV);
		static __declspec(dllexport) vector<cv::Vec4i> detectLinesP(cv::Mat &image, int lTH, int lTS, int lTV, int hTH, int hTS, int hTV);
	};

}