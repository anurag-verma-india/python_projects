# working
# ""
# Make a python script that generates a version 2 QR code (white background and black lines)
# Add numbers every QR code cell (each number has sequence wise cell numbers)

# Save that photo to the same folder as this script
# """

# First, install the required libraries:
# pip install "qrcode[pil]"

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os


def get_font(size):
    """
    Tries to load a common TrueType font from the system.
    Falls back to the default bitmap font if common fonts are not found.
    """
    # Common fonts on Linux and Windows
    font_names = ["DejaVuSans.ttf", "arial.ttf", "Verdana.ttf"]
    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue

    print(
        "Warning: Common TrueType fonts not found. Falling back to the default bitmap font."
    )
    return ImageFont.load_default()


def create_numbered_qr_image(data, filename="numbered_qr_code.png"):
    """
    Generates a version 2 QR code with sequentially numbered cells
    and saves it as a PNG image.
    """
    # --- 1. Generate the QR code structure ---
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=25,  # The size of each cell in pixels
        border=4,  # The width of the border (quiet zone) in cells
    )
    qr.add_data(data)
    qr.make(fit=False)

    # --- 2. Create a base image from the QR code ---
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    draw = ImageDraw.Draw(img)

    # --- 3. Set up for drawing numbers ---
    qr_dimension = len(qr.modules)
    box_size = qr.box_size
    border_pixels = qr.border * box_size

    font_size = int(box_size / 2.2)
    font = get_font(font_size)

    # --- 4. Iterate over each cell to draw the number ---
    cell_number = 1
    for row_index in range(qr_dimension):
        for col_index in range(qr_dimension):
            is_black = qr.modules[row_index][col_index]
            text_color = (255, 255, 255) if is_black else (0, 0, 0)

            x = border_pixels + col_index * box_size
            y = border_pixels + row_index * box_size

            text = str(cell_number)

            try:
                bbox = draw.textbbox((x, y), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw.textsize(text, font=font)

            text_x = x + (box_size - text_width) / 2
            text_y = y + (box_size - text_height) / 2

            draw.text((text_x, text_y), text, font=font, fill=text_color)

            cell_number += 1

    # --- 5. Save the final image ---
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    output_path = os.path.join(script_dir, filename)

    img.save(output_path)
    print(f"Successfully created QR code image: {output_path}")


if __name__ == "__main__":
    # my_link = "https://en.wikipedia.org/wiki/QR_code"
    # my_link = "https://google.com"
    my_link = "https://tinyurl.com/vermaa"
    create_numbered_qr_image(my_link)
