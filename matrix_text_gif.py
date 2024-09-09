import random
import string
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

# Settings for the animation
width, height = 600, 400  # Size of the output image
font_size = 30  # Font size of the matrix characters
columns = width // font_size  # Number of text columns
rows = height // font_size  # Number of text rows
frames = 200  # Increased number of frames for a longer animation

highlighted_words = ["DATA", "ABINITIO", "POWER BI", "VR", "AR", "AI", "SQL", "BLENDER", "UNITY", "PYTHON"]
highlighted_font_size = int(font_size * 2)  # bigger than the normal font


# Create a font object
try:
    font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", font_size)
except IOError:
    # Fallback font if DejaVuSansMono is not available
    font = ImageFont.load_default()

# Function to generate random characters
def get_random_char():
    return random.choice(string.ascii_lowercase + string.digits)

# Initialize the text drops (random vertical positions for each column)
text_drops = [random.randint(-rows, 0) for _ in range(columns)]

# Generate frames for the animation
images = []
for frame in range(frames):
    # Create a new blank image
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)

    # Draw falling characters
    for i in range(columns):
        x = i * font_size
        # Decide whether to highlight this column
        is_highlighted = random.random() < 0.05  # 2% chance of highlighting

        for j in range(rows):
            y = (text_drops[i] + j) % rows * font_size

            if is_highlighted and j == rows - 1:
                word = random.choice(highlighted_words).upper()  # Highlighted word in uppercase
                # Center the word in the column
                word_x = x - ((len(word) - 1) * highlighted_font_size) // 2
                
                # Draw the highlighted background before the word
                # Get the bounding box of the text to calculate the size of the background rectangle
                bbox = draw.textbbox((word_x, y), word, font=font)

                # Unpack the bounding box coordinates
                rect_x1, rect_y1, rect_x2, rect_y2 = bbox

                # Add padding to the background rectangle (e.g., 2 pixels)
                padding = 2
                rect_x1 -= padding
                rect_y1 -= padding
                rect_x2 += padding
                rect_y2 += padding
                
                # Draw the rectangle (background) with a highlight color (e.g., blue or white)
                draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill="blue")  

                draw.text((word_x, y), word, font=font, fill="white")
            else:
                char = get_random_char()
                color = (0, 0, random.randint(100, 255))  # Shades of blue
                draw.text((x, y), char, font=font, fill=color)

    # Update the drop position less frequently to slow down the movement
    if frame % 100 == 0:  # Update less often for slower movement
        text_drops = [(drop + 1) % rows for drop in text_drops]

    # Save the frame to the list
    images.append(np.array(img))

# Save frames as a GIF
gif_name = 'matrix_animation_blue_' + str(width) + '_' + str(height) + '.gif'
imageio.mimsave(gif_name, images, fps=3)
