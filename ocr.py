from PIL import Image
import pytesseract
import numpy as np

file = "1_python-ocr.jpeg"
file2 = "test2.jpg"
image1 = np.array(Image.open(file))
text = pytesseract.image_to_string(image1)

print(text)


print("test")
