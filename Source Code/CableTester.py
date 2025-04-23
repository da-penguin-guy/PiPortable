import os
import Helper as help
import customtkinter as ctk
import Io.IoManager as IO
#Set Directory
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
yamlData = help.GetYaml("AppConfig.yaml")
# Boilerplate
window = ctk.CTk()
window.geometry("1280x720")
window.title("Sound Slice Cable Tester")
#Create title label
title = ctk.CTkLabel(
    master=window, 
    text="Cable Tester",
    font=tuple(yamlData["TitleFont"])
)
title.pack(pady=20)
#Creating a grid to hold all the buttons
selectScreen = ctk.CTkFrame(window,corner_radius=20)
selectScreen.pack(pady=20, padx=20, fill="both", expand=True)

print(IO.GetCurrentIO(0))
window.mainloop()