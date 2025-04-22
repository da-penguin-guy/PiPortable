from PIL import Image, ImageColor
import customtkinter as ctk
import os
#Yaml Import Process
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def ImportYaml(path : str, scriptDirectory : str = "") -> dict:
    """
    Loads YAML data based on a relative path

    :param path: The relative path of the YAML file
    :param scriptDirectory: An optional directory joined with path to find an absolute path

    :return: YAML Dictornary
    """
    if(scriptDirectory != ""):
        path = os.path.join(scriptDirectory, path)
    with open(path, "r") as file:
        return yaml.safe_load(file)

def ImportImage(path: str) -> Image.Image:
    """
    Load an PNG image based on relative path

    :param image_path: Relative path to the primary image to load

    :return: PIL Image object
    """
    try:
        # Try to open the primary image
        image = Image.open(image_path)
        image.load()  # Ensure the image is fully loaded
        print("Loaded primary image successfully.")
        return image
    except Exception as e:
        print(f"Failed to load primary image: {e}")
        try:
            # Try to open the Error image
            fallback_image = Image.open(yamlData["ErrorIconPath"])
            fallback_image.load()
            print("Loaded error image successfully.")
            return fallback_image
        except Exception as fallback_error:
                print(f"Failed to load error image: {fallback_error}")
                return None

        
def RecolorImage(image: Image.Image, newColor : tuple[int,int,int]) -> Image.Image:
    """
    Recolor a single-color Pillow image with transparency. Uses alpha value to determine which pixels to recolor

    :param image: PIL Image to recolor
    :param newColor: (r,g,b), 0-255 value of the recolored pixels

    :return: PIL Image object
    """
    if(image == None):
        print("Image is empty")
        return image

    # Open the image
    img = image.convert("RGBA")
    
    # Extract channels
    data = img.getdata()
    new_data = []
    
    for item in data:
        # Preserve transparency (alpha channel)
        if item[3] > 0:  # Non-transparent pixels
            new_data.append((*newColor, item[3]))
        else:
            new_data.append(item)  # Keep fully transparent pixels unchanged

    # Apply the new data
    img.putdata(new_data)
    return img

def ConvertIcon(path: str, imageSize:tuple[int,int] = (100,100), lightColor:tuple[int,int,int] = (0,0,0), darkColor:tuple[int,int,int] = (255,255,255)) -> ctk.CTkImage:
    """
    Imports a CTK image. Automatically recolors image to fit light and dark mode

    :param path: Path of the image file. PNG is the only image type tested
    :param imageSize: The size of the image displayed. The format is (Width, Height).The default is (100,100)
    :param lightColor: The color the light mode icon should be recolored to. The format is (r,g,b), 0-255. Default is (0,0,0) aka black
    :param darkColor: The color the dark mode icon should be recolored to. The format is (r,g,b), 0-255. Default is (255,255,255) aka white

    :return: A CTK Image with a recolored dark and light image
    """
    image = ImportImage(path)
    return ctk.CTkImage(
        light_image=RecolorImage(image,lightColor), 
        dark_image=RecolorImage(image,darkColor), 
        size=imageSize)

def HexToRGB(hex : str) -> tuple[int,int,int]:
    """
    Converts a hex string into a tuple color. \n
    This is literally just a wrapper for ImageColor.getrgb() with a try \n
    Just read the docs for that
    """
    try:
        return ImageColor.getrgb(hex)
    except ValueError:
        print(f"String {hex} is invalid")
        return (0,0,0)