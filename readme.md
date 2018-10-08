# Indian Government Issued PAN Card Optical Character Recognition (OCR) Project


The purpose of this WIP Project is to efficiently extract the text contained in a PAN Card image and store it in a JSON. Herein, we are using the following libraries. The current version 2.0 has been run effectively in October, 2018. Any recommendations are welcome. We also need to understand the limitations of pytesseract as it won't run on noisy images with salt & pepper grains and/or poor image quality, i.e. anything below 300 DPI. More information can be found [here](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35248.pdf)

![alt text](https://github.com/farhanchoudhary/PAN_Card_OCR_Project/blob/master/Capture_2.PNG "Inline output after execution")

The algorithm has been tested with both good quality images and of images with poor quality. The accuracy of the information extracted depends highly on the resolution of the image and the quality of the image. While Tesseract performs well on near perfect images with little or no noise, it fails in more tricky situations specially where there's reflective light on the surface of the PAN card or twists/turns etc. There are a couple of versions in this compendium repository:

  * Implemented on PyTesseract
  * Implemented using Google API [Setup your Cloud Services](https://console.cloud.google.com/home/dashboard?project=psychic-surface-217102)
  * Implemented using OCR.Space [More info here](https://ocr.space/ocrapi)
  
*__Note__: While using the API Versions of this program, kindly make sure that the image size that you're using for detection is less than 1 MB, with file size exceeding the threshold the program will render cold*

## IDE and list of libraries used:

----------------------------------

1. PyCharm Community Edition running Python 3.6
2. Pillow 
3. [pytesseract](https://opensource.google.com/projects/tesseract)
4. cv2
5. re
6. json
7. [ftfy](https://ftfy.readthedocs.io/en/latest/)
8. os
9. argparse
10. [nostril](https://www.theoj.org/joss-papers/joss.00596/10.21105.joss.00596.pdf)

![alt text](https://github.com/farhanchoudhary/PAN_Card_OCR_Project/blob/master/Capture_3.PNG "Workflow/Logic of Project")

## Usage

---------------------------------------------

Each component in this repository has specific tasks, explained as follows:

1. **__crop_morphology.py__**
   	Usage is described in the file itself. What this section does is that it crops the image to an area where it just finds textual information. For instance, if it is a scanned copy of a PAN with white background. It will crop it till where it detects the border of the PAN Card. 
   	Command: `python crop_morphology.py image_pan.jpg` 

2. **__deskew.py__**
   	The intuition can be found at [this link](https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/) about implementing deskwing and why is it important when an image to text conversion is involved. Given an image containing a rotated block of text at an unknown angle, we need to correct the text skew by:
	
	1. Detecting the block of text in the image.
		
	2. Computing the angle of the rotated text.
		
	3. Rotating the image to correct for the skew.
		
  	We typically apply text skew correction algorithms in the field of automatic document analysis, but the process itself can be applied to other domains as well. 
   	Command: `python deskew.py image_pan.jpg`

3. **__morph_final.py__**
   	An alternate version to crop_morphology.py in case the efficiency drops. More info can be found [here](http://www.danvk.org/2015/01/07/finding-blocks-of-text-in-an-image-using-python-opencv-and-numpy.html)
   	Command: `python morph_final.py image_pan.jpg`

4. **__morph_interactive.py__**
   	A playground to morph images as per your need, cycling with various parameters found [here](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Morphing.html)
   	Command: `python morph_interactive.py image_pan.jpg`
	
	Press 1 & 2 to cycle through the different modes and the CV window will show the sliders to adjust the intensity of the preprocessing steps involved. 
	
   	Note: You will need to save the image as per your need. Tesseract is not a one-stop-shop for all OCR needs, especially for PAN Cards that differ on case to case basis.

5. **__json2csv.py__**
   	Once you have converted all the files into their respective extracted JSONs, you can export them into a CSV for analysis and other usage.
	
	Command: `python json2csv.py jsons output.csv` 
	
	Note: `jsons` is the folder name and not to be specified as \jsons, the program will automatically treat the folder specified to be in the directory of the program itself. In case `output.csv` is not written into the disk, create a flat-file with the same name which will be empty and there will be no write errors.

6. **__ocr_v2.py__**
   Contrary to the name, this is the **current functional** program to extract text from the image post all steps of pre-processing.

7. **__ocr_main.py__**
   	Uses OCR Space API to extract text from image.

8. **__google_vision.py__**
   	Uses Google Vision API to extract text from image.
	
9. **__preprocess_v2.py__**
	More information on this version of preprocessing can be found [here](http://www.m.cs.osakafu-u.ac.jp/cbdar2007/proceedings/papers/O1-1.pdf) which is based on the paper *Font and Background Color Independent Binarization*. For optimum accuracy prior to running the image through the Tesseract Engine, kindly run this file. 
	
	Command: `python preprocess_v2.py input.jpg output.jpg`
	
![alt text](https://github.com/farhanchoudhary/PAN_Card_OCR_Project/blob/master/Capture.PNG "Sample of Text Extracted and placed in CSV")

# Preprocessing Commands

### Usage: `python ocr_v2.py -i image_pan.jpg -p command`

| Command     | Context | Explanation |
|-------------|:--------:|:-----------|
| `thresh`    | Linear Threshold | First, you pick a threshold value, say 127. If the pixel value is greater than the threshold, it becomes black. If less, it becomes white. OpenCV provides us with different types of thresholding methods that can be passed as the fourth parameter. I often use binary threshold for most tasks, but for other thresholding methods you may visit [the official documentation](https://docs.opencv.org/3.4.0/d7/d4d/tutorial_py_thresholding.html).|
| `adaptive` | Adaptive Threshold | There are two adaptive methods for calculating the threshold value. While **Adaptive Thresh Mean** returns the mean of the neighborhood area, **Adaptive Gaussian Mean** calculates the weighted sum of the neighborhood values.|
| `linear`    | Image Resizing | Faster image resizing|
| `cubic`      | Image Resizing | You may need to scale your image to a larger size to recognize small characters. In this case, INTER_CUBIC generally performs better than other alternatives, though it’s also slower than others.|
| `blur`    | Median Blur | In Median Blurring the central element in the kernel area is replaced with the median of all the pixels under the kernel. Particularly, this outperforms other blurring methods in removing salt-and-pepper noise in the images. Median blurring is a non-linear filter. Unlike linear filters, median blurring replaces the pixel values with the median value available in the neighborhood values. So, median blurring preserves edges as the median value must be the value of one of neighboring pixels |
| `gauss`    | Gaussian Blur | Gaussian Blurring works in a similar fashion to Averaging, but it uses Gaussian kernel, instead of a normalized box filter, for convolution. Here, the dimensions of the kernel and standard deviations in both directions can be determined independently. Gaussian blurring is very useful for removing — guess what? — gaussian noise from the image. On the contrary, gaussian blurring does not preserve the edges in the input.|
| `bilateral` | Bilateral Filtering | Speaking of keeping edges sharp, bilateral filtering is quite useful for removing the noise without smoothing the edges. Similar to gaussian blurring, bilateral filtering also uses a gaussian filter to find the gaussian weighted average in the neighborhood. However, it also takes pixel difference into account while blurring the nearby pixels. Thus, it ensures only those pixels with similar intensity to the central pixel are blurred, whereas the pixels with distinct pixel values are not blurred. In doing so, the edges that have larger intensity variation, so-called edges, are preserved. |

# Accuracy Matrix

![alt text](https://github.com/farhanchoudhary/PAN_Card_OCR_Project/blob/master/s-1.jpg "Sample")

## Way Forward

PyTesseract and the Tesseract Engine has many flaws when it comes to converting image to text, especially if the image is noisy and/or contains salt and pepper noise. This can be overcome later by implementing image classification algorithms using LSTMs for better accuracy. 

#### This is a WIP Project because eventually I plan on expanding the program into a Flask application that would be able to extract information from PAN Card, Aadhar Card, Voter ID Card, Driving License and Indian Passport with a UI feature.
