
# B657 Assignment 1: Image Processing and Recognition Basics

# Contributors: dvasani, pphadke, bparikh, smirjank
The goal of this assignment is to build a simple Optical Music Recognition system to detect notes, quarter rests and eighth rests using the given templates. 


Figure 1: (a): A portion of a musical score. (b): Output from a simple OMR system, where notes are shown in red, quarter rests are shown in green, and eighth rests are shown in blue.

# Our approach:
We are using the Pillow library to read images in Grayscale and drawing boxes for the identified notes, quarter rests and eighth rests. We have also padded the image to avoid it from being cropped when we perform any convolution on it. Since the image has a white background originally, we have padded it with a white border to avoid false positives in the template matching step. Furthermore, we have created a 2d convolution function that will be used to perform template matching. 

# Steps performed for padding:
To perform the padding, we have created an empty canvas filled with white pixels corresponding to 255 values. 
Next, we created this canvas with size larger than the original image.
Then, we performed a convolution operation using an identity kernel on the canvas to paste the original image in the center of the canvas.

We have given priority to write an optimized code in order to make the algorithm efficient. The convolution operation is critical in the template matching step. As the size of the image increases the time required to convolve an image with the kernel also increases. Thus, we addressed that issue first and the largest of the images can be processed in an optimal manner. 



For each of these symbols, we have a black and white “template" i.e. a small “m x n” - pixel image containing just that symbol with black pixels indicating the symbol and white pixels indicating background.
We create a template matching function which computes a score for how well each region of a padded image matches with the given template. To create such function we apply a Hamming distance between the two binary images.
Mathematically,

to perform the above function, we have used a convolution function that we mentioned before.
Thus, we can see in order to convolve an image with the kernel we have to traverse through each row and column of an image with each row and column of the kernel (4 inners for loops - n4 time complexity) and hence we had to optimized the convolution operation to make time complexity - n2.

# Steps performed for Template Matching:
After we obtain the Hamming distance matrix for the padded image, the pixels having high values signify that they are a better match for the template than the rest. 
We thus choose the highest score in the matrix and normalize the whole matrix with that value. Hence, the whole matrix has values in the range of 0 to 1.
Now, we decide a threshold level after experimenting with some values such that it detects a good amount of notes, quarter rests and eighth rests for all the input images.
The pixels chosen from the previous step are stored and we plot a box on the padded image. The dimensions for the boxes are according to the size of the template we have matched. 

# Results:

# music1.png

![test](https://github.com/dipam7/iu_computer_vision/blob/master/Assignment_1/detected_music1.png)





# music2.png


![test](https://github.com/dipam7/iu_computer_vision/blob/master/Assignment_1/detected_music2.png)

# music3.png 


![test](https://github.com/dipam7/iu_computer_vision/blob/master/Assignment_1/detected_music3.png)
# music 4.png 

![test](https://github.com/dipam7/iu_computer_vision/blob/master/Assignment_1/detected_music4.png)




# rach.png


![test](https://github.com/dipam7/iu_computer_vision/blob/master/Assignment_1/detected_rach.png)
