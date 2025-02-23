import matplotlib.pyplot as plt

# import matplotlib
# from pathlib import Path
import sys


def latex_to_svg(latex_string, filename="equation.svg"):
    """
    Convert a LaTeX string to an SVG file with transparent background

    Args:
        latex_string (str): The LaTeX equation string
        filename (str): Name of the output SVG file (default: equation.svg)
    """
    # Set up the figure with transparent background
    fig = plt.figure(figsize=(10, 1))
    fig.patch.set_alpha(0.0)

    # Remove axes
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    # Render the LaTeX equation
    text = ax.text(
        0.5,
        0.5,
        f"${latex_string}$",
        horizontalalignment="center",
        verticalalignment="center",
        color="black",
        fontsize=24,
    )

    # Adjust the figure size to fit the equation
    renderer = fig.canvas.get_renderer()
    bbox = text.get_window_extent(renderer=renderer)
    bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())

    # Save as SVG with tight layout and transparent background
    plt.savefig(
        filename,
        bbox_inches=bbox_inches,
        transparent=True,
        format="svg",
        dpi=300,
        pad_inches=0.1,
    )

    plt.close()


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         # Get equation from command line argument
#         equation = sys.argv[1]
#         output_file = sys.argv[2] if len(sys.argv) > 2 else "equation.svg"
#         latex_to_svg(equation, output_file)
#     else:
#         # Example usage
#         # equation = r"E = mc^2"
#         equation = r"(ab)^+"
#         latex_to_svg(equation)

if __name__ == "__main__":
    # print("\nLaTeX to SVG Converter")
    # print("=====================")
    # print("\nExample usage:")
    # print("1. From command line:")
    # print('   python script.py "x^2 + y^2 = r^2" "circle_equation.svg"')
    # print("\n2. From within Python:")
    # print("   from script import latex_to_svg")
    # print('   latex_to_svg(r"E = mc^2", "energy_equation.svg")')
    # print("\nExample LaTeX equations:")
    # print("- Simple fraction: \\frac{1}{2}")
    # print("- Square root: \\sqrt{x^2 + y^2}")
    # print("- Integral: \\int_0^\\infty e^{-x^2} dx")
    # print("- Matrix: \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}\n")

    if len(sys.argv) > 1:
        # Get equation from command line argument
        equation = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "equation.svg"
        latex_to_svg(equation, output_file)
    else:
        # Example usage
        # equation = r"E = mc^2"
        equation = r"([A−Z]∪[a−z])⋅([A−Z]∪[a−z]∪[0-9])"
        # equation = r"a\n\begin{pmatrix} a & b \\ c & d \end{pmatrix}\n"
        latex_to_svg(equation)
        print(
            f"No equation provided as argument. Created example equation '{equation}' as 'equation.svg'"
        )
