from PIL import Image, ImageColor
import customtkinter as ctk
#Yaml Import Process
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def ImportYaml(path : str):
    return yaml.load(open(path, 'r'),Loader)

def ImportImage(path: str) -> Image.Image:
    """
    Get PNG image based on relative path
    """
    
    try:
        # Try opening the image
        return Image.open(path)  # Return a PIL.Image.Image object
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        # Check if the error image exists
        yamlData = ImportYaml("AppConfig.yaml")
        return Image.open(yamlData["ErrorIconPath"])  # Return fallback error image
        
def RecolorImage(image: Image.Image, new_color : tuple[int,int,int]) -> Image.Image:
    """
    Recolor a single-color Pillow image with transparency.
    """
    # Open the image
    img = image.convert("RGBA")
    
    # Extract channels
    data = img.getdata()
    new_data = []
    
    for item in data:
        # Preserve transparency (alpha channel)
        if item[3] > 0:  # Non-transparent pixels
            new_data.append((*new_color, item[3]))
        else:
            new_data.append(item)  # Keep fully transparent pixels unchanged

    # Apply the new data
    img.putdata(new_data)
    return img

def ConvertIcon(path: str, imageSize:tuple[int,int] = (100,100), lightColor:tuple[int,int,int] = (0,0,0), darkColor:tuple[int,int,int] = (255,255,255)) -> ctk.CTkImage:
    image = ImportImage(path)
    return ctk.CTkImage(
        light_image=RecolorImage(image,lightColor), 
        dark_image=RecolorImage(image,darkColor), 
        size=imageSize
        )

def HexToRGB(hex : str) -> tuple[int,int,int]:
    """
    Converts a hex string into a tuple color
    """
    try:
        return ImageColor.getrgb(hex)
    except ValueError:
        print(f"String {hex} is invalid")
        return (0,0,0)