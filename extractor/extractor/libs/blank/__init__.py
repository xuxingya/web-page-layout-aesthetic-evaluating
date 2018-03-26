#!/usr/bin/python
import cv
import numpy as np

class BlankArea:
  def __init__(self, img):
    self.img = cv.fromarray(img)
    self.width = self.img.cols
    self.height = self.img.rows
    self.cannyImg = cv.CreateMat(self.height, self.width, cv.CV_8UC1)
    self.outputImg = cv.CreateMat(self.height, self.width, cv.CV_8UC3)
    self.integralImg = cv.CreateMat(self.height+1, self.width+1, cv.CV_32FC1)
    self.calculatedImg = cv.CreateMat(self.height, self.width, cv.CV_8UC1)

    cv.Canny(self.img, self.cannyImg, 40, 100)
    cv.Integral(self.cannyImg, self.integralImg)
    cv.Set(self.calculatedImg, 0)
    cv.Set(self.outputImg, 0)

  def scanImg(self, scanBlock, color=None, thershold=4, iterativeCalculate=True):
    self.temporary_img = cv.CreateMat(self.height, self.width, cv.CV_8UC1)
    cv.Set(self.temporary_img, 0)
    for h in range(self.height):
      for w in range(self.width):
        if iterativeCalculate and self.calculatedImg[h, w] != 0:
          continue

        for i,j in ((1,1), (1,-1), (-1, 1), (-1, -1)):
          pixelValue = self.getIntegralPixelValue(w, h, (scanBlock[0]*i, scanBlock[1]*j), i*j)
          if pixelValue < thershold:
            self.setThisPoint(w, h, color, scanBlock, (i,j))
            break

  def setThisPoint(self, w, h, color, block, step):
    for sw in range(w, w+block[0], step[0]):
      for sh in range(h, h+block[1], step[1]):
        self.calculatedImg[sh, sw] = 255
        self.temporary_img[sh, sw] = 255
        if(color):
          self.outputImg[sh, sw] = color

  def subGetIntegralPixelValue(self, w, h, scanBlock):
    sw, sh = scanBlock
    pixelValue = self.integralImg[h+sh, w+sw] - self.integralImg[h+sh, w] - self.integralImg[h, w+sw] + self.integralImg[h, w]
    return pixelValue

  def getIntegralPixelValue(self, w, h , scanBlock, d): 
    sw, sh = scanBlock
    if (w+sw > self.width-1 or w+sw<0 or h+sh>self.height-1 or h+sh < 0): 
      return 65536

    return self.subGetIntegralPixelValue(w,h, (sw, sh)) * d

  def getTemporaryImage(self):
    return np.asarray(self.temporary_img)

  def getContours(self):
    color = 100

    contours = []
    roi = []
    for w in range(self.width):
      for h in range(self.height):
        if self.temporary_img[h, w] == 255:
          cc = cv.FloodFill(self.temporary_img, (w,h), color)
          contours.append(cc[0])
          roi.append(cc[2])

    return contours,roi


if __name__ == '__main__':
  import cv2, os
  img = cv2.imread(os.path.join(os.path.dirname(__file__),'src/chinaz_com_g.png'), 0);
  ba = BlankArea(img)

  ba.scanImg((32,32), (0,0,255), 3)
  #ba.scanImg((10,10), (255,0,0), 3)
  print ba.getContours()
  print ba.temporary_img[0,0]
  #cv.FloodFill(ba.temporary_img, (1275, 660), 100)
  #print ba.temporary_img[660, 1275]
  cv2.imwrite('test.jpg', np.asarray(ba.temporary_img))
