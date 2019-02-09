import os.path
import json
import io
import sys
import string
import pytesseract
import re
import difflib
import csv
import dateutil.parser as dparser
try:
	from PIL import Image, ImageEnhance, ImageFilter
except:
	print("Please Install PIL - For Python 3 Users the Library is now called Pillow")
	sys.exit()
path = sys.argv[1]

img = Image.open(path)
img = img.convert('RGB') #RGBA not supported or required in Python 3 onwards
pix = img.load()

for y in range(img.size[1]):
	for x in range(img.size[0]):
		if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
			pix[x, y] = (0, 0, 0, 255)
		else:
			pix[x, y] = (255, 255, 255, 255)

img.save('temp.jpg')

text_in = pytesseract.image_to_string(Image.open('temp.jpg'))
text = list(filter(lambda x: ord(x)<128, text_in))  # TO BE CHECKED
print(text_in)

text_output = open('outputbase.txt', 'w')
text_output.write(text_in)
text_output.close()

file = open('outputbase.txt', 'r')
text = file.read()
#print(text)

# Initializing data variable
name = None
fname = None
dob = None
pan = None
nameline = []
dobline = []
panline = []
text0 = []
text1 = []
text2 = []


# Searching for PAN
lines = text.split('\n')
for lin in lines:
	s = lin.strip()
	s = s.rstrip()
	s = s.lstrip()
	text1.append(s)

#text1 = list(text1)
text1 = list(filter(None, text1))
#print(text1)

# List Object Returned in the following order

'''

Note: Hindi has the worst error rates in tesseract and creates noise in image. Tesseract doesn't work well with noisy
data 
Reference: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35248.pdf

1. Income Tax Department Government of India (the text might be distorted due to quality of image or inherent problems
with tesseractocr and its inability to distinguish seamlessly between languages not native to the module or not as 
developed - such as Hindi.)
2. Name of the PAN Card Holder
3. Father's Name
4. Date of Birth in MM/DD/YYYY format as listed in the PAN Card
5. ----Permanent Account Number---- text that is a named entity in the PAN Card (not the actual PAN Card Number)
6. Permanent Account Number in the format ABCDE1234F
7. Signature as normal text - named entity in the PAN Card

'''

lineno=0 # to start from the first line of the text file.

for wordline in text1:
	xx = wordline.split('\n')
	if ([w for w in xx if re.search('(INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
		text1 = list(text1)
		lineno = text1.index(wordline)
		break

#text1 = list(text1)
text0 = text1[lineno+1:]
#print(text0) #Contains all the relevant extracted text in form of a list - uncomment to check

#-----------Read Database
with open('namedb.csv', 'r') as f:
	reader = csv.reader(f)
	newlist = list(reader)    
newlist = sum(newlist, [])

# Searching for Name and finding closest name in database
try:
	for x in text0:
		for y in x.split():
			if(difflib.get_close_matches(y.upper(), newlist)):
				nameline.append(x)
				break
except:
	pass

try:
	name = nameline[0]
	fname = nameline[1]
	pan = text0[4]
except:
	pass
	
try:
	dobline = [item for item in text0 if item not in nameline]
	for x in dobline: # dobline contains the date of birth and the PAN Card number, here we're just interested in DOB
		z = x.split()
		z = [s for s in z if len(s) > 3]
		for y in z:
			if(dparser.parse(y, fuzzy=True)):
				dob = y
				panline = dobline[dobline.index(x)+1:]
				break
except:
	pass
	
'''try:
	for wordline in panline:
		# panline now contains the two objects as string, which will be converted to a list using split
		xx = wordline.split() # Splits the final two objects of the actual PAN Card number & Signature Entity
		if ([w for w in xx if re.search('(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$', w)]):
			pan = panline[panline.index(wordline)+1]
			break
	pan = pan.replace(" ", "")
except:
	pass'''



# Making tuples of data
data = {}
data['Name'] = name
data['Father Name'] = fname
data['Date of Birth'] = dob
data['PAN'] = pan

#print(data)

# Writing data into JSON
try:
	to_unicode = unicode
except NameError:
	to_unicode = str

# Write JSON file
with io.open('data.json', 'w', encoding='utf8') as outfile:
	str_ = json.dumps(data,
					indent=4, sort_keys=True,
					separators=(',', ': '), ensure_ascii=False)
	outfile.write(to_unicode(str_))

# Read JSON file
with open('data.json') as data_file:
	data_loaded = json.load(data_file)

#print(data == data_loaded)

# Removing dummy files
os.remove('temp.jpg')

# Reading data back JSON(give correct path where JSON is stored)
with open('data.json', 'r') as f:
	ndata = json.load(f)

print('\t', "|+++++++++++++++++++++++++++++++|")
print('\t', '|', '\t', ndata['Name'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Father Name'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Date of Birth'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['PAN'])
print('\t', "|+++++++++++++++++++++++++++++++|")

