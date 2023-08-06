import cv2
import argparse
import re
import ctypes
from PIL import Image
import img2pdf
import os
import pytesseract
import pymongo
from pdf2image import convert_from_path
import math
from typing import Tuple, Union

import cv2
import numpy as np

from deskew import determine_skew


def rotate(
        image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + \
        abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + \
        abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


connection = pymongo.MongoClient('127.0.0.1:27017')
db = connection.invoiceocr
ref_point = []


def getinf(item):
    img1 = Image.open("page0.jpg")
    cv2.namedWindow("rectangle", cv2.WINDOW_NORMAL)
    img1 = img1.crop((item["keyword_cordinates"]["x1"]+shiftx, item["keyword_cordinates"]
                     ["y1"]+shifty, item["keyword_cordinates"]["x2"]+shiftw, item["keyword_cordinates"]["y2"]+shifth))
    image=cv2.imread('page0.jpg')
    cv2.rectangle(image,(item["keyword_cordinates"]["x1"]+shiftx, item["keyword_cordinates"]["y1"]+shifty), (item["keyword_cordinates"]["x2"]+shiftw, item["keyword_cordinates"]["y2"]+shifth), (0, 255, 0), 2)
    img1.save('img2.png')
    img1.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    print("Keyword: ", text)
    img1 = Image.open("page0.jpg")
    img1 = img1.crop((item["Date"]["x1"]+shiftx, item["Date"]
                     ["y1"]+shifty, item["Date"]["x2"]+shiftw, item["Date"]["y2"]+shifth))
    # image=cv2.imread('page0.jpg')
    cv2.rectangle(image,(item["Date"]["x1"]+shiftx, item["Date"]["y1"]+shifty), (item["Date"]["x2"]+shiftw, item["Date"]["y2"]+shifth), (0, 255, 0), 2)
    img1.save('img2.png')
    img1.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    print("Date of Invoice: ", text)

    img1 = Image.open("page0.jpg")
    img1 = img1.crop((item["Invoice_No"]["x1"]+shiftx, item["Invoice_No"]
                     ["y1"]+shifty, item["Invoice_No"]["x2"]+shiftw, item["Invoice_No"]["y2"]+shifth))
    cv2.rectangle(image,(item["Invoice_No"]["x1"]+shiftx, item["Invoice_No"]["y1"]+shifty), (item["Invoice_No"]["x2"]+shiftw, item["Invoice_No"]["y2"]+shifth), (0, 255, 0), 2)
    img1.save('img2.png')
    img1.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    print("invoice No ", text)
    img1 = Image.open("page0.jpg")
    img1 = img1.crop((item["Total Bill"]["x1"]+shiftx, item["Total Bill"]
                     ["y1"]+shifty, item["Total Bill"]["x2"]+shiftw, item["Total Bill"]["y2"]+shifth))
    cv2.rectangle(image,(item["Total Bill"]["x1"]+shiftx, item["Total Bill"]["y1"]+shifty), (item["Total Bill"]["x2"]+shiftw, item["Total Bill"]["y2"]+shifth), (0, 255, 0), 2)
    img1.save('img2.png')
    img1.close()
    # image = Image.open('img2.png')
    # image.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    print("Total Bill: ", text)
    img1 = Image.open("page0.jpg")
    img1 = img1.crop((item["Buyer"]["x1"]+shiftx, item["Buyer"]
                     ["y1"]+shifty, item["Buyer"]["x2"]+shiftw,item["Buyer"]["y2"]+shifth))
    cv2.rectangle(image,(item["Buyer"]["x1"]+shiftx, item["Buyer"]["y1"]+shifty), (item["Buyer"]["x2"]+shiftw, item["Buyer"]["y2"]+shifth), (0, 255, 0), 2)
    img1.save('img2.png')
    img1.close()
    # image = Image.open('img2.png')
    # image.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    print("Buyer: ", text)
    img1 = Image.open("page0.jpg")
    img1 = img1.crop((item["Seller"]["x1"]+shiftx, item["Seller"]
                     ["y1"]+shifty, item["Seller"]["x2"]+shiftw, item["Seller"]["y2"]+shifth))
    img1.save('img2.png')
    img1.close()
    # image = Image.open('img2.png')
    # image.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    print("Seller: ", text)
    cv2.imshow("rectangle",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def shape_selection(event, x, y, flags, param):
    # grab references to the global variables

    global ref_point2, crop

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        # ref_point = [(x, y)]
        ref_point.append((x, y))
        # it+=1
        ref_point2 = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        if(curr == 1):
            ref_point.append((x, y))
            cv2.rectangle(image, ref_point[len(
                ref_point)-1], ref_point[len(ref_point)-2], (0, 255, 0), 2)
        elif(curr == 2):
            ref_point2.append((x, y))
            cv2.rectangle(image, ref_point2[0], ref_point2[1], (0, 255, 0), 2)
        # cv2.resizeWindow("image", 1000,1500)
        cv2.imshow("image", image)


# now let's initialize the list of reference point
print("Select boxes in the order:\n1.Keyword\n2.Date of Invoice\n3.Invoice No.\n4.Buyer Details\n5.Seller Details   ")
crop = False
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--pdf", required=True, help="Path to the pdf")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
images = convert_from_path(args["pdf"])

shiftx=0
shifty=0
shiftw=0
shifth=0
for i in range(len(images)):
    images[i].save('page' + str(i) + '.jpg', 'JPEG')


found = 0
image = cv2.imread('page0.jpg')
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
angle = determine_skew(grayscale)
rotated = rotate(image, angle, (0, 0, 0))
cv2.imwrite('page0.jpg', rotated)

for document in db.invoices.find():
    img1 = Image.open("page0.jpg")
    img3 = img1.crop((document["keyword_cordinates"]["x1"], document["keyword_cordinates"]
                     ["y1"], document["keyword_cordinates"]["x2"], document["keyword_cordinates"]["y2"]))
    img3.save('img2.png')
    img3.close()
    image = Image.open('img2.png')
    image.close()
    text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
    if(text.strip()== document["keyword"].strip()):
        found = 1
        getinf(document)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if(found==0):
    for document in db.invoices.find():
        img = Image.open('page0.jpg')
        data = pytesseract.image_to_data(img, output_type='dict')
        boxes = len(data['level'])

        for i in range(boxes):
            
            if data['text'][i].strip()!= ''.strip():
                if(data['text'][i].strip()==document["keyword"].strip()):
                    shiftx=data["left"][i]-document["keyword_cordinates"]["x1"]
                    shifty=data["top"][i]-document["keyword_cordinates"]["y1"]
                    shiftw=data["left"][i]-document["keyword_cordinates"]["x1"]
                    shifth=data["top"][i]-document["keyword_cordinates"]["y1"]
                    img1 = Image.open("page0.jpg")
                    img1 = img1.crop((document["Seller"]["x1"]+shiftx, document["Seller"]
                                     ["y1"]+shifty, document["Seller"]["x2"]+shiftw, document["Seller"]["y2"]+shifth))
                    img1.save('img2.png')
                    img1.close()
                    text = str(pytesseract.image_to_string(Image.open(r"img2.png"), lang='eng'))
                
                    if( text.split("\n")[0].strip()==document["seller_key"].strip()):
                        found=1
                        break
        if(found==1):
            print("shiftx: ", shiftx, "shifty: ", shifty, "shiftw: ", shiftw, "shifth: ", shifth)
            getinf(document)
            break

if(found == 0):
    image = cv2.imread("page0.jpg")
    # image = cv2.resize(ims, ((500),1200))
    clone = image.copy()

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", shape_selection)
    curr = 1
    while True:
        cv2.imshow("image", image)
        # cv2.resizeWindow("image", 1000,1500)
        # cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            break
    if len(ref_point) >= 2:
        img1 = Image.open("page0.jpg")
        img3 = img1.crop(
            (ref_point[0][0], ref_point[0][1], ref_point[1][0], ref_point[1][1]))
        img3.save('img2.png')
        img3.close()
        image = Image.open('img2.png')
        image.close()
        text = str(pytesseract.image_to_string(
            Image.open(r"img2.png"), lang='eng'))

        myimg=Image.open('page0.jpg')
        data = pytesseract.image_to_data(myimg, output_type='dict')
        boxes = len(data['level'])
 
        for i in range(boxes):
            if data['text'][i].strip() == text.strip():
                break

        db.invoices.insert_one({"keyword":text})
        keyword = text
        db.invoices.update_one({"keyword": keyword}, {
        "$set": {"keyword_cordinates": {"x1":data["left"][i], "y1":data["top"][i], "x2": data["left"][i]+data["width"][i], "y2":data["top"][i]+data["height"][i]}}})
       

        img3 = img1.crop(
        (ref_point[2][0], ref_point[2][1], ref_point[3][0], ref_point[3][1]))
        db.invoices.update_one({"keyword": keyword}, {
        "$set": {"Date": {"x1": ref_point[2][0], "y1": ref_point[2][1], "x2": ref_point[3][0], "y2": ref_point[3][1]}}})
        img3.save('img2.png')
        img3.close()
        image = Image.open('img2.png')
        image.close()
        text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
        print("Date of Invoice: ", text)

        img3 = img1.crop(
        (ref_point[4][0], ref_point[4][1], ref_point[5][0], ref_point[5][1]))
        db.invoices.update_one({"keyword": keyword}, {
        "$set": {"Invoice_No": {"x1": ref_point[4][0], "y1": ref_point[4][1], "x2": ref_point[5][0], "y2": ref_point[5][1]}}})
        img3.save('img2.png')
        img3.close()
        image = Image.open('img2.png')
        image.close()
        text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
        print("Invoice No: ", text)

        img3 = img1.crop(
        (ref_point[6][0], ref_point[6][1], ref_point[7][0], ref_point[7][1]))
        db.invoices.update_one({"keyword": keyword}, {
        "$set": {"Total Bill": {"x1": ref_point[6][0], "y1": ref_point[6][1], "x2": ref_point[7][0], "y2": ref_point[7][1]}}})
        img3.save('img2.png')
        img3.close()
        image = Image.open('img2.png')
        image.close()
        text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
        print("Total Bill ", text)

        img3 = img1.crop(
        (ref_point[8][0], ref_point[8][1], ref_point[9][0], ref_point[9][1]))
        db.invoices.update_one({"keyword": keyword}, {
        "$set": {"Buyer": {"x1": ref_point[8][0], "y1": ref_point[8][1], "x2": ref_point[9][0], "y2": ref_point[9][1]}}})
        img3.save('img2.png')
        img3.close()
        image = Image.open('img2.png')
        image.close()
        text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
        print("Buyer: ", text)

        img3 = img1.crop(
        (ref_point[10][0], ref_point[10][1], ref_point[11][0], ref_point[11][1]))
        db.invoices.update_one({"keyword": keyword}, {
        "$set": {"Seller": {"x1": ref_point[10][0], "y1": ref_point[10][1], "x2": ref_point[11][0], "y2": ref_point[11][1]}}})
        img3.save('img2.png')
        img3.close()
        image = Image.open('img2.png')
        image.close()
        text = str(pytesseract.image_to_string(
        Image.open(r"img2.png"), lang='eng'))
        sellerkey=text.split("\n")[0]
        db.invoices.update_one({"keyword": keyword},{"$set": {"seller_key": sellerkey}})
        print("Seller: ", text)

    cv2.destroyAllWindows()
