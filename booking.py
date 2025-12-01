# booking_ui.py
import tkinter as tk
from tkinter import messagebox
from data import ghe_da_dat, luu_ve


def open_booking_window(movie):
    win = tk.Toplevel()
    win.title(f"Đặt vé - {movie['ten']}")
    win.geometry("550x550")

    tk.Label(win, text=f"Phim: {movie['ten']}", font=("Arial", 16, "bold")).pack(pady=5)
    tk.Label(win, text=f"Suất chiếu: {movie['suat']}", font=("Arial", 12)).pack()

    # FRAME CHỨA GHẾ
    frame_seat = tk.Frame(win)
    frame_seat.pack(pady=15)

    ghe_selected = []
    ghe_blocked = ghe_da_dat(movie["id"], movie["suat"])

    ROWS = ["A", "B", "C", "D", "E"]
    COLS = 8
    buttons = {}

    def click_seat(seat):
        if seat in ghe_blocked:
            return

        if seat in ghe_selected:
            ghe_selected.remove(seat)
            buttons[seat].config(bg="white")
        else:
            ghe_selected.append(seat)
            buttons[seat].config(bg="green")

        total_price.set(len(ghe_selected) * int(movie["gia"]))

    # VẼ GHẾ
    for r in ROWS:
        for c in range(1, COLS + 1):
            seat = f"{r}{c}"
            color = "red" if seat in ghe_blocked else "white"

            btn = tk.Button(frame_seat, text=seat, width=4, bg=color,
                            command=lambda s=seat: click_seat(s))
            btn.grid(row=ROWS.index(r), column=c, padx=5, pady=5)
            buttons[seat] = btn

    # TỔNG TIỀN
    total_price = tk.IntVar(value=0)
    tk.Label(win, text="Tổng tiền:", font=("Arial", 14)).pack()
    tk.Label(win, textvariable=total_price, font=("Arial", 18), fg="blue").pack()

    # THANH TOÁN
    def thanh_toan():
        if not ghe_selected:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn ghế!")
            return

        for g in ghe_selected:
            luu_ve(movie["id"], movie["ten"], movie["suat"], g, movie["gia"])

        messagebox.showinfo("Thành công", "Đặt vé thành công!")

        win.destroy()  # quay về trang chọn phim

    tk.Button(win, text="Thanh toán", font=("Arial", 14), bg="orange",
              command=thanh_toan).pack(pady=15)

    win.mainloop()
