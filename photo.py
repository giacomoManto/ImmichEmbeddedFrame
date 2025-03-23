from immich import Immich
import os
from dotenv import load_dotenv

load_dotenv()
# Retrieve API key from .env
x_api_key = os.getenv("X_API_KEY")

if not x_api_key:
    raise ValueError("X_API_KEY not found in .env file")

url = "http://mantovanellinet:2283"

server = Immich(x_api_key, url)

album = server.getAlbumInfoByName("Photo Frame")
for photo in album["assets"]:
    with open(os.path.basename(photo["originalPath"]), "wb") as f:
        f.write(server.downloadAsset(photo["id"]))