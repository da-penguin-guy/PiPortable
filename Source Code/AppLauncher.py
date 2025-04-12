import os
import subprocess
import Helper as help
import customtkinter as ctk


#Setting CD because python is stupid
os.chdir(os.path.abspath(os.path.dirname(__file__)))

#Importing Yaml
yamlData = help.ImportYaml("AppConfig.yaml")
#Setting apperance
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
# Boilerplate
window = ctk.CTk()
window.geometry("1280x720")
window.title("Sound Slice")
#Create title label
title = ctk.CTkLabel(
    master=window, 
    text="Sound Slice Applications",
    font=tuple(yamlData["TitleFont"])
)
title.pack(pady=20)
#Creating a grid to hold all the buttons
selectScreen = ctk.CTkFrame(window,corner_radius=20)
selectScreen.pack(pady=20, padx=20, fill="both", expand=True)
numX = 3
x=0
y=0
for app in yamlData["Apps"]:
    print(app)
    # Load icons used
    appIcon = help.ConvertIcon(app["Icon"])
    #Create button!
    appButton = ctk.CTkButton(
        master=selectScreen,
        text=app["Name"],
        font=tuple(yamlData["LabelFont"]),
        image=appIcon,
        compound="left",
        corner_radius=20,
        #Creating an inline function to run an async terminal function to run a python script
        command= lambda: subprocess.Popen([app["Type"], app["Location"]])
    )
    appButton.grid(row = y, column = x, padx = 10, pady = 10)
    x += 1
    if x >= numX:
        x = 0
        y += 1

#Run the thing
window.mainloop()