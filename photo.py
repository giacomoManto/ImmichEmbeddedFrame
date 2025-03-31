from immich import Immich
import os
from dotenv import load_dotenv
import epd7in3e
from PIL import Image

if not os.path.exists("assets/original/"):
    os.makedirs("assets/original/")
    
if not os.path.exists("assets/processed/"):   
    os.makedirs("assets/processed/")

EPD_WIDTH = epd7in3e.EPD_WIDTH
EPD_HEIGHT = epd7in3e.EPD_HEIGHT

def apply_act_palette(image_path, act_path, output_path="output.bmp", ratio_mode="crop"):
    """
    Applies an .act color palette to an image, resizes it to 800x480, 
    and saves it as a bitmap.

    :param image_path: Path to the input image.
    :param act_path: Path to the .act color palette file.
    :param output_path: Path to save the output bitmap.
    """
    
    # Step 1: Open the image and resize to 800x480
    img = Image.open(image_path).convert("RGB")

    VALID_RATIO_MODES = ["maintain", "stretch", "crop"]
    if ratio_mode not in VALID_RATIO_MODES:
        raise ValueError(f"Invalid ratio mode. Choose from {VALID_RATIO_MODES}")

    if ratio_mode == "maintain":
        # add white bars to maintain aspect ratio

        img.thumbnail((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)

        # Create a new white image
        new_img = Image.new("RGB", (EPD_WIDTH, EPD_HEIGHT), (255, 255, 255))
        # Calculate position to paste the thumbnail
        paste_x = (EPD_WIDTH - img.width) // 2
        paste_y = (EPD_HEIGHT - img.height) // 2
        # Paste the thumbnail onto the white image
        new_img.paste(img, (paste_x, paste_y))

        img = new_img
    elif ratio_mode == "stretch":
        # stretch to fit
        img = img.resize((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)

    elif ratio_mode == "crop":
        # crop to fit

        # Calculate the aspect ratio of the image and the display
        img_aspect = img.width / img.height
        display_aspect = EPD_WIDTH / EPD_HEIGHT
        # Determine the new size
        if img_aspect > display_aspect:
            # Image is wider than display, crop width
            new_width = int(img.height * display_aspect)
            img = img.crop(((img.width - new_width) // 2, 0, (img.width + new_width) // 2, img.height))
        else:
            # Image is taller than display, crop height
            new_height = int(img.width / display_aspect)
            img = img.crop((0, (img.height - new_height) // 2, img.width, (img.height + new_height) // 2))
        # Resize to fit the display
        img = img.resize((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)



    # Step 2: Load the .act color table (256 colors, RGB format)
    with open(act_path, "rb") as f:
        act_data = f.read()

    if len(act_data) < 768:
        raise ValueError("Invalid .act file: must contain at least 768 bytes (256 RGB triplets).")

    # Convert ACT file to a list of (R, G, B) tuples
    palette = [act_data[i:i+3] for i in range(0, 768, 3)]
    palette = [tuple(color) for color in palette]

    # Step 3: Convert to a palette-based image
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette([value for rgb in palette for value in rgb])

    # Convert image to use this palette
    img = img.quantize(palette=palette_img, dither=Image.FLOYDSTEINBERG)

    # Step 4: Save as a .bmp file
    img.save(output_path, "BMP")

    print(f"Image saved as {output_path}")


load_dotenv()
# Retrieve API key from .env
x_api_key = os.getenv("X_API_KEY")

if not x_api_key:
    raise ValueError("X_API_KEY not found in .env file")

url = "http://mantovanellinet:2283"

server = Immich(x_api_key, url)

album = server.getAlbumInfoByName("Photo Frame")
for photo in album["assets"]:
    if photo not in os.listdir("assets/original"):
        with open("assets/original/" + os.path.basename(photo["originalPath"]), "wb+") as f:
            f.write(server.downloadAsset(photo["id"]))
        
for photo in os.listdir("assets/original/"):
    if photo not in os.listdir():
        apply_act_palette(os.path.join("assets/original/", photo), "6-color.act", os.path.join("assets/processed/", photo.split(".")[0] + ".bmp"))
        print(f"Processed {photo}")
    else:
        print(f"Already processed {photo}")
        
        
epd = epd7in3e.EPD()
epd.init()
epd.Clear()
print("1.read bmp file")

bmp_image = Image.open("/assets/processed/2A17C0D9-DA24-4D74-8EF2-F7DF3260B709.bmp")

print("2.display image")
epd.display(epd.getbuffer(bmp_image))