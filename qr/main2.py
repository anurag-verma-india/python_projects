# First, install the required library:
# pip install qrcode

import qrcode
import io

def generate_numbered_qr(data):
    """
    Generates a QR code for the given data and returns a string
    representation with numbered modules for hand-drawing.
    """
    # Configure QR code
    qr = qrcode.QRCode(
        version=2,  # Version 2 QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1, # Not relevant for text output, but required
        border=4,   # The quiet zone around the QR code
    )
    
    # Add data and generate the QR code matrix
    qr.add_data(data)
    qr.make(fit=False)  # Do not automatically find the best fit

    modules = qr.modules
    output = io.StringIO()
    counter = 1
    
    # Calculate the maximum number of digits for alignment
    num_black_modules = sum(row.count(True) for row in modules)
    max_digits = len(str(num_black_modules))

    # Create the numbered string representation
    for r, row in enumerate(modules):
        line = ""
        for c, module in enumerate(row):
            if module:
                # Black module: print the current number
                line += str(counter).ljust(max_digits + 1)
                counter += 1
            else:
                # White module: print dots for spacing
                line += ("." * max_digits) + " "
        output.write(line + "\n")
        
    return output.getvalue(), len(modules)

if __name__ == "__main__":
    # The link to encode
    # link_to_encode = "https://github.com/google/gemini-cli"
    link_to_encode = "http://github.com/"
    
    # Generate the numbered QR code string
    numbered_qr_string, grid_size = generate_numbered_qr(link_to_encode)
    
    # Print the result
    print(f"Numbered QR code for: {link_to_encode}")
    print("=" * 30)
    print("Instructions:")
    print("1. Get a piece of graph paper.")
    print(f"2. The grid size is {grid_size}x{grid_size}.")
    print("3. Fill in the squares that correspond to a number.")
    print("4. Leave the squares with '.' empty (white).")
    print("=" * 30)
    print(numbered_qr_string)


# TODO