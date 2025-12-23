import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def load_image_from_url(url, size=(150, 220)):
    if not url or url.strip() == "":
        return create_placeholder(size)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        return create_placeholder(size)

def create_placeholder(size):
    img = Image.new('RGB', size, color='gray')
    return ImageTk.PhotoImage(img)