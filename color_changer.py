from fileinput import filename
from PIL import Image
import os

# pip install pillow

output_dir = "output"
input_dir = '.'


target_colors = [
    ("Blonde", (254, 249, 205)),
    ("Dark blonde", (192, 154, 106)),
    ("Medium brown", (124, 63, 0)),
    ("Dark brown", (47, 30, 14)),
    ("Black", (0, 0, 0)),
    ("Auburn", (150, 69, 53)),
    ("Red", (177, 101, 0)),
    ("Gray", (210, 210, 209)),
    ("White", (255, 255, 255))
]


def change_png_color(image_path, new_color, output_path):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        if item[3] > 0:  # If pixel is not transparent
            new_data.append((*new_color, item[3]))  # Preserve alpha channel
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path)


def replace_color(image_path, target_color, new_color, tolerance=30, output_path="output.png"):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    def is_close(c1, c2, tol):
        return all(abs(a - b) <= tol for a, b in zip(c1[:3], c2[:3]))

    new_data = [
        (*new_color, item[3]) if is_close(item,
                                          target_color, tolerance) else item
        for item in data
    ]

    img.putdata(new_data)
    img.save(output_path)


if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)

    print("Starting color replacement...")
    for color_name, target_color in target_colors:
        for file in os.listdir(input_dir):
            if file.lower().endswith('.png'):
                print("Processing file: {} for color {}".format(os.path.join(input_dir, file), color_name))
                change_png_color(os.path.join(input_dir, file), target_color,
                                f"{output_dir}/{file.split('.png')[0]}_{color_name}.png")
    print("Color replacement completed.")
