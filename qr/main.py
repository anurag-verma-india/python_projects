import qrcode
from PIL import Image, ImageDraw, ImageFont
import sys

def generate_numbered_qr(url, output_filename="numbered_qr.png"):
    """
    Generate a QR code with numbered boxes for manual drawing reference
    
    Args:
        url (str): The URL to encode in the QR code
        output_filename (str): Name of the output image file
    """
    
    # Create QR code instance with version 2
    qr = qrcode.QRCode(
        version=2,  # Version 2 = 25x25 modules
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=40,  # Size of each box in pixels
        border=4,
    )
    
    # Add data and make the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Get the QR code matrix (True = black, False = white)
    matrix = qr.get_matrix()
    size = len(matrix)
    
    print(f"QR Code size: {size}x{size} modules")
    
    # Calculate image dimensions
    box_size = 60  # Larger boxes to fit numbers
    border_size = 4 * box_size
    img_size = size * box_size + 2 * border_size
    
    # Create image with white background
    img = Image.new('RGB', (img_size, img_size), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)  # macOS
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)  # Linux
            except:
                font = ImageFont.load_default()
    
    # Draw the QR code with numbers
    box_number = 1
    
    for row in range(size):
        for col in range(size):
            # Calculate box position
            x1 = border_size + col * box_size
            y1 = border_size + row * box_size
            x2 = x1 + box_size
            y2 = y1 + box_size
            
            # Determine if this module should be black (filled)
            is_black = matrix[row][col]
            
            if is_black:
                # Draw black border for black modules
                draw.rectangle([x1, y1, x2, y2], fill='white', outline='black', width=2)
                
                # Add number in the center
                text = str(box_number)
                
                # Get text size for centering
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                text_x = x1 + (box_size - text_width) // 2
                text_y = y1 + (box_size - text_height) // 2
                
                draw.text((text_x, text_y), text, fill='red', font=font)
                box_number += 1
            else:
                # Draw light gray border for white modules (for reference)
                draw.rectangle([x1, y1, x2, y2], fill='white', outline='lightgray', width=1)
    
    # Save the image
    img.save(output_filename)
    print(f"QR code saved as: {output_filename}")
    print(f"Total boxes to fill: {box_number - 1}")
    
    # Generate text instructions
    generate_drawing_instructions(matrix, f"drawing_instructions_{output_filename.split('.')[0]}.txt")

def generate_drawing_instructions(matrix, filename):
    """Generate text file with drawing instructions"""
    size = len(matrix)
    
    with open(filename, 'w') as f:
        f.write("QR CODE DRAWING INSTRUCTIONS\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Grid size: {size}x{size}\n")
        f.write("Fill in the boxes with the following numbers:\n\n")
        
        box_number = 1
        for row in range(size):
            row_boxes = []
            for col in range(size):
                if matrix[row][col]:  # If black module
                    row_boxes.append(f"{box_number}")
                    box_number += 1
                else:
                    row_boxes.append("  ")
            
            f.write(f"Row {row + 1:2d}: {' '.join(f'{box:>3}' for box in row_boxes)}\n")
        
        f.write(f"\nTotal boxes to fill: {box_number - 1}\n")
        f.write("\nInstructions:\n")
        f.write("1. Draw a grid with the dimensions shown above\n")
        f.write("2. Fill in the numbered boxes (shown in the image) with black\n")
        f.write("3. Leave all other boxes white\n")
        f.write("4. Make sure the pattern matches exactly for the QR code to work\n")
    
    print(f"Drawing instructions saved as: {filename}")

if __name__ == "__main__":
    # Get URL from command line or use default
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter the URL to encode: ")
    
    # Generate the numbered QR code
    generate_numbered_qr(url)
    
    print("\nTo use this script:")
    print("python qr_generator.py 'https://example.com'")
    print("\nOr run without arguments to enter URL interactively.")