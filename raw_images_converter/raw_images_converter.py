# -*-coding: utf-8-*-

from PIL import Image

rawData = open("F:\三班\节目\DSC_0046.NEF", 'rb').read()
imgSize = (4000,6000)# the image size
img = Image.frombytes('1', imgSize, rawData)
img.save("foo.jpg")# can give any format you like .png
