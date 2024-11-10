from PIL import Image
import fitz  # PyMuPDF
import io
import os
import pandas as pd
import camelot  # For structured PDF table extraction
import numpy as np
from paddleocr import PaddleOCR  # For improved OCR on images

# Initialize PaddleOCR
ocr_model = PaddleOCR()

# Define paths
folder_path = r"E:\OneDrive_1_10-26-2024\folder"  # Folder containing both PDF and JPEG files
output_jpeg_excel_path = r"E:\OneDrive_1_10-26-2024\extracted_text_jpeg.xlsx"  # Excel file for JPEG text
output_pdf_excel_path = r"E:\OneDrive_1_10-26-2024\extracted_text_pdf.xlsx"  # Excel file for PDF text

# Lists to store extracted data
jpeg_data = []
pdf_data = []

# Function to extract text from JPEG images
def extract_text_from_images(folder_path):
    # Loop through all files in the folder and check if they are .jpg files
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            filepath = os.path.join(folder_path, filename)

            # Open and process the image
            image = Image.open(filepath)
            img_array = np.array(image)  # Convert the image to a numpy array
            text_results = ocr_model.ocr(img_array, cls=True)  # Using PaddleOCR for better results

            # Combine recognized text into a single string
            text = " ".join([result[1][0] for line in text_results for result in line])

            # Check if text is empty or contains only whitespace, and flag it if necessary
            if not text.strip():
                text = "FLAGGED:CHECK MANUALLY"  # Mark flagged images for manual inspection

            # Append filename and text to jpeg_data list
            jpeg_data.append({"Filename": filename, "Extracted Text": text})

# Function to extract text from PDF files
def extract_text_from_pdf(folder_path):
    # Loop through all files in the folder and check if they are .pdf files
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)

            # Try using Camelot for table extraction
            try:
                tables = camelot.read_pdf(filepath, pages='all')
                for i, table in enumerate(tables):
                    pdf_data.append(
                        {"Filename": f"{filename} - Table {i + 1}", "Extracted Text": table.df.to_string(index=False)}
                    )
            except Exception as e:
                if "PdfFileReader is deprecated" in str(e):
                    print(f"Deprecated warning for {filename}, switching to OCR processing.")
                    extract_pdf_with_ocr(filepath, filename)
                else:
                    print(f"Table extraction failed for {filename}: {e}")
                    # Fallback to OCR in case Camelot fails for other reasons
                    extract_pdf_with_ocr(filepath, filename)

            # Open the PDF for text extraction using PyMuPDF (fitz)
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
                        img_array = np.array(img)  # Convert the image to a numpy array
                        text_results = ocr_model.ocr(img_array, cls=True)

                        page_text = " ".join([result[1][0] for line in text_results for result in line])
                        pdf_data.append({"Filename": f"{filename} - Page {page_num + 1}", "Extracted Text": page_text})

# Function to process PDFs with OCR (for handwritten or problematic files)
def extract_pdf_with_ocr(filepath, filename):
    try:
        # Use PaddleOCR to extract text from the PDF images
        with fitz.open(filepath) as pdf:
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                img_array = np.array(img)  # Convert the image to a numpy array
                text_results = ocr_model.ocr(img_array, cls=True)

                page_text = " ".join([result[1][0] for line in text_results for result in line])
                pdf_data.append({"Filename": f"{filename} - Page {page_num + 1}", "Extracted Text": page_text})
    except Exception as e:
        print(f"OCR extraction failed for {filename}: {e}")

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
