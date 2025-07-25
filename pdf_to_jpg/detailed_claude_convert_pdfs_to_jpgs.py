import os
from pdf2image import convert_from_path
from pathlib import Path
from tqdm import tqdm
import PyPDF2

def get_pdf_page_count(pdf_path):
    """
    Get the number of pages in a PDF file.
    
    Parameters:
    pdf_path (str): Path to the PDF file
    
    Returns:
    int: Number of pages in the PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
    except Exception as e:
        print(f"Warning: Could not determine page count for {pdf_path}: {e}")
        return 1  # Default to 1 if we can't determine the page count

def convert_pdfs_to_jpgs(pdf_folder, output_folder):
    """
    Converts all PDF files in the pdf_folder to JPG images and stores them in subfolders
    within the output_folder, each named after the original PDF file.
    
    Parameters:
    pdf_folder (str): Path to the folder containing the PDF files to be converted.
    output_folder (str): Path to the folder where the JPG images will be stored.
    """
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to convert.")
    
    # Overall progress bar for all files
    overall_progress = tqdm(pdf_files, desc="Overall Progress", unit="file", position=0)
    
    for pdf_file in overall_progress:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_subdir = os.path.splitext(pdf_file)[0]
        output_subpath = os.path.join(output_folder, output_subdir)
        
        # Update overall progress description
        overall_progress.set_description(f"Processing: {pdf_file}")
        
        # Create the output subfolder if it doesn't exist
        Path(output_subpath).mkdir(parents=True, exist_ok=True)
        
        # Get page count for individual file progress
        page_count = get_pdf_page_count(pdf_path)
        
        # Convert the PDF to JPG images
        try:
            images = convert_from_path(pdf_path)
            
            # Individual file progress bar
            file_progress = tqdm(
                enumerate(images), 
                total=len(images),
                desc=f"Converting {pdf_file}",
                unit="page",
                position=1,
                leave=False
            )
            
            # Save the JPG images to the output subfolder
            for i, image in file_progress:
                jpg_path = os.path.join(output_subpath, f"{output_subdir}_{i+1}.jpg")
                image.save(jpg_path, "JPEG")
                file_progress.set_postfix({"Page": f"{i+1}/{len(images)}"})
            
            file_progress.close()
            
        except Exception as e:
            print(f"Error converting {pdf_file}: {e}")
            continue
        
        # Update overall progress postfix
        overall_progress.set_postfix({"Completed": f"{overall_progress.n + 1}/{len(pdf_files)}"})
    
    overall_progress.close()
    print("\nConversion completed!")

# Alternative version with more detailed progress information
def convert_pdfs_to_jpgs_detailed(pdf_folder, output_folder):
    """
    Enhanced version with more detailed progress tracking.
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return
    
    # Calculate total pages across all PDFs for more accurate overall progress
    print("Analyzing PDF files...")
    total_pages = 0
    file_page_counts = {}
    
    for pdf_file in tqdm(pdf_files, desc="Analyzing PDFs", unit="file"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        page_count = get_pdf_page_count(pdf_path)
        file_page_counts[pdf_file] = page_count
        total_pages += page_count
    
    print(f"Found {len(pdf_files)} PDF file(s) with {total_pages} total pages to convert.")
    
    # Overall progress bar based on pages
    overall_progress = tqdm(total=total_pages, desc="Overall Progress", unit="page", position=0)
    
    for file_idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_subdir = os.path.splitext(pdf_file)[0]
        output_subpath = os.path.join(output_folder, output_subdir)
        
        # Update overall progress description
        overall_progress.set_description(f"File {file_idx}/{len(pdf_files)}: {pdf_file}")
        
        # Create the output subfolder if it doesn't exist
        Path(output_subpath).mkdir(parents=True, exist_ok=True)
        
        try:
            # Convert the PDF to JPG images
            images = convert_from_path(pdf_path)
            
            # Individual file progress bar
            file_progress = tqdm(
                enumerate(images), 
                total=len(images),
                desc=f"Converting {pdf_file}",
                unit="page",
                position=1,
                leave=False
            )
            
            # Save the JPG images to the output subfolder
            for i, image in file_progress:
                jpg_path = os.path.join(output_subpath, f"{output_subdir}_{i+1}.jpg")
                image.save(jpg_path, "JPEG")
                
                # Update both progress bars
                file_progress.set_postfix({"Page": f"{i+1}/{len(images)}"})
                overall_progress.update(1)
                overall_progress.set_postfix({
                    "File": f"{file_idx}/{len(pdf_files)}",
                    "Current": f"{pdf_file[:20]}..." if len(pdf_file) > 20 else pdf_file
                })
            
            file_progress.close()
            
        except Exception as e:
            print(f"Error converting {pdf_file}: {e}")
            # Still update overall progress even if file failed
            overall_progress.update(file_page_counts.get(pdf_file, 1))
            continue
    
    overall_progress.close()
    print("\nConversion completed!")

# Example usage
if __name__ == "__main__":
    # Basic version with progress bars
    # convert_pdfs_to_jpgs("pdfs", "output")
    
    # Uncomment the line below to use the detailed version instead
    convert_pdfs_to_jpgs_detailed("pdfs", "output")