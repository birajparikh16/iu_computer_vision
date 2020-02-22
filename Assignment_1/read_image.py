import sys
from PIL import Image
from PIL import ImageDraw
import numpy as np
import copy
import time
import math

sobel = np.array([[-1, 0, 1],
                 [-2, 0, 2],
                 [-1, 0, 1]])

def display_np(x):
    """
    Display a numpy array as an image
    """
    result = Image.fromarray(x.astype('uint8'))
    result.show()

def check_range(x): return np.min(x), np.max(x)

def read_image(x):
    x = Image.open('test-images/' + x).convert("L")
    x = np.array(x)
    return x

def read_list(imgs):
    return [read_image(im) for im in imgs]


def pad_image(x, kernel):
    """
    Create a new numpy array with all values 255 and then add the image in between
    i/p: image, kernel
    o/p: padded_kernelx
    """
    to_add = kernel.shape[0] - 1
    padded_image = np.full((x.shape[0] + to_add, x.shape[1] + to_add), 255)
    t = to_add // 2
    padded_image[t: padded_image.shape[0] - t, t: padded_image.shape[1] - t] = x
    return padded_image

def conv2d(image, kernel, div = 1, clip = False):
    # number of rows and columns of the kernel
    r = kernel.shape[0]
    c = kernel.shape[1]

    # initialize a canvas for the output with 255s. We will fill values in this
    output = np.full(image.shape, 255)
    for i in range(image.shape[0] - r - 1):
        for j in range(image.shape[1] - c - 1):
            output[i][j] = np.sum(kernel * image[i:i+r, j:j+c]) / div
    if clip: np.clip(output, 0, 255, out = output)
    return output
    # display_np(output)


def find_threshold(y):
    """
    Takes a number y and returns a threshold eg 3542, thresh = 3000
    eg2 16258325 thresh 10000000
    """
    # change threshold based on the value of template
    # try iterative approach for finding threshold based on
    # size of the image
    # and then combining find threshold and get indexes

    y = [int(i) for i in str(y)]
    thresh = y[0] * 10 ** (len(y) - 1)
    print(thresh)
    return thresh

def get_indexes(x, vals):
    idxs1, idxs2 = np.array([]), np.array([])
    
    # filter out close values
    
    for v in vals:
        v_idxs = np.where(x == v)
        idxs1 = np.append(idxs1 ,v_idxs[0])
        idxs2 = np.append(idxs2 ,v_idxs[1])
    return idxs1, idxs2

def temp_match(templates, padded_im, canvas):
    """
    Takes a list of templates and an image and returns the matched template
    """
    pix = Image.fromarray(padded_im.astype('uint8'))
    img = ImageDraw.Draw(pix)  
    
    for template in templates:
        # apply the hamming distance forumula
        op = conv2d(padded_im, template) + conv2d(255 - padded_im, 255 - template)

        # get the min and maximum value
        x,y = check_range(op)    

        # find threshold, eg if max val is 583 thresh = 500
        thresh = find_threshold(y)

        # get all the values above thresh
        temp_op = op[op > thresh]

        # get indexes of the values above thresh
        idxs1, idxs2 = get_indexes(op, temp_op)

        tr, tc = int(template.shape[0]), int(template.shape[1])
        cr, cc = int(canvas.shape[0]), int(canvas.shape[1])

        # if the template is not going out of the canvas, plot it
        for r,c in zip(idxs1, idxs2):
            r, c = int(r), int(c)
            if r+tr < cr and c+tc < cc:
                canvas[r:r+tr, c:c+tc] = padded_im[r:r+tr, c:c+tc]
                img.rectangle([(c,r),(c+tc,r+tr)],fill=None,outline="green")
    pix.show()
    display_np(canvas)


def preprocess(x):
    pixels = read_image(x)
    p = pad_image(pixels, sobel)
    templates = read_list(['template1.png', 'template2.png', 'template3.png'])
    canvas = np.full(p.shape, 255)
    temp_match(templates, p, canvas)


if __name__ == '__main__':
    x = sys.argv[1]
    preprocess(x)