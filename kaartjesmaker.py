from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap

# Step 1: Create a blank canvas
canvas_width, canvas_height = 152, 296
canvas = Image.new('P', (canvas_width, canvas_height), color='white')

palette = [
    255, 255, 255,  # white
    0, 0, 0,        # black
    255, 0, 0       # red
]

canvas.putpalette(palette)

# Step 2: Open the icon
icon_path = "wolf.png"
icon = Image.open(icon_path)

# Step 3: Get the size of the icon
icon_width, icon_height = icon.size

# Step 4: Calculate the position for the bottom-right corner
x_position = canvas_width - icon_width
y_position = canvas_height - icon_height

# Step 5: Paste the icon onto the canvas
canvas.paste(icon, (x_position, y_position), icon)

draw = ImageDraw.Draw(canvas)

text = f"Je bent de weerwolf. Elke nacht mag je met de andere weerwolven besluiten wie jullie opeten. "

font = ImageFont.truetype("officecodepro-regular.otf", size=16)  # Use a TrueType font
padding = 2

# Define the box dimensions
box = (0, 0, 152, 296)  # (left, top, right, bottom)
box_width = box[2] - box[0] - 2 * padding  # Account for padding
char_width = draw.textlength("A", font=font) # Approximate width of one character

max_chars = int(box_width // char_width)

# Wrap the text
wrapped_text = textwrap.fill(text, width=max_chars)

# Draw the wrapped text inside the box
draw.text((box[0] + padding, box[1] + padding), wrapped_text, fill=1, font=font)
rotated_canvas = canvas.transpose(Image.ROTATE_270)

rgb_image = rotated_canvas.convert('RGB')
inverted_image = ImageOps.invert(rgb_image)

# Step 4: repair Cyan -> red for the inverted image
width, height = inverted_image.size
target_color = (0, 255, 255)  # Cyan
replacement_color = (255, 0, 0)  # Red
pixels = inverted_image.load()
for x in range(width):
    for y in range(height):
        if pixels[x, y] == target_color:
            pixels[x, y] = replacement_color


# Save the image as JPEG with maximum quality
image_path = 'weerwolf.jpg'
rgb_image.save(image_path, 'JPEG', quality="maximum")
inverted_image.save('inversewolf.jpg', 'JPEG', quality="maximum")

