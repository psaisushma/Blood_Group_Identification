import cv2
import numpy

# one image in screen 

# img=cv2.imread('blood_Cell.jpg')
# cv2.imshow("Read Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# loaded to multiple output screen

# img1=cv2.imread('blood_Cell.jpg',cv2.IMREAD_COLOR)
# img2=cv2.imread('blood_Cell.jpg',cv2.IMREAD_GRAYSCALE)
# cv2.imshow("Image1", img1)
# cv2.imshow("Image2", img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# loaded to single output screen

# img1=cv2.imread('blood_Cell.jpg')
# img2=cv2.imread('blood_Cell.jpg')
# imp=numpy.concatenate((img1,img2),axis=1)
# cv2.imshow("Concatenated_Images", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# save an image using opencv

# img=cv2.imread('Blood_Cell.png',cv2.IMREAD_GRAYSCALE)
# imgn='grayscale_converted_img.png'
# cv2.imwrite(imgn,img)
# # img=cv2.imread('grayscale_converted_img.jpg')
# # cv2.imshow('output',img)
# cv2.imshow('normal_img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # resize the images

# img=cv2.imread('Blood_Cell.png')

# cv2.imwrite(imgn,img)
# hi=cv2.resize(img,(0,0),fx=0.1,fy=0.1)
# li=cv2.resize(img,(700,350))
# shrinking = cv2.resize(img,(750,400),interpolation=cv2.INTER_AREA)
# cv2.imshow('normal_img',img)
# cv2.imshow('shrinking_img',shrinking)
# cv2.imshow('resized_img',hi)
# cv2.imshow('largest_img',li)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

abo_img=cv2.imread('blood_cell.jpg')
cv2.imshow('original Image', abo_img)

gr_img=cv2.cvtColor(abo_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Image', gr_img)

blur= cv2.GaussianBlur(gr_img,(5,5),0)
cv2.imshow('Blurred Image', blur)

val1,threshold =cv2.threshold(blur,120,255,cv2.THRESH_BINARY)
cv2. imshow('Threshold image', threshold)
contour, val2= cv2. findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# print(contour)
con_len=len(contour)
# print(con_len)
if(con_len<50):
    print('O')
elif(50 <= con_len< 100):
    print('A')
elif(100 <= con_len< 150):
    print('B')
else:
    print('AB')
cv2.waitKey(0)
cv2.destroyAllWindows()
