# First, install the required libraries:
# pip install "qrcode[pil]"

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime


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


def create_coordinated_qr_image(
    data, filename="coordinated_qr_code.png", savetolocation="", coordinates=True
):
    """
    Generates a version 2 QR code with cell coordinates (e.g., "1,1")
    and saves it as a PNG image.
    """
    # --- 1. Generate the QR code structure ---
    qr = qrcode.QRCode(
        # version=2,
        # version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=35,  # The size of each cell in pixels
        border=4,  # The width of the border (quiet zone) in cells
    )
    qr.add_data(data)
    qr.make(fit=False)

    # --- 2. Create a base image from the QR code ---
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    draw = ImageDraw.Draw(img)

    if coordinates:
        # --- 3. Set up for drawing coordinates ---
        qr_dimension = len(qr.modules)
        box_size = qr.box_size
        border_pixels = qr.border * box_size

        # Adjust font size to fit coordinate strings (e.g., "25,25")
        font_size = int(box_size / 3.5)
        font = get_font(font_size)

        # --- 4. Iterate over each cell to draw the coordinates ---
        for row_index in range(qr_dimension):
            for col_index in range(qr_dimension):
                is_black = qr.modules[row_index][col_index]
                text_color = (255, 255, 255) if is_black else (0, 0, 0)

                x = border_pixels + col_index * box_size
                y = border_pixels + row_index * box_size

                # Use cell coordinates (e.g., "1,1", "1,2") as text
                text = f"{row_index + 1},{col_index + 1}"

                try:
                    # Modern Pillow versions use textbbox for better size calculation
                    bbox = draw.textbbox((x, y), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    # Fallback for older Pillow versions
                    text_width, text_height = draw.textsize(text, font=font)

                text_x = x + (box_size - text_width) / 2
                text_y = y + (box_size - text_height) / 2

                draw.text((text_x, text_y), text, font=font, fill=text_color)

    if savetolocation == "":
        # --- 5. Save the final image ---
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # Fallback for interactive environments
            script_dir = os.getcwd()

        output_path = os.path.join(script_dir, filename)

        img.save(output_path)
        print(f"Successfully created QR code image: {output_path}")
    else:
        img.save(savetolocation)


if __name__ == "__main__":
    # my_link = "https://tinyurl.com/vermaa"
    my_link = "https://instagram.com/anurag_verma_india"


    # Get the current date and time
    current_datetime = datetime.now()

    # Extract only the time component
    current_time = current_datetime.strftime("%Hh%Mm%Ss")

    create_coordinated_qr_image(
        my_link,
        savetolocation=f"qr-{current_time}.png",
        # coordinates=False,
        coordinates=True
    )
    
