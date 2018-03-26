#include <opencv2/opencv.hpp>
#include <iostream>
#include <time.h>
#include <vector>
#include "globalDefine.h"
#include "BlankArea.h"

using namespace std;
using namespace cv;

int main()
{
	cv::Mat inputPicture = imread("chinaz_com_g.png", 0);

	BlankArea blankArea(inputPicture);
	inputPicture.release();
	blankArea.scanImg(cvSize(120, 120), COLOR_RED, 2);
	blankArea.scanImg(cvSize(24, 24), COLOR_BLUE, 2);


	//imshow("outputImg", blankArea.getOutputImg());
	//imshow("cannyImg", blankArea.getCannyImg());
	//imshow("calculatedImg", blankArea.getCalculatedImg());
	//imshow("originalImg", blankArea.getOriginalImg());
	//imshow("integral", blankArea.getIntegralImg());

	imwrite( "test.jpg", blankArea.getOutputImg() );
	//waitKey(0);

	return 0;
}
