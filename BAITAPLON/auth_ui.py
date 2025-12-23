import tkinter as tk
from tkinter import messagebox, Toplevel
import data

class LoginPage(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.master = master
        self.on_success = on_success # Callback function khi login thành công
        
        self.configure(bg="#f0f0f0")
        
        # Tạo khung đăng nhập ở giữa
        frame = tk.Frame(self, bg="white", padx=20, pady=20, bd=1, relief="solid")
        frame.pack(pady=100)
        
        tk.Label(frame, text="RẠP CHIẾU PHIM", font=("Arial", 20, "bold"), bg="white", fg="#e74c3c").pack(pady=10)
        
        tk.Label(frame, text="Tên đăng nhập:", bg="white").pack(anchor="w")
        self.entry_user = tk.Entry(frame, width=30)
        self.entry_user.pack(pady=5)
        
        tk.Label(frame, text="Mật khẩu:", bg="white").pack(anchor="w")
        self.entry_pass = tk.Entry(frame, show="*", width=30)
        self.entry_pass.pack(pady=5)
        
        tk.Button(frame, text="Đăng nhập", command=self.handle_login, bg="#3498db", fg="white", width=25).pack(pady=15)
        tk.Button(frame, text="Đăng ký tài khoản mới", command=self.show_register, bg="white", fg="#3498db", bd=0).pack()

    def handle_login(self):import tkinter as tk
from tkinter import messagebox, Toplevel
import data

class LoginPage(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.master = master
        self.on_success = on_success # Callback function khi login thành công
        
        self.configure(bg="#f0f0f0")
        
        # Tạo khung đăng nhập ở giữa
        frame = tk.Frame(self, bg="white", padx=20, pady=20, bd=1, relief="solid")
        frame.pack(pady=100)
        
        tk.Label(frame, text="RẠP CHIẾU PHIM", font=("Arial", 20, "bold"), bg="white", fg="#e74c3c").pack(pady=10)
        
        tk.Label(frame, text="Tên đăng nhập:", bg="white").pack(anchor="w")
        self.entry_user = tk.Entry(frame, width=30)
        self.entry_user.pack(pady=5)
        
        tk.Label(frame, text="Mật khẩu:", bg="white").pack(anchor="w")
        self.entry_pass = tk.Entry(frame, show="*", width=30)
        self.entry_pass.pack(pady=5)
        
        tk.Button(frame, text="Đăng nhập", command=self.handle_login, bg="#3498db", fg="white", width=25).pack(pady=15)
        tk.Button(frame, text="Đăng ký tài khoản mới", command=self.show_register, bg="white", fg="#3498db", bd=0).pack()

    def handle_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        user = data.check_login(u, p)
        if user:
            messagebox.showinfo("Thành công", f"Chào mừng {user['Ten']}!")
            self.on_success(user) # Gọi hàm callback ở app.py để chuyển trang
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

    def show_register(self):
        RegisterPopup(self.master)

class RegisterPopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Đăng ký")
        self.geometry("300x350")
        
        tk.Label(self, text="ĐĂNG KÝ", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self, text="Tên đăng nhập:").pack(anchor="w", padx=20)
        self.e_ten = tk.Entry(self, width=30)
        self.e_ten.pack(padx=20)

        tk.Label(self, text="Mật khẩu:").pack(anchor="w", padx=20)
        self.e_pass = tk.Entry(self, width=30, show="*")
        self.e_pass.pack(padx=20)
        
        tk.Label(self, text="Email:").pack(anchor="w", padx=20)
        self.e_email = tk.Entry(self, width=30)
        self.e_email.pack(padx=20)
        
        tk.Label(self, text="SĐT:").pack(anchor="w", padx=20)
        self.e_sdt = tk.Entry(self, width=30)
        self.e_sdt.pack(padx=20)
        
        tk.Button(self, text="Đăng ký ngay", command=self.save, bg="#2ecc71", fg="white").pack(pady=20)

    def save(self):
        # Gọi hàm đăng ký từ data.py
        if data.register_user(self.e_ten.get(), self.e_pass.get(), self.e_sdt.get(), self.e_email.get()):
            messagebox.showinfo("OK", "Đăng ký thành công! Hãy đăng nhập.")
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra (có thể file CSV đang mở hoặc lỗi ghi file).")
        u = self.entry_user.get()
        p = self.entry_pass.get()
        user = data.check_login(u, p)
        if user:
            messagebox.showinfo("Thành công", f"Chào mừng {user['Ten']}!")
            self.on_success(user) # Gọi hàm callback ở app.py để chuyển trang
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

    def show_register(self):
        RegisterPopup(self.master)

class RegisterPopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Đăng ký")
        self.geometry("300x350")
        
        tk.Label(self, text="ĐĂNG KÝ", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self, text="Tên đăng nhập:").pack(anchor="w", padx=20)
        self.e_ten = tk.Entry(self, width=30)
        self.e_ten.pack(padx=20)

        tk.Label(self, text="Mật khẩu:").pack(anchor="w", padx=20)
        self.e_pass = tk.Entry(self, width=30, show="*")
        self.e_pass.pack(padx=20)
        
        tk.Label(self, text="Email:").pack(anchor="w", padx=20)
        self.e_email = tk.Entry(self, width=30)
        self.e_email.pack(padx=20)
        
        tk.Label(self, text="SĐT:").pack(anchor="w", padx=20)
        self.e_sdt = tk.Entry(self, width=30)
        self.e_sdt.pack(padx=20)
        
        tk.Button(self, text="Đăng ký ngay", command=self.save, bg="#2ecc71", fg="white").pack(pady=20)

    def save(self):
        # Gọi hàm đăng ký từ data.py
        if data.register_user(self.e_ten.get(), self.e_pass.get(), self.e_sdt.get(), self.e_email.get()):
            messagebox.showinfo("OK", "Đăng ký thành công! Hãy đăng nhập.")
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra (có thể file CSV đang mở hoặc lỗi ghi file).")