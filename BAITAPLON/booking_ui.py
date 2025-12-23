import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import urllib.parse
import data
import poster_utils 

class BookingPage(tk.Frame):
    def __init__(self, master, user, movie, on_back_home):
        super().__init__(master)
        self.user = user
        self.movie = movie
        self.on_back_home = on_back_home
        
        self.ds_lich_chieu = data.lay_lich_chieu_theo_phim(movie['ID'])
        self.selected_lich = None
        self.selected_seats = []
        self.buttons_ghe = {}

        # --- UI CHÍNH ---
        tk.Button(self, text="< Quay lại", command=on_back_home).pack(anchor="nw", padx=10, pady=5)
        tk.Label(self, text=f"ĐẶT VÉ: {movie['Ten']}", font=("Arial", 16, "bold"), fg="#e74c3c").pack(pady=5)
        
        if not self.ds_lich_chieu:
            tk.Label(self, text="Phim này chưa có lịch chiếu nào!", fg="red", font=("Arial", 12)).pack(pady=50)
            return

        # 1. Chọn Lịch
        tk.Label(self, text="Vui lòng chọn suất chiếu:", font=("Arial", 10, "bold")).pack()
        frame_lich = tk.Frame(self)
        frame_lich.pack(pady=10)
        
        cols = ("Ngày", "Giờ", "Phòng")
        self.tree = ttk.Treeview(frame_lich, columns=cols, show="headings", height=5)
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=100, anchor="center")
        self.tree.pack(side="left")
        
        sb = tk.Scrollbar(frame_lich, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)
        
        for lich in self.ds_lich_chieu:
            self.tree.insert("", "end", values=(lich['Ngay'], lich['Gio'], lich['Phong']), tags=(str(lich),))
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select_schedule)

        # 2. Màn hình & Ghế
        self.frame_man_hinh = tk.Frame(self)
        self.frame_man_hinh.pack(pady=10)
        tk.Label(self.frame_man_hinh, text="--- MÀN HÌNH ---", bg="#ddd", width=40).pack(pady=5)
        
        self.seat_frame = tk.Frame(self.frame_man_hinh)
        self.seat_frame.pack()
        
        # 3. Thanh toán
        self.lbl_total = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.lbl_total.pack(pady=10)
        
        self.btn_pay = tk.Button(self, text="THANH TOÁN", bg="#e67e22", fg="white", 
                                 command=self.open_payment_dialog, state="disabled") 
        self.btn_pay.pack(pady=10)

    def on_select_schedule(self, event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected[0])['values']
        self.selected_lich = {'Ngay': vals[0], 'Gio': vals[1], 'Phong': vals[2]}
        self.selected_seats = []
        self.lbl_total.config(text="Tổng tiền: 0 VND")
        self.btn_pay.config(state="normal")
        self.ve_so_do_ghe()

    def ve_so_do_ghe(self):
        for widget in self.seat_frame.winfo_children(): widget.destroy()
        booked = data.lay_ghe_da_dat(self.movie['ID'], self.selected_lich['Ngay'], self.selected_lich['Gio'], self.selected_lich['Phong'])
        rows = ['A', 'B', 'C', 'D', 'E']; cols = 8
        self.buttons_ghe = {}
        for r_idx, row in enumerate(rows):
            for c in range(1, cols + 1):
                seat_id = f"{row}{c}"
                is_booked = seat_id in booked
                btn = tk.Button(self.seat_frame, text=seat_id, width=4, height=2, bg="red" if is_booked else "white", state="disabled" if is_booked else "normal", command=lambda s=seat_id: self.toggle_seat(s))
                btn.grid(row=r_idx, column=c-1, padx=3, pady=3)
                self.buttons_ghe[seat_id] = btn

    def toggle_seat(self, seat_id):
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            self.buttons_ghe[seat_id].config(bg="white")
        else:
            self.selected_seats.append(seat_id)
            self.buttons_ghe[seat_id].config(bg="#2ecc71")
        total = len(self.selected_seats) * int(self.movie['GiaVe'])
        self.lbl_total.config(text=f"Tổng tiền: {total:,} VND")

    # --- POPUP THANH TOÁN (STK 9999992025) ---
    def open_payment_dialog(self):
        if not self.selected_seats: messagebox.showwarning("Lỗi", "Chưa chọn ghế!"); return
        
        total_money = len(self.selected_seats) * int(self.movie['GiaVe'])
        
        self.top = tk.Toplevel(self)
        self.top.title("Cổng thanh toán")
        self.top.geometry("480x700") 
        self.top.configure(bg="white")
        
        tk.Label(self.top, text="QUÉT MÃ ỦNG HỘ MTTQVN", font=("Arial", 14, "bold"), bg="white", fg="#c0392b").pack(pady=15)
        
        # --- CẤU HÌNH SỐ TÀI KHOẢN MỚI ---
        stk_api = "9999992025"  # Số tài khoản chuẩn bạn vừa cung cấp
        
        # Nội dung chuyển khoản (Mã hóa URL an toàn)
        thoi_gian_ht = datetime.now().strftime("%d%m %H%M")
        noi_dung_raw = f"ID {self.user['ID_Nguoi_Dung']} T {thoi_gian_ht}"
        noi_dung_encoded = urllib.parse.quote(noi_dung_raw)
        
        # Tạo Link QR VietQR (VCB)
        # Link ảnh sẽ tự động chứa STK 9999992025 và Bank ID là Vietcombank
        qr_url = f"https://img.vietqr.io/image/VCB-{stk_api}-compact.png?amount={total_money}&addInfo={noi_dung_encoded}"
        
        try:
            img = poster_utils.load_image_from_url(qr_url, size=(280, 280))
            lbl_qr = tk.Label(self.top, image=img, bg="white", bd=1, relief="solid")
            lbl_qr.image = img 
            lbl_qr.pack(pady=5)
        except:
            tk.Label(self.top, text="[KHÔNG TẢI ĐƯỢC QR]", bg="#ddd", width=30, height=10).pack(pady=5)
            
        # Thông tin chi tiết bên dưới
        info_frame = tk.Frame(self.top, bg="#f9f9f9", padx=15, pady=15, bd=1, relief="ridge")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        # Dùng Grid để căn chỉnh
        tk.Label(info_frame, text="Ngân hàng:", bg="#f9f9f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=2)
        tk.Label(info_frame, text="Vietcombank (VCB)", bg="#f9f9f9", font=("Arial", 10, "bold"), fg="#27ae60").grid(row=0, column=1, sticky="w", padx=10)
        
        tk.Label(info_frame, text="Số tài khoản:", bg="#f9f9f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(info_frame, text="9999.99.2025", bg="#f9f9f9", font=("Arial", 12, "bold"), fg="red").grid(row=1, column=1, sticky="w", padx=10)
        
        tk.Label(info_frame, text="Chủ TK:", bg="#f9f9f9", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=2)
        tk.Label(info_frame, text="MTTQ VN - BAN CUU TRO TW", bg="#f9f9f9", font=("Arial", 9, "bold")).grid(row=2, column=1, sticky="w", padx=10)
        
        tk.Label(info_frame, text="Số tiền:", bg="#f9f9f9", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=2)
        tk.Label(info_frame, text=f"{total_money:,} VND", bg="#f9f9f9", font=("Arial", 11, "bold"), fg="#e67e22").grid(row=3, column=1, sticky="w", padx=10)
        
        tk.Label(info_frame, text="Nội dung:", bg="#f9f9f9", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=2)
        tk.Label(info_frame, text=noi_dung_raw, bg="#f9f9f9", font=("Arial", 10, "bold")).grid(row=4, column=1, sticky="w", padx=10)

        # Nút xác nhận
        tk.Button(self.top, text="ĐÃ CHUYỂN KHOẢN", bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                  command=self.confirm_booking, width=25, height=2).pack(pady=10)

    def confirm_booking(self):
        total = len(self.selected_seats) * int(self.movie['GiaVe'])
        l = self.selected_lich
        
        data.luu_ve(
            self.user['ID_Nguoi_Dung'], self.movie['ID'], self.movie['Ten'], 
            ','.join(self.selected_seats), total, 
            l['Ngay'], l['Gio'], l['Phong']
        )
        
        messagebox.showinfo("Thành công", "Cảm ơn tấm lòng của bạn!\nVé đã được lưu vào hệ thống.")
        self.top.destroy()
        self.on_back_home()