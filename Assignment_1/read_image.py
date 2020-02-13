from PIL import Image
from PIL import ImageFilter
import numpy as np

im = Image.open('test-images/music1.png').convert("L")
im.show()

# pixels = np.array(im)
# print(pixels.shape)
def check_range(x): return (np.min(x), np.max(x))


def convolve(image, kernel, div = 1):
    
    # get the pixel values
    pixels = np.array(image)
    print(check_range(pixels))

    this assumes the kernel is square
    to_remove = 4 if kernel.shape[0] == 5 else 2
    
    # how much subset of the image to take at a time eg 3*3
    size = kernel.shape[0]
    
    # initialize a canvas for the output with 0s. We will fill values in this
    output = np.zeros((pixels.shape[0] - to_remove, pixels.shape[1] - to_remove, pixels.shape[2]))
    for ch in range(pixels.shape[2]):
        for j in range(pixels.shape[1] - to_remove):
            for i in range(pixels.shape[0] - to_remove):
                output[i][j][ch] = np.sum(kernel * pixels[i:i+size, j:j+size, ch]) / div
#     print(check_range(output))
    if check_range(output)[0] < 0:
        np.clip(output, 0, 255, out=output)
    result = Image.fromarray(output.astype('uint8'))
    result.save(kernel_name + ".jpg")
    image.show()
    result.show()