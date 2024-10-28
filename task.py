import os
import pytesseract
from PIL import Image
import pandas as pd
import fitz # PyMuPDF
folder_path = r'E:\OneDrive_1_10-26-2024\folder'
#folder obj that holds filepath
# Lists to store extracted data for images and PDFs
image_data = []
pdf_data = []
# Function to extract text from images
def extract_text_from_image(image_path):
img = Image.open(image_path)
text = pytesseract.image_to_string(img) # Extract text using Tesseract
return text.strip()
# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
text = ""
doc = fitz.open(pdf_path) # Open the PDF file
for page in doc: # Iterate through each page
text += page.get_text() + "\n" # Extract text from the page
return text.strip()
# Process each file in the directory
for filename in os.listdir(folder_path):
file_path = os.path.join(folder_path, filename)
if filename.lower().endswith(('.jpg', '.jpeg')):
# Extract text from image
extracted_text = extract_text_from_image(file_path)
image_data.append([filename, extracted_text]) # Store filename and text
elif filename.lower().endswith('.pdf'):
# Extract text from PDF
extracted_text = extract_text_from_pdf(file_path)
pdf_data.append([filename, extracted_text]) # Store filename and text
# Create DataFrames from the extracted data
image_df = pd.DataFrame(image_data, columns=["Filename", "Extracted Text"])
pdf_df = pd.DataFrame(pdf_data, columns=["Filename", "Extracted Text"])
# Save DataFrames to CSV files
image_df.to_csv(os.path.join(folder_path, 'images_extracted.csv'), index=False)
pdf_df.to_csv(os.path.join(folder_path, 'pdfs_extracted.csv'), index=False)
print("Text extraction complete. CSV files created.")
