import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import data

class AdminDashboard(tk.Frame):
    def __init__(self, master, on_logout):
        super().__init__(master)
        self.selected_phim_id = None
        self.selected_lich_id = None
        self.selected_user_id = None
        
        # --- HEADER ---
        top_frame = tk.Frame(self, bg="#2c3e50", height=50)
        top_frame.pack(fill="x")
        tk.Label(top_frame, text="QUẢN TRỊ VIÊN (ADMIN)", fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        tk.Button(top_frame, text="Đăng xuất", command=on_logout).pack(side="right", padx=10)
        
        # --- TABS ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_phim = tk.Frame(notebook)
        self.tab_lich = tk.Frame(notebook) 
        self.tab_user = tk.Frame(notebook) 
        self.tab_doanh_thu = tk.Frame(notebook)
        
        notebook.add(self.tab_phim, text="1. Quản lý Phim")
        notebook.add(self.tab_lich, text="2. Quản lý Lịch Chiếu")
        notebook.add(self.tab_user, text="3. Quản lý Người dùng")
        notebook.add(self.tab_doanh_thu, text="4. Doanh thu")
        
        self.build_tab_phim()
        self.build_tab_lich()
        self.build_tab_user()
        self.build_tab_doanh_thu()

    # ================= TAB 1: QUẢN LÝ PHIM (ĐÃ SỬA LỖI TÊN BIẾN) =================
    def build_tab_phim(self):
        # 1. Tìm kiếm
        frame_search = tk.Frame(self.tab_phim)
        frame_search.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_search, text="🔍 Tìm phim:").pack(side="left")
        
        # Sửa lỗi ở đây: entry_search -> entry_search_phim
        self.entry_search_phim = tk.Entry(frame_search, width=30)
        self.entry_search_phim.pack(side="left", padx=5)
        self.entry_search_phim.bind("<KeyRelease>", self.refresh_list_phim) # Tìm real-time

        # 2. Form Nhập liệu
        frame_input = tk.LabelFrame(self.tab_phim, text="Thông tin phim")
        frame_input.pack(fill="x", padx=5, pady=5)
        
        self.entries_phim = {}
        fields = ['Tên phim', 'Thể loại', 'Thời lượng', 'Năm', 'Giá vé', 'Link Poster']
        for i, field in enumerate(fields):
            tk.Label(frame_input, text=field).grid(row=0, column=i, padx=5, sticky="w")
            e = tk.Entry(frame_input, width=15)
            e.grid(row=1, column=i, padx=5, pady=5)
            self.entries_phim[field] = e
            
        btn_frame = tk.Frame(frame_input)
        btn_frame.grid(row=1, column=len(fields), padx=10)
        tk.Button(btn_frame, text="Thêm", bg="#27ae60", fg="white", command=self.add_movie).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Sửa", bg="#f39c12", fg="white", command=self.update_movie).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Xóa", bg="#c0392b", fg="white", command=self.delete_movie).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Reset", command=self.clear_form_phim).pack(side="left", padx=2)

        # 3. Bảng
        cols = ("ID", "Ten", "TheLoai", "ThoiLuong", "Nam", "GiaVe", "Poster")
        self.tree_phim = ttk.Treeview(self.tab_phim, columns=cols, show="headings", height=10)
        for col in cols: self.tree_phim.heading(col, text=col); self.tree_phim.column(col, width=100)
        self.tree_phim.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_phim.bind("<<TreeviewSelect>>", self.on_select_phim)
        self.refresh_list_phim()

    def on_select_phim(self, event):
        sel = self.tree_phim.selection()
        if not sel: return
        vals = self.tree_phim.item(sel[0])['values']
        self.selected_phim_id = vals[0]
        keys = ['Tên phim', 'Thể loại', 'Thời lượng', 'Năm', 'Giá vé', 'Link Poster']
        for i, k in enumerate(keys):
            self.entries_phim[k].delete(0, tk.END); self.entries_phim[k].insert(0, vals[i+1])

    def clear_form_phim(self):
        self.selected_phim_id = None
        for e in self.entries_phim.values(): e.delete(0, tk.END)

    def add_movie(self):
        d = {k: v.get() for k, v in self.entries_phim.items()}
        data.them_phim(d['Tên phim'], d['Thể loại'], d['Thời lượng'], d['Năm'], d['Giá vé'], d['Link Poster'])
        self.refresh_list_phim(None); self.clear_form_phim()

    def update_movie(self):
        if not self.selected_phim_id: return messagebox.showwarning("Lỗi", "Chọn phim cần sửa!")
        d = {k: v.get() for k, v in self.entries_phim.items()}
        data.cap_nhat_phim(self.selected_phim_id, d['Tên phim'], d['Thể loại'], d['Thời lượng'], d['Năm'], d['Giá vé'], d['Link Poster'])
        self.refresh_list_phim(None); self.clear_form_phim(); messagebox.showinfo("OK", "Đã cập nhật!")

    def delete_movie(self):
        if not self.selected_phim_id: return
        if messagebox.askyesno("Xóa", "Bạn chắc chắn muốn xóa?"):
            data.xoa_phim(self.selected_phim_id)
            self.refresh_list_phim(None); self.clear_form_phim()

    def refresh_list_phim(self, event=None):
        for i in self.tree_phim.get_children(): self.tree_phim.delete(i)
        keyword = self.entry_search_phim.get().lower()
        
        for p in data.doc_danh_sach_phim():
            if keyword in p['Ten'].lower():
                self.tree_phim.insert("", "end", values=(p['ID'], p['Ten'], p['TheLoai'], p['ThoiLuong'], p['Nam'], p['GiaVe'], p['Poster']))

    # ================= TAB 2: QUẢN LÝ LỊCH CHIẾU (SỬA/XÓA/AUTO) =================
    def build_tab_lich(self):
        frame_input = tk.LabelFrame(self.tab_lich, text="Thông tin Lịch Chiếu")
        frame_input.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_input, text="Phim:").grid(row=0, column=0); self.cb_phim = ttk.Combobox(frame_input, width=20, state="readonly"); self.cb_phim.grid(row=0, column=1)
        tk.Label(frame_input, text="Ngày:").grid(row=0, column=2); self.cb_ngay = ttk.Combobox(frame_input, width=10, state="readonly"); 
        today = datetime.now(); self.cb_ngay['values'] = [(today + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)]; self.cb_ngay.current(0); self.cb_ngay.grid(row=0, column=3)
        tk.Label(frame_input, text="Giờ:").grid(row=0, column=4); self.cb_gio = ttk.Combobox(frame_input, values=["09:00","12:00","15:00","18:00","21:00"], width=8); self.cb_gio.current(0); self.cb_gio.grid(row=0, column=5)
        tk.Label(frame_input, text="Phòng:").grid(row=0, column=6); self.cb_phong = ttk.Combobox(frame_input, values=["Phòng 01","Phòng 02","Phòng VIP"], width=10); self.cb_phong.current(0); self.cb_phong.grid(row=0, column=7)
        
        # Nút chức năng
        btn_frame = tk.Frame(frame_input)
        btn_frame.grid(row=0, column=8, padx=10)
        tk.Button(btn_frame, text="Thêm", bg="#27ae60", fg="white", command=self.add_schedule).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Sửa", bg="#f39c12", fg="white", command=self.update_schedule).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Xóa", bg="#c0392b", fg="white", command=self.delete_schedule).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Reset", command=self.clear_form_lich).pack(side="left", padx=2)
        
        # Auto button
        tk.Button(self.tab_lich, text="⚡ XẾP LỊCH TỰ ĐỘNG (3 NGÀY)", bg="#8e44ad", fg="white", command=self.auto_schedule).pack(pady=5)

        cols = ("ID", "TenPhim", "Ngay", "Gio", "Phong")
        self.tree_lich = ttk.Treeview(self.tab_lich, columns=cols, show="headings")
        for c in cols: self.tree_lich.heading(c, text=c)
        self.tree_lich.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree_lich.bind("<<TreeviewSelect>>", self.on_select_schedule)
        self.tab_lich.bind("<Visibility>", self.refresh_data_lich)
        self.refresh_data_lich(None)

    def refresh_data_lich(self, event):
        phims = data.doc_danh_sach_phim()
        self.phim_map = {p['Ten']: p['ID'] for p in phims} 
        self.cb_phim['values'] = list(self.phim_map.keys())
        if self.phim_map and not self.cb_phim.get(): self.cb_phim.current(0)
        
        for item in self.tree_lich.get_children(): self.tree_lich.delete(item)
        lichs = data.doc_toan_bo_lich()
        lichs.sort(key=lambda x: int(x['ID_Lich']), reverse=True)
        for l in lichs: self.tree_lich.insert("", "end", values=(l['ID_Lich'], l['TenPhim'], l['Ngay'], l['Gio'], l['Phong']))

    def on_select_schedule(self, event):
        sel = self.tree_lich.selection()
        if not sel: return
        vals = self.tree_lich.item(sel[0])['values']
        self.selected_lich_id = vals[0]
        self.cb_phim.set(vals[1]); self.cb_ngay.set(vals[2]); self.cb_gio.set(vals[3]); self.cb_phong.set(vals[4])

    def clear_form_lich(self):
        self.selected_lich_id = None
        if self.tree_lich.selection(): self.tree_lich.selection_remove(self.tree_lich.selection()[0])

    def add_schedule(self):
        ten = self.cb_phim.get()
        if not ten: return
        success, msg = data.them_lich_chieu(self.phim_map[ten], ten, self.cb_ngay.get(), self.cb_gio.get(), self.cb_phong.get())
        if success: self.refresh_data_lich(None); messagebox.showinfo("OK", msg)
        else: messagebox.showwarning("Trùng", msg)

    def update_schedule(self):
        if not self.selected_lich_id: return messagebox.showwarning("Lỗi", "Chọn lịch cần sửa!")
        ten = self.cb_phim.get()
        success, msg = data.cap_nhat_lich_chieu(self.selected_lich_id, self.phim_map[ten], ten, self.cb_ngay.get(), self.cb_gio.get(), self.cb_phong.get())
        if success: self.refresh_data_lich(None); self.clear_form_lich(); messagebox.showinfo("OK", msg)
        else: messagebox.showwarning("Lỗi", msg)

    def delete_schedule(self):
        if not self.selected_lich_id: return
        if messagebox.askyesno("Xóa", "Xóa lịch chiếu này?"):
            data.xoa_lich_chieu(self.selected_lich_id)
            self.refresh_data_lich(None); self.clear_form_lich()

    def auto_schedule(self):
        if messagebox.askyesno("Auto", "Tự động xếp lịch cho 3 ngày tới?"):
            ok, msg = data.tu_dong_xep_lich()
            if ok: self.refresh_data_lich(None); messagebox.showinfo("OK", msg)
            else: messagebox.showerror("Lỗi", msg)

    # ================= TAB 3: QUẢN LÝ USER (ĐÃ SỬA LỖI TÊN BIẾN) =================
    def build_tab_user(self):
        # Tìm kiếm
        frame_search = tk.Frame(self.tab_user)
        frame_search.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_search, text="🔍 Tìm SĐT/Tên:").pack(side="left")
        
        # Sửa lỗi ở đây: entry_search -> entry_search_user
        self.entry_search_user = tk.Entry(frame_search, width=30)
        self.entry_search_user.pack(side="left", padx=5)
        self.entry_search_user.bind("<KeyRelease>", lambda e: self.refresh_list_user())

        # Form sửa
        frame_edit = tk.LabelFrame(self.tab_user, text="Sửa thông tin User")
        frame_edit.pack(fill="x", padx=10)
        
        self.entries_user = {}
        fields = ['Tên', 'SĐT', 'Email', 'Mật khẩu', 'Vai trò']
        for i, f in enumerate(fields):
            tk.Label(frame_edit, text=f).grid(row=0, column=i)
            e = tk.Entry(frame_edit, width=15)
            e.grid(row=1, column=i, padx=5, pady=5)
            self.entries_user[f] = e
            
        tk.Button(frame_edit, text="Lưu Sửa", bg="#f39c12", fg="white", command=self.update_user).grid(row=1, column=5, padx=5)
        tk.Button(frame_edit, text="Xóa User", bg="#c0392b", fg="white", command=self.delete_user).grid(row=1, column=6, padx=5)

        # Bảng
        cols = ("ID", "Ten", "VaiTro", "SDT", "Email", "MatKhau", "NgayTao")
        self.tree_user = ttk.Treeview(self.tab_user, columns=cols, show="headings")
        for c in cols: self.tree_user.heading(c, text=c)
        self.tree_user.column("ID", width=50); self.tree_user.column("VaiTro", width=70)
        self.tree_user.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree_user.bind("<<TreeviewSelect>>", self.on_select_user)
        self.tab_user.bind("<Visibility>", lambda e: self.refresh_list_user())
        self.refresh_list_user()

    def on_select_user(self, event):
        sel = self.tree_user.selection()
        if not sel: return
        vals = self.tree_user.item(sel[0])['values']
        self.selected_user_id = vals[0]
        # Fill form
        self.entries_user['Tên'].delete(0, tk.END); self.entries_user['Tên'].insert(0, vals[1])
        self.entries_user['Vai trò'].delete(0, tk.END); self.entries_user['Vai trò'].insert(0, vals[2])
        self.entries_user['SĐT'].delete(0, tk.END); self.entries_user['SĐT'].insert(0, vals[3])
        self.entries_user['Email'].delete(0, tk.END); self.entries_user['Email'].insert(0, vals[4])
        self.entries_user['Mật khẩu'].delete(0, tk.END); self.entries_user['Mật khẩu'].insert(0, vals[5])

    def refresh_list_user(self):
        for i in self.tree_user.get_children(): self.tree_user.delete(i)
        users = data.doc_danh_sach_user()
        
        # 1. Lọc theo từ khóa
        keyword = self.entry_search_user.get().lower()
        users = [u for u in users if keyword in u['Ten'].lower() or keyword in u['SoDienThoai']]
        
        # 2. Sắp xếp: Admin (ID 9999) lên đầu
        users.sort(key=lambda x: 0 if str(x['ID_Nguoi_Dung']) == '9999' else 1)
        
        for u in users:
            self.tree_user.insert("", "end", values=(u['ID_Nguoi_Dung'], u['Ten'], u['VaiTro'], u['SoDienThoai'], u['Email'], u['MatKhau'], u['ThoiGianTao']))

    def update_user(self):
        if not self.selected_user_id: return messagebox.showwarning("Lỗi", "Chọn user!")
        d = {k: v.get() for k, v in self.entries_user.items()}
        
        data.cap_nhat_thong_tin_user(self.selected_user_id, d['Tên'], d['SĐT'], d['Email'], d['Mật khẩu'], d['Vai trò'])
        self.refresh_list_user(); messagebox.showinfo("OK", "Đã cập nhật!")

    def delete_user(self):
        if not self.selected_user_id: return
        if str(self.selected_user_id) == '9999': return messagebox.showwarning("Cấm", "Không thể xóa Super Admin!")
        if messagebox.askyesno("Xóa", "Xóa user này?"):
            data.xoa_user(self.selected_user_id)
            self.refresh_list_user()

    # ================= TAB 4: DOANH THU =================
    def build_tab_doanh_thu(self):
        frame_dt = tk.Frame(self.tab_doanh_thu)
        frame_dt.pack(expand=True)
        self.lbl_doanh_thu = tk.Label(frame_dt, text="0 VND", font=("Arial", 30, "bold"), fg="#27ae60")
        self.lbl_doanh_thu.pack(pady=20)
        tk.Button(frame_dt, text="Cập nhật doanh thu", command=self.update_dt, height=2).pack()
        self.update_dt()
        
    def update_dt(self):
        total = data.thong_ke_doanh_thu()
        self.lbl_doanh_thu.config(text=f"{total:,} VND")