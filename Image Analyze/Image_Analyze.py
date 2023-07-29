from pydoc import describe
from tkinter import RIGHT
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
from PIL import Image,ImageTk,ImageDraw,ImageFont
import sys
import time
import tkinter as tk
from tkinter import filedialog



subscription_key = '8824649b4ed24a4cbbe3c2b1d2e01136'
endpoint = "https://computer-vision-00001.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
#folder='F:/Azure/vs stdio python/Congitive Services Demo/Images/Abdul'
#out_folder='F:/Azure/vs stdio python/Congitive Services Demo/Images/Output'
#files=os.listdir(folder)
font_size=20
font = ImageFont.truetype("arial.ttf", font_size)



def windowGUI():
    def open_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = Image.open(file_path)
            desired_width = 300
            desired_height = 200
            image = image.resize((desired_width, desired_height), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(image)
            image_label.config(image=tk_image)
            image_label.image = tk_image  # To prevent garbage collection
            
            #results=computervision_client.detect_objects_in_stream(image)
            with open(file_path,mode='rb') as image_stream:
                results_des=computervision_client.describe_image_in_stream(image_stream)
            text_image=""
            
            for caption in results_des.captions:
                text_image=text_image+" "+caption.text+" with confidence "+str(caption.confidence*100)[:4]

            description_label.config(text="Image Description:\n" + text_image+"\n")
            with open(file_path,mode='rb') as image_stream:
                results_obj=computervision_client.detect_objects_in_stream(image_stream)
            obj_text=""
            for object in results_obj.objects:
                obj_text=obj_text+f'{ object.object_property } ({ object.confidence*100 }%)\n'
            object_label.config(text="Object Detected:\n" + obj_text)
                  
    def exit():
        root.destroy()       

    # Create the main window
    root = tk.Tk()
    root.title("Image Analysis")
    root.geometry("1200x800")
    root.configure(bg="lightblue")
    root.option_add("*Button.background", "red")
    root.option_add("*Button.foreground", "black")
    root.option_add("*Button.font", "Helvetica 12 bold")
    root.option_add("*Label.background", "lightblue")
    root.option_add("*Label.foreground", "black")
    root.option_add("*Label.font", "Helvetica 14")
    
    
    image_label = tk.Label(root)
    image_label.pack()

    desc = tk.Label(root, text="Let's Describe Image and detect objects\n")
    desc.pack()

    # Create the button to open the image
    select_button = tk.Button(root, text="Select Image", command=open_image)
    select_button.pack(pady=10)

    # Create the label to display the image
    image_label = tk.Label(root)
    image_label.pack()
    description_label = tk.Label(root, text="Image Description:\n")
    description_label.pack()
    object_label = tk.Label(root, text="Object Detected:\n")
    object_label.pack()
    exit_button = tk.Button(root, text="Exit", command=exit)
    exit_button.pack(pady=10)
    # Start the main event loop
    root.mainloop()


windowGUI()