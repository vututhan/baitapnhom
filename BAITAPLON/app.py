import tkinter as tk
# Import module của từng người
import auth_ui
import customer_ui
import admin_ui

# Cấu hình cửa sổ chính
root = tk.Tk()
root.title("HỆ THỐNG QUẢN LÝ VÉ XEM PHIM - TEAMWORK")
root.geometry("1000x700")

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def dang_xuat():
    clear_screen()
    auth_ui.LoginPage(root, on_success=xu_ly_dang_nhap_xong).pack(fill="both", expand=True)

def xu_ly_dang_nhap_xong(user_info):
    clear_screen()
    if user_info['VaiTro'] == 'admin':
        # Vào trang Admin (Phương)
        admin_ui.AdminDashboard(root, on_logout=dang_xuat).pack(fill="both", expand=True)
    else:
        # Vào trang Khách (Thế Anh + Vũ)
        customer_ui.CustomerDashboard(root, user=user_info, on_logout=dang_xuat).pack(fill="both", expand=True)

# Khởi chạy màn hình Login (Nghĩa) đầu tiên
if __name__ == "__main__":
    dang_xuat() # Gọi hàm này để hiển thị login
    root.mainloop()