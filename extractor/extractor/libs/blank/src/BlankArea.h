#include <opencv2/opencv.hpp>
#include "globalDefine.h"
#include <iostream>

using namespace std;

class BlankArea
{
public:
	BlankArea(cv::Mat& inputImg);
	void scanImg(CvSize scanBlock, CvScalar color, int thershold = 2, bool iterativeCalculate = ITERATIVE_CALCULATE_ON);
	void setOutputToBlack(){ outputImg.setTo(0); }
	cv::Mat & getOutputImg(){ return outputImg; }
	cv::Mat & getOriginalImg(){ return originalImg; }
	cv::Mat & getCannyImg(){ return cannyImg; }
	cv::Mat & getCalculatedImg(){ return calculatedImg; }
	cv::Mat & getIntegralImg(){ return integralImg; }
private:
	int width, height;
	cv::Mat originalImg;
	cv::Mat cannyImg;
	cv::Mat integralImg;
	cv::Mat calculatedImg;
	cv::Mat outputImg;
	void inline setThisPoint(int w, int h, CvSize block, int step[], CvScalar color);
	int inline getIntegralPixelValue(int w, int h, CvSize scanBlock, int d);
	int inline subGetIntegralPixelValue(int w, int h, CvSize scanBlock);
};

BlankArea::BlankArea(cv::Mat& inputImg)
{
	inputImg.copyTo(originalImg);
	width = originalImg.cols;
	height = originalImg.rows;
	cv::Canny(inputImg, cannyImg, 20, 40);
	cv::integral(cannyImg, integralImg);
	calculatedImg.create(originalImg.size(), CV_8UC1);
	outputImg.create(originalImg.size(), CV_8UC3);
	calculatedImg.setTo(0);
	outputImg.setTo(0);
}

void BlankArea::scanImg(CvSize scanBlock, CvScalar color,int thershold, bool iterativeCalculate)
{
	int w, h;
	for (h = 0; h < height; ++h){
		for (w = 0; w < width; ++w){
			//if this point has been calculated before, skip
			if (iterativeCalculate == ITERATIVE_CALCULATE_ON &&
				*(calculatedImg.ptr(h) + w) != 0)
				continue;

			//test whether scanBlock is capatible with this point
			int step [4][2] = {
				{ 1, -1 },
				{ 1, 1 },
				{ -1, -1 },
				{ -1, 1}
			};
			int i;
			for (i = 0; i < 4; i++) {
				CvSize x = cvSize(0,0);
				x.width = step[i][0] * scanBlock.width;
				x.height = step[i][1] * scanBlock.height;
				int pixelValue = getIntegralPixelValue(w, h, x, step[i][0]*step[i][1]);
				if (pixelValue < thershold){
					setThisPoint(w,h,x,step[i],color);
					break;
				}
			}
			
		}
	}
}

void inline BlankArea::setThisPoint(int w, int h, CvSize block, int step[], CvScalar color)
{
	int bw = w + block.width;
	int bh = h + block.height;
	while(w!=bw){
		while(h!=bh){
			*(calculatedImg.ptr(h) + w) = 255;
			for (int i = 0; i < 3;++i)
				*(outputImg.ptr(h) + 3 * w + i) = color.val[i];
			h += step[1];
		}
		w += step[0];
	}
}

int inline BlankArea::subGetIntegralPixelValue(int w, int h, CvSize scanBlock)
{
	int pixelValue =
		*(integralImg.ptr<int>(h + scanBlock.height) + w + scanBlock.width)
		- *(integralImg.ptr<int>(h + scanBlock.height) + w)
		- *(integralImg.ptr<int>(h) +w + scanBlock.width)
		+ *(integralImg.ptr<int>(h) +w);
	return pixelValue;
}

int inline BlankArea::getIntegralPixelValue(int w, int h, CvSize scanBlock, int d=1)
{
	if (w + scanBlock.width > width - 1 || w+scanBlock.width < 0 
	|| h + scanBlock.height > height - 1 || h+scanBlock.height <0)
		return 65536;
	return subGetIntegralPixelValue(w, h,scanBlock)*d;
}
