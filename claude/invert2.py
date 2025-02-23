import xml.etree.ElementTree as ET
import base64
import io
from PIL import Image
import re

def is_color_similar(color1, color2, threshold=15):
    """
    Check if two hex colors are similar within a given threshold.
    
    :param color1: First hex color (e.g., '#171717')
    :param color2: Second hex color (e.g., '#171616')
    :param threshold: Maximum difference allowed in each color channel
    :return: Boolean indicating color similarity
    """
    # Remove '#' if present
    color1 = color1.lstrip('#')
    color2 = color2.lstrip('#')
    
    # Convert hex to RGB
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
    r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
    
    # Check if each color channel is within the threshold
    return (abs(r1 - r2) <= threshold and 
            abs(g1 - g2) <= threshold and 
            abs(b1 - b2) <= threshold)

def convert_pixel_color(pixel, color_mappings, threshold=15):
    """
    Convert a single pixel color based on provided mappings.
    
    :param pixel: RGB or RGBA pixel tuple
    :param color_mappings: Dictionary of {old_color: new_color}
    :param threshold: Color similarity threshold
    :return: Converted pixel color
    """
    # Convert pixel to hex color
    r, g, b = pixel[:3]
    pixel_hex = f'#{r:02x}{g:02x}{b:02x}'
    
    # Check against color mappings
    for old_color, new_color in color_mappings.items():
        if is_color_similar(pixel_hex, old_color, threshold):
            # Convert new color to RGB
            new_color = new_color.lstrip('#')
            return (int(new_color[0:2], 16), 
                    int(new_color[2:4], 16), 
                    int(new_color[4:6], 16)) + pixel[3:] if len(pixel) == 4 else ()
    
    return pixel

def convert_image_colors(image, color_mappings, threshold=15):
    """
    Convert colors in a PIL Image based on provided mappings.
    
    :param image: PIL Image object
    :param color_mappings: Dictionary of {old_color: new_color}
    :param threshold: Color similarity threshold
    :return: Modified PIL Image
    """
    # Convert image to RGBA to preserve transparency
    image = image.convert('RGBA')
    
    # Create a new image with converted pixels
    new_image = Image.new('RGBA', image.size)
    
    # Process each pixel
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            new_pixel = convert_pixel_color(pixel, color_mappings, threshold)
            new_image.putpixel((x, y), new_pixel)
    
    return new_image

def convert_svg_colors(input_file, output_file, color_mappings):
    """
    Convert colors in an SVG file and its embedded images.
    
    :param input_file: Path to input SVG file
    :param output_file: Path to output SVG file
    :param color_mappings: Dictionary of {old_color: new_color}
    """
    # Parse the SVG file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Namespaces to handle different SVG formats
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        '': 'http://www.w3.org/2000/svg'
    }
    
    # Define XPath to find elements with fill or stroke attributes
    color_attrs = ['fill', 'stroke']
    
    # Function to recursively process elements
    def process_element(element):
        for attr in color_attrs:
            color = element.get(attr, '')
            if color and color.startswith('#'):
                # Check if color needs conversion
                for old_color, new_color in color_mappings.items():
                    if is_color_similar(color, old_color):
                        element.set(attr, new_color)
                        break
        
        # Process image elements with base64 encoded images
        if element.tag.endswith('image'):
            href = element.get('{http://www.w3.org/1999/xlink}href', '')
            if href.startswith('data:image/png;base64,'):
                # Decode base64 image
                base64_data = href.split(',')[1]
                image_data = base64.b64decode(base64_data)
                
                # Open image with PIL
                image = Image.open(io.BytesIO(image_data))
                
                # Convert image colors
                converted_image = convert_image_colors(image, color_mappings)
                
                # Save converted image to bytes
                img_byte_arr = io.BytesIO()
                converted_image.save(img_byte_arr, format='PNG')
                
                # Encode back to base64
                new_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                
                # Update image href with new base64 data
                new_href = f'data:image/png;base64,{new_base64}'
                element.set('{http://www.w3.org/1999/xlink}href', new_href)
        
        # Process child elements
        for child in element:
            process_element(child)
    
    # Process the entire SVG tree
    process_element(root)
    
    # Save the modified SVG
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    # Color conversion mappings
    color_map = {
        '#171717': '#FFF9F5',  # Dark near-black to off-white
        '#E9E9E9': '#000000'   # Light gray to black
    }
    
    # Example usage
    input_svg = 'input.svg'
    output_svg = 'output.svg'
    
    convert_svg_colors(input_svg, output_svg, color_map)
    print(f"SVG and embedded PNG color conversion complete. Output saved to {output_svg}")

if __name__ == "__main__":
    main()
