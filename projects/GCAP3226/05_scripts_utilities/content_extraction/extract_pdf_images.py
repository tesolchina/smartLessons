#!/usr/bin/env python3
"""
Extract images from PDF files
"""

import fitz  # PyMuPDF
import os
import sys
from pathlib import Path

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extract all images from a PDF file and save them to the output directory
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save extracted images
        
    Returns:
        list: List of extracted image paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the PDF
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return []
    
    extracted_images = []
    image_count = 0
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get images on this page
        image_list = page.get_images(full=True)
        
        if image_list:
            print(f"Found {len(image_list)} images on page {page_num + 1}")
        
        # Extract each image
        for img_index, img in enumerate(image_list):
            try:
                # Get image data
                xref = img[0]
                pix = fitz.Pixmap(pdf_document, xref)
                
                # Skip if image is too small (likely decorative elements)
                if pix.width < 50 or pix.height < 50:
                    pix = None
                    continue
                
                # Determine file format
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_format = "png"
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix = pix1
                    img_format = "png"
                
                # Create filename
                image_count += 1
                filename = f"page_{page_num + 1:02d}_image_{img_index + 1:02d}.{img_format}"
                img_path = os.path.join(output_dir, filename)
                
                # Save image
                pix.save(img_path)
                extracted_images.append(img_path)
                
                print(f"Extracted: {filename} ({pix.width}x{pix.height})")
                
                # Clean up
                pix = None
                
            except Exception as e:
                print(f"Error extracting image {img_index + 1} from page {page_num + 1}: {e}")
                continue
    
    pdf_document.close()
    
    print(f"\nExtracted {len(extracted_images)} images total")
    return extracted_images

def main():
    """Main function to extract images from the GCAP3226 simulation PDF"""
    
    # Set up paths
    project_root = Path(__file__).parent.parent
    pdf_path = project_root / "course_materials" / "week4" / "GCAP3226_week4_Simulation_20250920.pdf"
    output_dir = project_root / "course_materials" / "week4" / "images"
    
    print(f"PDF path: {pdf_path}")
    print(f"Output directory: {output_dir}")
    
    # Check if PDF exists
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return 1
    
    # Extract images
    extracted_images = extract_images_from_pdf(str(pdf_path), str(output_dir))
    
    if extracted_images:
        print(f"\nSuccessfully extracted {len(extracted_images)} images to {output_dir}")
        print("\nExtracted files:")
        for img_path in extracted_images:
            print(f"  - {os.path.basename(img_path)}")
    else:
        print("No images were extracted from the PDF")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())