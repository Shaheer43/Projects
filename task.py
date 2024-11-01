import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io
import os
import glob
import pandas as pd

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Administrator\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Define paths
folder_path = r"E:\OneDrive_1_10-26-2024\folder"  # Folder containing both PDF and JPEG files
output_jpeg_excel_path = r"E:\OneDrive_1_10-26-2024\extracted_text_jpeg.xlsx"  # Excel file for JPEG text
output_pdf_excel_path = r"E:\OneDrive_1_10-26-2024\extracted_text_pdf.xlsx"  # Excel file for PDF text

# Lists to store extracted data
jpeg_data = []
pdf_data = []

# Function to extract text from JPEG images
def extract_text_from_images(folder_path):
    for filepath in glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.jpeg")):
        filename = os.path.basename(filepath)

        # Open and process the image
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

        # Check if text is empty or contains only whitespace, and flag it if necessary
        if not text.strip():  # Check if text is empty or whitespace
            text = "FLAGGED:CHECK MANUALLY"

        # Append filename and text to jpeg_data list
        jpeg_data.append({"Filename": filename, "Extracted Text": text})

# Function to extract text from PDF files
def extract_text_from_pdf(folder_path):
    for filepath in glob.glob(os.path.join(folder_path, "*.pdf")):
        filename = os.path.basename(filepath)

        # Open the PDF
        with fitz.open(filepath) as pdf:
            for page_num in range(len(pdf)):
                page = pdf[page_num]

                # Extract text directly if available
                page_text = page.get_text()

                if page_text.strip():
                    pdf_data.append({"Filename": f"{filename} - Page {page_num + 1}", "Extracted Text": page_text})
                else:
                    # If no text, use OCR on the page image
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    page_text = pytesseract.image_to_string(img)
                    pdf_data.append({"Filename": f"{filename} - Page {page_num + 1}", "Extracted Text": page_text})

# Run extraction functions
extract_text_from_images(folder_path)
extract_text_from_pdf(folder_path)

# Save JPEG data to a separate Excel file
df_jpeg = pd.DataFrame(jpeg_data)
df_jpeg.to_excel(output_jpeg_excel_path, index=False)

# Save PDF data to a separate Excel file
df_pdf = pd.DataFrame(pdf_data)
df_pdf.to_excel(output_pdf_excel_path, index=False)

print(f"Text extracted from JPEG images and saved to {output_jpeg_excel_path}")
print(f"Text extracted from PDF files and saved to {output_pdf_excel_path}")
