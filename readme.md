# Indian Government Issued PAN Card Optical Character Recognition (OCR) Project


The purpose of this WIP Project is to efficiently extract the text contained in a PAN Card image and store it in a JSON. Herein, we are using the following libraries. The current version 2.0 has been run effectively in October, 2018. Any recommendations are welcome. We also need to understand the limitations of pytesseract as it won't run on noisy images with salt & pepper grains and/or poor image quality, i.e. anything below 300 DPI. More information can be found [here](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35248.pdf)

![alt text](https://github.com/farhanchoudhary/PAN_Card_OCR_Project/blob/master/Capture_2.PNG)"Inline output after execution"

The algorithm has been tested with both good quality images and of images with poor quality. The accuracy of the information extracted depends highly on the resolution of the image and the quality of the image. While Tesseract performs well on near perfect images with little or no noise, it fails in more tricky situations specially where there's reflective light on the surface of the PAN card or twists/turns etc. There are a couple of versions in this compendium repository:

  * Implemented on PyTesseract
  * Implemented using Google API [Setup your Cloud Services](https://console.cloud.google.com/home/dashboard?project=psychic-surface-217102)
  * Implemented using OCR.Space [More info here](https://ocr.space/ocrapi)

## IDE and list of libraries used:

----------------------------------

1. PyCharm Community Edition running Python 3.6
2. Pillow 
3. pytesseract
4. cv2
5. re
6. json
7. ftfy
8. os
9. argparse
10. nostril 

## Usage

---------------------------------------------

Each component in this repository has specific tasks, explained as follows:

1. **__crop_morphology.py__**
   	Usage is described in the file itself. What this section does is that it crops the image to an area where it just finds textual information. For instance, if it is a scanned copy of a PAN with white background. It will crop it till where it detects the border of the PAN Card. 
   	Command: `python crop_morphology.py image_pan.jpg` 

2. **__deskew.py__**
   	Given an image containing a rotated block of text at an unknown angle, we need to correct the text skew by:
	
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
	
![alt text](https://github.com/farhanchoudhary/PAN_Card_OCR_Project/blob/master/Capture.PNG)"Sample of Text Extracted and placed in CSV"
