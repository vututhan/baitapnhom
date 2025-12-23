import tkinter as tk
from tkinter import ttk, messagebox
import threading
import data          # Module dữ liệu
import poster_utils  # Module ảnh
import booking_ui    # Module đặt vé

# =============================================================================
# 1. TRANG CHI TIẾT PHIM (Giữ nguyên)
# =============================================================================
class MovieDetailPage(tk.Frame):
    def __init__(self, master, user, phim, on_back, on_book_now):
        super().__init__(master, bg="white")
        self.phim = phim
        
        # Header
        header = tk.Frame(self, bg="white")
        header.pack(fill="x", pady=5, padx=10)
        tk.Button(header, text="< Quay lại", command=on_back, bg="#ecf0f1", fg="#2c3e50", bd=0, padx=15, pady=8).pack(side="left")
        
        # Container chính
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cột trái: Ảnh
        frame_img = tk.Frame(container, bg="white")
        frame_img.pack(side="left", fill="y", padx=(0, 20), anchor="n")
        
        self.lbl_poster = tk.Label(frame_img, text="Loading...", bg="#bdc3c7", width=30, height=20)
        self.lbl_poster.pack()
        threading.Thread(target=self.safe_load_image, args=(phim.get('Poster'), self.lbl_poster, (250, 370)), daemon=True).start()
        
        # Cột phải: Thông tin
        frame_info = tk.Frame(container, bg="white")
        frame_info.pack(side="left", fill="both", expand=True)
        
        tk.Label(frame_info, text=phim['Ten'], font=("Arial", 22, "bold"), bg="white", fg="#2c3e50", wraplength=500, justify="left").pack(anchor="w", pady=(0, 10))
        
        infos = [
            ("Thể loại", phim.get('TheLoai', 'Unknown')),
            ("Thời lượng", phim.get('ThoiLuong', '--')),
            ("Đạo diễn", phim.get('DaoDien', '--')),
            ("Giá vé", f"{int(phim.get('GiaVe', 0)):,} VNĐ")
        ]
        for k, v in infos:
            row = tk.Frame(frame_info, bg="white")
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=f"{k}: ", font=("Arial", 10, "bold"), bg="white", width=10, anchor="w").pack(side="left")
            tk.Label(row, text=v, font=("Arial", 10), bg="white").pack(side="left")

        tk.Label(frame_info, text="Nội dung:", font=("Arial", 11, "bold"), bg="white", pady=10).pack(anchor="w")
        txt = tk.Text(frame_info, height=8, bg="#f9f9f9", bd=0, padx=10, pady=10, font=("Arial", 10), wrap="word")
        txt.insert("1.0", phim.get('MoTa', 'Đang cập nhật...'))
        txt.config(state="disabled")
        txt.pack(fill="x")
        
        tk.Button(frame_info, text="ĐẶT VÉ NGAY", bg="#e67e22", fg="white", font=("Arial", 12, "bold"), 
                  padx=20, pady=10, command=lambda: on_book_now(phim)).pack(pady=20, anchor="w")

    def safe_load_image(self, url, label, size):
        if not url: return
        try:
            img = poster_utils.load_image_from_url(url, size=size)
            label.after(0, lambda: self.update_img(label, img))
        except: pass
        
    def update_img(self, label, img):
        label.config(image=img, text="", width=0, height=0)
        label.image = img

# =============================================================================
# 2. GIAO DIỆN KHÁCH HÀNG (FULL CHỨC NĂNG)
# =============================================================================
class CustomerDashboard(tk.Frame):
    def __init__(self, master, user, on_logout):
        super().__init__(master)
        self.master = master
        self.user = user
        self.on_logout = on_logout
        self.movie_widgets = []
        self.all_phims = []
        
        # --- MENU BAR ---
        menu_frame = tk.Frame(self, bg="#333", height=60)
        menu_frame.pack(fill="x", side="top")
        
        # 1. User Info
        self.lbl_user_name = tk.Label(menu_frame, text=f"👤 {user.get('Ten','Khách')}", bg="#333", fg="#f1c40f", font=("Arial", 11, "bold"))
        self.lbl_user_name.pack(side="left", padx=15)
        
        # 2. THANH TÌM KIẾM
        search_frame = tk.Frame(menu_frame, bg="#333")
        search_frame.pack(side="left", padx=10)
        
        tk.Label(search_frame, text="🔍 Tìm:", bg="#333", fg="white", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.entry_search = tk.Entry(search_frame, width=25, font=("Arial", 10))
        self.entry_search.pack(side="left")
        self.entry_search.insert(0, "Nhập tên phim...")
        
        self.entry_search.bind("<FocusIn>", self.on_search_focus_in)
        self.entry_search.bind("<FocusOut>", self.on_search_focus_out)
        self.entry_search.bind("<KeyRelease>", self.apply_filters)

        # 3. BỘ LỌC
        tk.Label(menu_frame, text="Thể loại:", bg="#333", fg="white", font=("Arial", 10)).pack(side="left", padx=(15, 5))
        self.cb_theloai = ttk.Combobox(menu_frame, state="readonly", width=15)
        self.cb_theloai.pack(side="left")
        self.cb_theloai.bind("<<ComboboxSelected>>", self.apply_filters)

        # 4. BUTTONS
        tk.Button(menu_frame, text="Đăng xuất", command=on_logout, bg="#c0392b", fg="white", bd=0, padx=10).pack(side="right", padx=5)
        tk.Button(menu_frame, text="Hồ sơ", command=self.show_profile, bg="#8e44ad", fg="white", bd=0, padx=10).pack(side="right", padx=5)
        tk.Button(menu_frame, text="Lịch sử", command=self.show_history, bg="#2980b9", fg="white", bd=0, padx=10).pack(side="right", padx=5)
        tk.Button(menu_frame, text="Trang chủ", command=self.show_home, bg="#27ae60", fg="white", bd=0, padx=10).pack(side="right", padx=5)

        # --- CONTENT FRAME ---
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        
        # Load dữ liệu
        try:
            self.all_phims = data.doc_danh_sach_phim()
        except Exception as e:
            print(f"[LỖI] Không đọc được data: {e}")
            self.all_phims = []

        self.show_home()

    # --- XỬ LÝ SEARCH ---
    def on_search_focus_in(self, event):
        if self.entry_search.get() == "Nhập tên phim...":
            self.entry_search.delete(0, "end"); self.entry_search.config(fg="black")
    def on_search_focus_out(self, event):
        if self.entry_search.get() == "":
            self.entry_search.insert(0, "Nhập tên phim..."); self.entry_search.config(fg="grey")

    def apply_filters(self, event=None):
        genre = self.cb_theloai.get()
        keyword = self.entry_search.get().lower()
        if keyword == "nhập tên phim...": keyword = ""
        
        result = []
        for p in self.all_phims:
            match_genre = (genre == "Tất cả" or not genre) or (genre in p.get('TheLoai', ''))
            match_keyword = keyword in p.get('Ten', '').lower()
            if match_genre and match_keyword: result.append(p)
        self.render_movie_list(result)

    # --- HIỂN THỊ HOME ---
    def show_home(self):
        self.clear_content()
        
        self.canvas = tk.Canvas(self.content_frame, bg="#ecf0f1")
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#ecf0f1")
        
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        window_id = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(window_id, width=e.width))
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind('<Enter>', lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind('<Leave>', lambda e: self.canvas.unbind_all("<MouseWheel>"))
        
        self.update_genre_list()
        self.render_movie_list(self.all_phims)

    def update_genre_list(self):
        genres = set()
        for p in self.all_phims:
            parts = [x.strip() for x in p.get('TheLoai', '').split(',') if x.strip()]
            genres.update(parts)
        self.cb_theloai['values'] = ["Tất cả"] + sorted(list(genres))
        if not self.cb_theloai.get(): self.cb_theloai.current(0)

    def render_movie_list(self, phim_list):
        for w in self.scroll_frame.winfo_children(): w.destroy()

        if not phim_list:
            tk.Label(self.scroll_frame, text="Không tìm thấy phim phù hợp!", 
                     font=("Arial", 14), bg="#ecf0f1", fg="#7f8c8d").pack(pady=50)
            return

        grid_frame = tk.Frame(self.scroll_frame, bg="#ecf0f1")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_idletasks() 
        width = self.master.winfo_width()
        if width < 100: width = 800
        cols = max(1, width // 230) 

        for i, phim in enumerate(phim_list):
            card = tk.Frame(grid_frame, bg="white", bd=1, relief="raised")
            card.grid(row=i//cols, column=i%cols, padx=10, pady=10, sticky="nsew")
            
            lbl_img = tk.Label(card, bg="#bdc3c7", width=22, height=12, text="No Image", fg="white", cursor="hand2")
            lbl_img.pack(pady=5, padx=5)
            lbl_img.bind("<Button-1>", lambda e, p=phim: self.go_to_details(p))
            threading.Thread(target=self.safe_load_image, args=(phim.get('Poster'), lbl_img), daemon=True).start()
            
            tk.Label(card, text=phim.get('Ten', 'No Name'), font=("Arial", 10, "bold"), bg="white", wraplength=180).pack()
            tk.Label(card, text=f"{int(phim.get('GiaVe',0)):,} đ", fg="#e74c3c", bg="white").pack()
            
            tk.Button(card, text="CHI TIẾT", bg="#3498db", fg="white", font=("Arial", 8, "bold"),
                      command=lambda p=phim: self.go_to_details(p)).pack(pady=5)
        
        self.scroll_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def safe_load_image(self, url, label):
        if not url: return
        try:
            img = poster_utils.load_image_from_url(url)
            label.after(0, lambda: self.update_img_ui(label, img))
        except: pass

    def update_img_ui(self, label, img):
        label.config(image=img, width=0, height=0, text="")
        label.image = img

    def go_to_details(self, phim):
        self.clear_content()
        MovieDetailPage(self.content_frame, self.user, phim, self.show_home, self.go_to_booking).pack(fill="both", expand=True)

    def go_to_booking(self, phim):
        self.clear_content()
        booking_ui.BookingPage(self.content_frame, self.user, phim, on_back_home=self.show_home).pack(fill="both", expand=True)

    # --- CHỨC NĂNG HỒ SƠ & SỬA ĐỔI (CÓ ĐỔI PASSWORD) ---
    def show_profile(self):
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg="white")
        header.pack(fill="x", pady=10)
        tk.Button(header, text="< Quay lại", command=self.show_home, bg="#ecf0f1", bd=0, padx=15, pady=5).pack(side="left", padx=10)
        tk.Label(header, text="HỒ SƠ CÁ NHÂN", font=("Arial", 16, "bold"), fg="#8e44ad", bg="white").pack(side="left", padx=20)
        
        form = tk.Frame(self.content_frame, bg="white", bd=1, relief="solid", padx=40, pady=40)
        form.pack(pady=20)
        
        # Tên
        tk.Label(form, text="Tên hiển thị:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.entry_name = tk.Entry(form, width=30, font=("Arial", 11))
        self.entry_name.insert(0, self.user.get('Ten', ''))
        self.entry_name.pack(fill="x")
        
        # Email
        tk.Label(form, text="Email:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.entry_email = tk.Entry(form, width=30, font=("Arial", 11))
        self.entry_email.insert(0, self.user.get('Email', ''))
        self.entry_email.pack(fill="x")
        
        # SĐT
        tk.Label(form, text="Số điện thoại:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.entry_sdt = tk.Entry(form, width=30, font=("Arial", 11))
        self.entry_sdt.insert(0, self.user.get('SoDienThoai', ''))
        self.entry_sdt.pack(fill="x")

        # Mật khẩu (Thêm mới)
        tk.Label(form, text="Mật khẩu:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.entry_pass = tk.Entry(form, width=30, font=("Arial", 11), show="*")
        self.entry_pass.insert(0, self.user.get('MatKhau', ''))
        self.entry_pass.pack(fill="x")
        
        # Nút Lưu
        tk.Button(form, text="LƯU THAY ĐỔI", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), 
                  command=self.save_profile, pady=8).pack(fill="x", pady=30)

    def save_profile(self):
        ten = self.entry_name.get()
        email = self.entry_email.get()
        sdt = self.entry_sdt.get()
        mat_khau = self.entry_pass.get() # Lấy mật khẩu mới
        
        if not ten or not email or not mat_khau:
            messagebox.showwarning("Lỗi", "Không được để trống thông tin!")
            return
            
        # Gọi hàm backend mới (có mat_khau)
        if data.cap_nhat_thong_tin_user(self.user['ID_Nguoi_Dung'], ten, sdt, email, mat_khau):
            self.user['Ten'] = ten
            self.user['Email'] = email
            self.user['SoDienThoai'] = sdt
            self.user['MatKhau'] = mat_khau
            
            self.lbl_user_name.config(text=f"👤 {ten}")
            messagebox.showinfo("Thành công", "Đã cập nhật hồ sơ & mật khẩu!")
        else:
            messagebox.showerror("Lỗi", "Không thể lưu thông tin. Vui lòng thử lại.")

    # --- CHỨC NĂNG LỊCH SỬ ---
    def show_history(self):
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg="white")
        header.pack(fill="x", pady=10)
        tk.Button(header, text="< Quay lại", command=self.show_home, bg="#ecf0f1", bd=0, padx=15, pady=5).pack(side="left", padx=10)
        tk.Label(header, text="LỊCH SỬ GIAO DỊCH", font=("Arial", 16, "bold"), fg="#2980b9", bg="white").pack(side="left", padx=20)
        
        cols = ("Phim", "NgayChieu", "Gio", "Phong", "Ghe", "Tien", "ThoiGianDat")
        headers = ("Tên Phim", "Ngày Chiếu", "Giờ", "Phòng", "Ghế", "Tổng Tiền", "Thời Gian Đặt")
        
        tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        tree.column("Phim", width=200); tree.column("NgayChieu", width=100, anchor="center")
        tree.column("Gio", width=80, anchor="center"); tree.column("Phong", width=80, anchor="center")
        tree.column("Ghe", width=150, anchor="w"); tree.column("Tien", width=100, anchor="e")
        tree.column("ThoiGianDat", width=150, anchor="center")
        
        for col, title in zip(cols, headers): tree.heading(col, text=title)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            history = data.doc_lich_su_ve(self.user['ID_Nguoi_Dung'])
            for ve in reversed(history):
                tree.insert("", "end", values=(ve['MovieName'], ve.get('NgayChieu', ''), ve.get('SuatChieu', ''), ve.get('PhongChieu', ''), ve['Seats'], f"{int(ve['TotalPrice']):,} đ", ve['Time']))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tải được dữ liệu: {e}")
    
    def clear_content(self):
        self.canvas = None
        for w in self.content_frame.winfo_children(): w.destroy()
        
    def _on_mousewheel(self, event):
        if self.canvas: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")