#include "BlankArea.h"

extern "C" {
  BlankArea* BlankArea_new(cv::Mat & inputImg) { return new BlankArea(inputImg); }
  void BlankArea_release(BlankArea* ba) { delete ba; }

  void scanImg(BlankArea* ba, CvSize scanBlock, CvScalar color, int thershold = 2, bool iterativeCalculate = ITERATIVE_CALCULATE_ON) { ba->scanImg(scanBlock, color, thershold, iterativeCalculate); }
  void setOutputToBlack(BlankArea* ba) { ba->setOutputToBlack(); }
  cv::Mat & getOriginalImg(BlankArea *ba) { return ba->getOriginalImg(); }
  cv::Mat & getOutputImg(BlankArea *ba) { return ba->getOutputImg(); }
  cv::Mat & getCalculatedImg(BlankArea *ba) { return ba->getCalculatedImg(); }
}
