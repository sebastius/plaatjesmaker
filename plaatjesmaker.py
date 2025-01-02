# 296x152 hw type 4
# 212x104 hw type 3
# 152x152 hw type 0
# hw type 102 groot paneel

hardware = [
    {"hwType": 0, "h":152,"v":152},
    {"hwType": 3, "h":212,"v":104},
    {"hwType": 4, "h":296,"v":152},   
]

import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

def get_hw_type_info(hwType):
    for entry in hardware:
        if entry["hwType"] == hwType:
            return entry
    return None  # Return None if hwType not found

apip = "192.168.1.162" 

url = "http://{}/get_db".format(apip)

print(url)
tagsdb = []
try:
    # Fetch the JSON data
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues
    # Parse the JSON data
    data = response.json()

    # Extract 'tags' entries
    tags = data.get('tags', [])

    # Extract 'mac' and 'hwType' fields

    for entry in tags:
        mac = entry.get('mac')
        hw_type = entry.get('hwType')
        if mac is not None and hw_type is not None:
            tagsdb.append({'mac': mac, 'hwType': hw_type})

    # Output the extracted data
    print("Extracted Data:", tagsdb)

except requests.exceptions.RequestException as e:
    print("Error fetching data:", e)
except ValueError as e:
    print("Error parsing JSON:", e)


 # destination mac address
dither = 0   # set dither to 1 is you're sending photos etc

for index, entry in enumerate(tagsdb):

    mac = entry['mac']
    hwinfo = get_hw_type_info(entry['hwType'])
    if hwinfo is None:
        print('hwtype not on list,skipping')
        continue

    h=hwinfo['h']
    v=hwinfo['v']
    print(f"{mac}, {h}x{v}")
    #h = hardware[]

    # Create a new paletted image with indexed colors
    image = Image.new('P', (h, v))

    # Define the color palette (white, black, red)
    palette = [
        255, 255, 255,  # white
        0, 0, 0,        # black
        255, 0, 0       # red
    ]

    # Assign the color palette to the image
    image.putpalette(palette)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    text = f"Position in adress list: {index}, Mac: {mac}, h{h}, v{v}"
    #text = "Dit is mac adress {}".format(mac)

    font = ImageFont.truetype("officecodepro-regular.otf", size=16)  # Use a TrueType font
    padding = 2

    # Define the box dimensions
    box = (0, 0, h, v)  # (left, top, right, bottom)
    box_width = box[2] - box[0] - 2 * padding  # Account for padding
    char_width = draw.textlength("A", font=font) # Approximate width of one character

    max_chars = int(box_width // char_width)
   
    # Wrap the text
    wrapped_text = textwrap.fill(text, width=max_chars)

    # Draw the wrapped text inside the box
    draw.text((box[0] + padding, box[1] + padding), wrapped_text, fill=1, font=font)

    # Convert the image to 24-bit RGB
    rgb_image = image.convert('RGB')

    # Save the image as JPEG with maximum quality
    image_path = 'output.jpg'
    rgb_image.save(image_path, 'JPEG', quality="maximum")
    if (mac == "0000033505843E10"):
        image_path="weerwolf.jpg"
    if (mac == "0000032CA01A3E10"):
        image_path="inversewolf.jpg"
    # Prepare the HTTP POST request
    url = "http://" + apip + "/imgupload"
    payload = {"dither": dither, "mac": mac}  # Additional POST parameter
    files = {"file": open(image_path, "rb")}  # File to be uploaded

    # Send the HTTP POST request
    try:
        response = requests.post(url, data=payload, files=files)

        # Check the response status
        if response.status_code == 200:
            print(f"{mac} Image uploaded successfully! {image_path}")
        else:
            print(f"{mac} Failed to upload the image.")
    except:
        print(f"{mac} Failed to upload the image.")
        continue