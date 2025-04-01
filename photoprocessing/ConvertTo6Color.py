from PIL import Image
from utils.logging_setup import setup_logger

logger = setup_logger(__name__)

def apply_act_palette(image_path, act_path, WIDTH=800, HEIGHT=480, output_path="output.bmp", ratio_mode="crop", rotate=True):
    """Converts a given photo at image_path to given act color pallet and saves to output_path."""
    
    logger.info(f"Processing image: {image_path} with ACT palette: {act_path}")

    try:
        img = Image.open(image_path).convert("RGB")
        logger.debug(f"Image opened successfully: {img.size}")

        aspect = float(img.width) / float(img.height)
        rotated_aspect = 1.0 / aspect

        if rotate and abs(rotated_aspect - (WIDTH / HEIGHT)) < abs(aspect - (WIDTH / HEIGHT)):
            img = img.rotate(90, expand=True)
            logger.debug("Rotated image to better fit aspect ratio")

        if ratio_mode not in ["maintain", "stretch", "crop"]:
            raise ValueError(f"Invalid ratio mode: {ratio_mode}")

        # Resize logic
        if ratio_mode == "maintain":
            img.thumbnail((WIDTH, HEIGHT), Image.LANCZOS)
            new_img = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
            paste_x = (WIDTH - img.width) // 2
            paste_y = (HEIGHT - img.height) // 2
            new_img.paste(img, (paste_x, paste_y))
            img = new_img
            logger.debug("Maintained aspect ratio with padding")
        
        elif ratio_mode == "stretch":
            img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
            logger.debug("Stretched image to fit dimensions")
        
        elif ratio_mode == "crop":
            img_aspect = img.width / img.height
            display_aspect = WIDTH / HEIGHT

            if img_aspect > display_aspect:
                new_width = int(img.height * display_aspect)
                img = img.crop(((img.width - new_width) // 2, 0, (img.width + new_width) // 2, img.height))
            else:
                new_height = int(img.width / display_aspect)
                img = img.crop((0, (img.height - new_height) // 2, img.width, (img.height + new_height) // 2))

            img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
            logger.debug("Cropped image to match aspect ratio")

        # Load ACT color palette
        with open(act_path, "rb") as f:
            act_data = f.read()

        if len(act_data) < 768:
            raise ValueError("Invalid .act file: must contain at least 768 bytes (256 RGB triplets).")

        palette = [tuple(act_data[i:i+3]) for i in range(0, 768, 3)]
        palette_img = Image.new("P", (1, 1))
        palette_img.putpalette([value for rgb in palette for value in rgb])
        
        # Apply palette
        img = img.quantize(palette=palette_img, dither=Image.FLOYDSTEINBERG)
        logger.debug("Applied ACT color palette")

        # Save final image
        img.save(output_path, "BMP")
        logger.info(f"Saved processed image to {output_path}")

    except Exception as e:
        logger.error(f"Error processing image: {e}", exc_info=True)
