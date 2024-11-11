import os
from pdf2image import convert_from_path
from pathlib import Path

def convert_pdfs_to_jpgs(pdf_folder, output_folder):
    """
    Converts all PDF files in the pdf_folder to JPG images and stores them in subfolders
    within the output_folder, each named after the original PDF file.

    Parameters:
    pdf_folder (str): Path to the folder containing the PDF files to be converted.
    output_folder (str): Path to the folder where the JPG images will be stored.
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_subdir = os.path.splitext(pdf_file)[0]
        output_subpath = os.path.join(output_folder, output_subdir)

        # Create the output subfolder if it doesn't exist
        Path(output_subpath).mkdir(parents=True, exist_ok=True)

        # Convert the PDF to JPG images
        images = convert_from_path(pdf_path)

        # Save the JPG images to the output subfolder
        for i, image in enumerate(images):
            jpg_path = os.path.join(output_subpath, f"{output_subdir}_{i+1}.jpg")
            image.save(jpg_path, "JPEG")

        print(f"Converted {pdf_file} to JPG images in {output_subpath}")

# Example usage
# convert_pdfs_to_jpgs("path/to/pdf/folder", "path/to/output/folder")
convert_pdfs_to_jpgs("pdfs", "output")
