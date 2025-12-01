# main.py
import tkinter as tk
from data import load_phim
from booking import open_booking_window
from PIL import Image, ImageTk


def home_ui():
    root = tk.Tk()
    root.title("Hệ thống đặt vé")
    root.geometry("700x600")

    tk.Label(root, text="CHỌN PHIM", font=("Arial", 22, "bold")).pack(pady=15)

    movies = load_phim()

    frame = tk.Frame(root)
    frame.pack()

    for m in movies:
        item = tk.Frame(frame, bd=2, relief="ridge", padx=10, pady=10)
        item.pack(pady=10, fill="x")

        # Text
        info = tk.Frame(item)
        info.pack(side="left", padx=15)

        tk.Label(info, text=m["ten"], font=("Arial", 16, "bold")).pack(anchor="w")
        tk.Label(info, text=f"Thời lượng: {m['thoiluong']} phút").pack(anchor="w")
        tk.Label(info, text=f"Suất: {m['suat']}").pack(anchor="w")
        tk.Label(info, text=f"Giá: {m['gia']} VND").pack(anchor="w")

        tk.Button(item, text="Đặt vé", font=("Arial", 12),
                  command=lambda movie=m: open_booking_window(movie)).pack(side="right")

    root.mainloop()


if __name__ == "__main__":
    home_ui()
