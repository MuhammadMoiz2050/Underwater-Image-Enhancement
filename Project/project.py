import numpy as np
import skimage
import cv2
from PIL import Image,ImageOps
from matplotlib.pyplot import imshow,title,figure
from matplotlib import pyplot as plt
import math
import scipy
from skimage import io,color
from skimage.color import rgb2lab, lab2rgb

img_path = r'G:\University Stuff\8th semester\Dip\Project\Dip proj\19I_0692_Muhmmad Moiz Sajid\Picture1.png'

def main(img_path):

    def plot_histogram(channel, title):
        flattened_channel = channel.ravel()
        # plt.hist(flattened_channel, bins=256, range=[0, 256])
        plt.title(title)
        # plt.show()

    def apply_clahe(channel, clipLimit, tileGridSize):
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        return clahe.apply(channel)

    # Load the image
    img = cv2.imread(img_path)

    # Display the original image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.title("1 Original Image")
    # plt.imshow(img_rgb)
    # plt.show()

    #Feature 1: Channel Splitting
    b, g, r = cv2.split(img)

    #Feature 2: Display the histograms of the color channels
    plot_histogram(r, "Red Channel Histogram")
    plot_histogram(g, "Green Channel Histogram")
    plot_histogram(b, "Blue Channel Histogram")

    #Feature 3: Apply CLAHE to each color channel
    r_clahe = apply_clahe(r, clipLimit=6, tileGridSize=(4, 4))
    g_clahe = apply_clahe(g, clipLimit=1, tileGridSize=(2, 2))
    b_clahe = apply_clahe(b, clipLimit=1, tileGridSize=(2, 2))

    #Feature 4: Display the histograms of the CLAHE-adjusted color channels
    plot_histogram(r_clahe, "CLAHE-Adjusted Red Channel Histogram")
    plot_histogram(g_clahe, "CLAHE-Adjusted Green Channel Histogram")
    plot_histogram(b_clahe, "CLAHE-Adjusted Blue Channel Histogram")

    # Merge the color channels and display the resulting image
    merged = cv2.merge([b_clahe, g_clahe, r_clahe])
    img_clahe_rgb = cv2.cvtColor(merged, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(22, 12))
    # plt.title("2 Contrast Adjusted img")
    # plt.imshow(img_clahe_rgb)
    # plt.show()


    #Feature 5: sharpening the edges, convolving using the sharpening filter
    sharpKernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpImg = cv2.filter2D(src=img_clahe_rgb, ddepth=-1, kernel=sharpKernel)
    plt.figure(figsize = (22,12))
    # plt.title("3 Sharpened image")
    # plt.imshow(sharpImg)
    # plt.show()

    #saving image
    cv2.imwrite('contrastedImg.jpg', img_clahe_rgb)

    #Feature 6 LAB colour space conversion
    labImg = cv2.cvtColor(img_clahe_rgb, cv2.COLOR_BGR2LAB)  #merged img

    # Copying image for colour preservation
    copyLab = np.copy(labImg)

    #converting into grayscale
    copyLab[...,1] = copyLab[...,2] = 0
    # plt.title("4 LAB colour space img in gray scale")
    # plt.imshow(copyLab[...,0],cmap='gray')
    # plt.show()


    #-----------------------------------

    # creating a blurred copy for masking
    imageBlur = np.copy(copyLab[...,0].astype(np.uint8))
    blurred = cv2.GaussianBlur(imageBlur, (15,15),0) 

    #using the blur image for creating mask
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # plt.title("5 Binary Mask")
    # plt.imshow(thresh, cmap='gray')
    # plt.show()

    #Dilation and erosion of image

    kernel_size = (9,9)
    kernel = np.ones(kernel_size, np.uint8)
    dilated_img = cv2.dilate(thresh, kernel, iterations = 2)
    eroded_img = cv2.erode(dilated_img, kernel)

    # plt.title("6 Morphological operated mask")
    # plt.imshow(eroded_img,cmap='gray')
    # plt.show()

    #Foreground Extraction
    foreground = cv2.bitwise_and(dilated_img,imageBlur)
    # plt.title("7 Foreground")
    # imshow(foreground,cmap='gray')
    # plt.show()

    #Background separation for contrast adjustment
    background = cv2.bitwise_and(~dilated_img, imageBlur)
    # plt.title("8 Background")
    # imshow(background,cmap='gray')
    # plt.show()


    #Apply contrast adjustment to the background
    clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(2,2))
    background_clahe = clahe.apply(background)
    # plt.title("9 Contrast adjusted")
    # fig, ax = plt.subplots(figsize=(22, 12))
    # plt.imshow(background_clahe, cmap='gray')
    # plt.show()

    #Merge the foreground and background
    enhanced_img = cv2.bitwise_or(background_clahe, foreground)
    # plt.title("10 Enhanced image")
    # imshow(enhanced_img,cmap='gray')
    # plt.show()


    #Merging the enhanced background and foreground
    # copyLab = np.dstack((enhanced_img, labImg[..., 1], labImg[..., 2]))

    copyLab[...,0] = enhanced_img
    copyLab[...,1] = labImg[...,1]
    copyLab[...,2] = labImg[...,2]
    #Convert back to RGB
    # lab_inverted = color.lab2rgb(copyLab)
    # convert the LAB image to BGR color space
    bgr = cv2.cvtColor(copyLab, cv2.COLOR_LAB2BGR)

    # convert the BGR image to RGB color space
    lab_inverted = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


    # plt.title("11 final output")
    # figure(figsize = (22,12))
    # plt.imshow(bgr)
    # plt.show()

    #saving the final output
    cv2.imwrite('finaloutput.jpg', lab_inverted)

if __name__ == "__main__":
    main(img_path)