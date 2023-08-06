import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os


def bodySegmentation(orignalImg,backgroundImg=(255,255,255),threshold=0.3):
    segmentor = SelfiSegmentation()
    img = segmentor.removeBG(orignalImg,backgroundImg,threshold)
    return img