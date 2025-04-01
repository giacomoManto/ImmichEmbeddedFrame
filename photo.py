from immich import Immich
import os
from dotenv import load_dotenv
import display.drivers.epd7in3e as epd7in3e
from PIL import Image
import time
from pillow_heif import register_heif_opener
from photoprocessing.ConvertTo6Color import apply_act_palette

register_heif_opener()

if not os.path.exists("assets/original/"):
    os.makedirs("assets/original/")
    
if not os.path.exists("assets/processed/"):   
    os.makedirs("assets/processed/")

EPD_WIDTH = epd7in3e.EPD_WIDTH
EPD_HEIGHT = epd7in3e.EPD_HEIGHT
EPD_ASPECT = float(EPD_WIDTH) / float(EPD_HEIGHT)


load_dotenv()
# Retrieve API key from .env
x_api_key = os.getenv("X_API_KEY")

if not x_api_key:
    raise ValueError("X_API_KEY not found in .env file")

url = ""

server = Immich(x_api_key, url)

album = server.getAlbumInfoByName("Photo Frame")

photoList = []

for photo in album["assets"]:
    photoList.append(os.path.basename(photo["originalPath"]).split(".")[0])
    if os.path.basename(photo["originalPath"]) not in os.listdir("assets/original"):
        print(f"Downloading {photo['originalPath']}")
        with open("assets/original/" + os.path.basename(photo["originalPath"]), "wb+") as f:
            f.write(server.downloadAsset(photo["id"]))
    else:
        print("Already downloaded " + os.path.basename(photo["originalPath"]))
        
for photo in os.listdir("assets/original/"):
    if photo.split(".")[0] + ".bmp" not in os.listdir("assets/processed/"):
        apply_act_palette(os.path.join("assets/original/", photo), "6-color.act", os.path.join("assets/processed/", photo.split(".")[0] + ".bmp"))
        print(f"Processed {photo}")
    else:
        print(f"Already processed {photo}")
        
for photo in os.listdir("assets/original"):
    name = photo.split(".")[0]
    if name not in photoList:
        print(f"Removing {name}")
        os.remove(os.path.join("assets/original/", photo))
        os.remove(os.path.join("assets/processed/", name + ".bmp"))

        
epd = epd7in3e.EPD()
epd.init()
epd.Clear()
print("1.read bmp file")

for image in os.listdir("assets/processed/"):
    print(f"Displaying {image}")
    epd.display(epd.getbuffer(Image.open(os.path.join("assets/processed/", image))))
    time.sleep(10)
    
epd.sleep()