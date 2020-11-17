import cv2
import glob
from pathlib import Path
from tqdm import tqdm

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

image_path = "../dump/semiclean1/*.jpg"
blur_path = "../dump/semiclean1/blur"
clean_path = "../dump/semiclean1/clean"

images_file = glob.glob(image_path)

for imagePath in tqdm(images_file):
    # load the image, convert it to grayscale, and compute the
    # focus measure of the image using the Variance of Laplacian
    # method
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)

    if fm < 500:
        Path(imagePath).rename(blur_path + "/" + imagePath.split('\\')[-1] )
    else:
        Path(imagePath).rename(clean_path + "/" + imagePath.split('\\')[-1] )

