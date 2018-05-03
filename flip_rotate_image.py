import os
from PIL import Image


def readImg(imgName):
    try:
        img_src = Image.open("face_image/" + imgName)
        print("read img!")
    except:
        print("{} is not image file!".format(imgName))
        img_src = 1
    return img_src


def spinImg(imgNames):
    for imgName in imgNames:
        img_src = readImg(imgName)
        if img_src == 1:continue
        else:
            #上下反転
            tmp = img_src.transpose(Image.FLIP_TOP_BOTTOM)
            tmp.save("flipTB_" + imgName)
            #90度回転
            tmp = img_src.transpose(Image.ROTATE_90)
            tmp.save("spin90_" + imgName)
            #270度回転
            tmp = img_src.transpose(Image.ROTATE_270)
            tmp.save("spin270_" + imgName)
            #左右反転
            tmp = img_src.transpose(Image.FLIP_LEFT_RIGHT)
            tmp.save("flipLR_" + imgName)
            print("{} is done!".format(imgName))


#read imgs names
imgNames = os.listdir("face_image")#画像が保存されてるディレクトリへのpathを書きます
print(imgNames)
spinImg(imgNames)