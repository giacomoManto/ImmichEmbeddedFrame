from PIL import Image
from utils.logging_setup import setup_logger
from pillow_heif import register_heif_opener



class ImageProcessor:
    def __init__(self, act_path, width, height, rotate, ratio_mode="maintain"):
        self.logger = setup_logger(__name__)
        self.width = width
        self.height = height
        self.rotate = rotate
        self.ratio_mode = ratio_mode
        register_heif_opener()
        
        # Load ACT color palette
        with open(act_path, "rb") as f:
            act_data = f.read()
            if len(act_data) < 768:
                raise ValueError("Invalid .act file: must contain at least 768 bytes (256 RGB triplets).")
            self.palette = [tuple(act_data[i:i+3]) for i in range(0, 768, 3)]
        

    def apply_act_palette(self, image_path, output_path):
        """Converts a given photo at image_path to given act color pallet and saves to output_path."""
        
        self.logger.info(f"Processing image: {image_path}")

        try:
            img = Image.open(image_path).convert("RGB")
            self.logger.debug(f"Image opened successfully: {img.size}")

            aspect = float(img.width) / float(img.height)
            rotated_aspect = 1.0 / aspect

            if self.rotate and abs(rotated_aspect - (self.width / self.height)) < abs(aspect - (self.width / self.height)):
                img = img.rotate(90, expand=True)
                self.logger.debug("Rotated image to better fit aspect ratio")

            if self.ratio_mode not in ["maintain", "stretch", "crop"]:
                raise ValueError(f"Invalid ratio mode: {self.ratio_mode}")

            # Resize logic
            if self.ratio_mode == "maintain":
                img.thumbnail((self.width, self.height), Image.LANCZOS)
                new_img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
                paste_x = (self.width - img.width) // 2
                paste_y = (self.height - img.height) // 2
                new_img.paste(img, (paste_x, paste_y))
                img = new_img
                self.logger.debug("Maintained aspect ratio with padding")
            
            elif self.ratio_mode == "stretch":
                img = img.resize((self.width, self.height), Image.LANCZOS)
                self.logger.debug("Stretched image to fit dimensions")
            
            elif self.ratio_mode == "crop":
                img_aspect = img.width / img.height
                display_aspect = self.width / self.height

                if img_aspect > display_aspect:
                    new_width = int(img.height * display_aspect)
                    img = img.crop(((img.width - new_width) // 2, 0, (img.width + new_width) // 2, img.height))
                else:
                    new_height = int(img.width / display_aspect)
                    img = img.crop((0, (img.height - new_height) // 2, img.width, (img.height + new_height) // 2))

                img = img.resize((self.width, self.height), Image.LANCZOS)
                self.logger.debug("Cropped image to match aspect ratio")

            palette_img = Image.new("P", (1, 1))
            palette_img.putpalette([value for rgb in self.palette for value in rgb])
            
            # Apply palette
            img = img.quantize(palette=palette_img, dither=Image.FLOYDSTEINBERG)
            self.logger.debug("Applied ACT color palette")

            # Save final image
            img.save(output_path, "BMP")
            self.logger.info(f"Saved processed image to {output_path}")

        except Exception as e:
            self.logger.error(f"Error processing image: {e}", exc_info=True)
