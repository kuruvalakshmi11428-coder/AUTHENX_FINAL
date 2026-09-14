import pytesseract
from PIL import Image

image = Image.open("sample_document.png")
image.seek(0)
text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(text)