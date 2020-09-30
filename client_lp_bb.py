import base64
from io import BytesIO
import glob
import time
import requests
from tqdm import tqdm
import numpy as np
import json
import random
import cv2
import ast
from time import sleep

from requests import Request, Session


# resizing, keeping proper proportion
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

# list all frames

image_path = ["C:/Users/Zabir/Documents/plates_test/*.jpg", "C:/Users/Zabir/Documents/jpg/*.jpg"]
# updated image path
image_path = ["C:/Users/Zabir/Documents/test_train/test_train/train/jpg/*.jpg", "C:/Users/Zabir/Documents/test_train/test_train/test/jpg/*.jpg"]
#
image_path = ["D:/dhaka-ai_competition/train/Final Train Dataset/*.jpg", "D:/dhaka-ai_competition/test1/test/*.jpg"]


# image_path = ["*.jpg", "*.jpg"] # dummy tester
save_folder_tag = ["../dump/semiclean1", "../dump/clean1"] # inside dump folder
save_folder_tag = ["../dump/semiclean2", "../dump/semiclean3"]

save_folder_tag = ["../dump/noisy1", "../dump/noisy2"]
img_cnt = 0






for i, i_path in enumerate(image_path):
    img_files = sorted(glob.glob(i_path))
    frames_names = [a for a in img_files]

    s = Session()

    

    for ori_frame_name in tqdm(frames_names):
        try:
            ori_frame = cv2.imread(ori_frame_name)

            frame = image_resize(ori_frame, width = 416)
            nf_x = ori_frame.shape[1] / frame.shape[1] # normalizing factor to convert co-ordinates from small frame to actual high-res frame
            nf_y =  ori_frame.shape[0] / frame.shape[0]


            data = base64.b64encode(frame)

            # r = requests.post("http://192.168.106.222:5000/predict_b64", data={'imgb64' : data})

            req = Request('POST', "http://192.168.106.222:5000/predict_b64", data={'imgb64' : data})

            prepped = req.prepare()

            r = s.send(prepped)

            out = ast.literal_eval(json.loads(r.json())['data'])  # json.loads(r.json())['data']
            
            # print(out)

            lp_cnt = 0
            # print(out)
            for obj in out:

                if obj[0] == 'lp':
                    xc = obj[2][0]*nf_x
                    yc = obj[2][1]*nf_y
                    w = obj[2][2]*nf_x
                    h = obj[2][3]*nf_y
                    x1 = int(xc - w/2)
                    x2 = int(xc + w/2)
                    y1 = int(yc - h/2)
                    y2 = int(yc + h/2)
                    lp_cropped = ori_frame[y1:y2, x1:x2, :]
                    try:
                        origin = save_folder_tag[i].split("/")[-1]
                        cv2.imwrite(f"{save_folder_tag[i]}/{origin}_{img_cnt}_{lp_cnt}.jpg", lp_cropped)
                        # print(f"{save_folder_tag[i]}/{origin}_{img_cnt}_{lp_cnt}.jpg")
                    except:
                        pass
                        # print("failed")
                    lp_cnt += 1

            img_cnt += 1
        except:
            time.sleep(1)
            print('failed')

