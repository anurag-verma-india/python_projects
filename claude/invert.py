import xml.etree.ElementTree as ET
import base64
import io
from PIL import Image

def is_color_similar(color1, color2, threshold=15):
    """
    Check if two hex colors are similar within a given threshold.
    """
    # Remove '#' if present
    color1 = color1.lstrip('#')
    color2 = color2.lstrip('#')
    
    # Ensure full 6-digit hex
    color1 = color1 if len(color1) == 6 else color1 * 2
    color2 = color2 if len(color2) == 6 else color2 * 2
    
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
    """
    # Ensure we have an RGB or RGBA pixel
    if len(pixel) < 3:
        return pixel
    
    # Convert pixel to hex color
    r, g, b = pixel[:3]
    pixel_hex = f'#{r:02x}{g:02x}{b:02x}'
    
    # Check against color mappings
    for old_color, new_color in color_mappings.items():
        if is_color_similar(pixel_hex, old_color, threshold):
            # Convert new color to RGB
            new_color = new_color.lstrip('#')
            new_rgb = (
                int(new_color[0:2], 16), 
                int(new_color[2:4], 16), 
                int(new_color[4:6], 16)
            )
            
            # Preserve alpha if it exists
            return new_rgb + pixel[3:] if len(pixel) == 4 else new_rgb
    
    return pixel

def convert_svg_colors(input_file, output_file, color_mappings):
    """
    Convert colors in an SVG file and its embedded images.
    """
    # Parse the SVG file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Register namespaces
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    
    # Attributes to check for color conversion
    color_attrs = ['fill', 'stroke', 'stop-color']
    
    def process_element(element):
        # Convert color attributes
        for attr in color_attrs:
            color = element.get(attr, '')
            if color and color.startswith('#'):
                for old_color, new_color in color_mappings.items():
                    if is_color_similar(color, old_color):
                        element.set(attr, new_color)
                        break
        
        # Handle image elements
        if element.tag.endswith('}image'):
            href_attr = '{http://www.w3.org/1999/xlink}href'
            href = element.get(href_attr, '')
            
            # Check for base64 encoded images
            if href.startswith('data:image'):
                try:
                    # Extract base64 data
                    prefix, base64_data = href.split(',', 1)
                    
                    # Decode image
                    image_bytes = base64.b64decode(base64_data)
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Convert to RGBA
                    image = image.convert('RGBA')
                    
                    # Create new image for converted pixels
                    new_image = Image.new('RGBA', image.size)
                    
                    # Convert pixels
                    for x in range(image.width):
                        for y in range(image.height):
                            pixel = image.getpixel((x, y))
                            new_pixel = convert_pixel_color(pixel, color_mappings)
                            new_image.putpixel((x, y), new_pixel)
                    
                    # Save converted image to bytes
                    img_byte_arr = io.BytesIO()
                    new_image.save(img_byte_arr, format='PNG')
                    
                    # Encode back to base64
                    converted_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                    
                    # Update image href
                    new_href = f'{prefix},{converted_base64}'
                    element.set(href_attr, new_href)
                
                except Exception as e:
                    print(f"Error converting image: {e}")
        
        # Process child elements
        for child in element:
            process_element(child)
    
    # Process the entire SVG tree
    process_element(root)
    
    # Write the modified SVG
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    # Color conversion mappings
    color_map = {
        '#171717': '#FFF9F5',  # Dark near-black to off-white
        '#E9E9E9': '#000000'   # Light gray to black
    }
    
    # Check command-line arguments
    import sys
    if len(sys.argv) < 3:
        print("Usage: python script.py input.svg output.svg")
        sys.exit(1)
    
    input_svg = sys.argv[1]
    output_svg = sys.argv[2]
    
    convert_svg_colors(input_svg, output_svg, color_map)
    print(f"Conversion complete. Output saved to {output_svg}")

if __name__ == "__main__":
    main()
