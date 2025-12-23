import csv
import os
import time
import random
from datetime import datetime, timedelta

FILE_PHIM = 'Du_lieu_phim.csv'
FILE_USER = 'Nguoi_dung.csv'
FILE_VE = 'Ve.csv'
FILE_LICH = 'Lich_chieu.csv'

# ================= 1. LOGIC PHIM =================
def doc_danh_sach_phim():
    phims = []
    if not os.path.exists(FILE_PHIM): return []
    with open(FILE_PHIM, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: phims.append(row)
    return phims

def them_phim(ten, the_loai, thoi_luong, nam, gia, poster):
    new_id = int(time.time())
    file_exists = os.path.isfile(FILE_PHIM)
    with open(FILE_PHIM, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['ID', 'Ten', 'TheLoai', 'ThoiLuong', 'Nam', 'GiaVe', 'Poster']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        writer.writerow({'ID': new_id, 'Ten': ten, 'TheLoai': the_loai, 'ThoiLuong': thoi_luong, 'Nam': nam, 'GiaVe': gia, 'Poster': poster})

def cap_nhat_phim(id_phim, ten, the_loai, thoi_luong, nam, gia, poster):
    phims = doc_danh_sach_phim()
    updated = False
    for p in phims:
        if str(p['ID']) == str(id_phim):
            p.update({'Ten': ten, 'TheLoai': the_loai, 'ThoiLuong': thoi_luong, 'Nam': nam, 'GiaVe': gia, 'Poster': poster})
            updated = True; break
    if updated:
        with open(FILE_PHIM, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['ID', 'Ten', 'TheLoai', 'ThoiLuong', 'Nam', 'GiaVe', 'Poster']
            writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(phims)
    return updated

def xoa_phim(id_phim):
    phims = doc_danh_sach_phim()
    phims = [p for p in phims if str(p['ID']) != str(id_phim)]
    with open(FILE_PHIM, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['ID', 'Ten', 'TheLoai', 'ThoiLuong', 'Nam', 'GiaVe', 'Poster']
        writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(phims)

# ================= 2. LOGIC USER (AUTH & EDIT) =================
def doc_danh_sach_user():
    users = []
    if not os.path.exists(FILE_USER): return []
    with open(FILE_USER, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader: users.append(row)
    return users

def check_login(username, password):
    users = doc_danh_sach_user()
    for row in users:
        if row['Ten'] == username and row['MatKhau'] == password: return row
    return None

def register_user(ten, mat_khau, so_dien_thoai, email):
    new_id = int(time.time()); thoi_gian = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(FILE_USER)
    with open(FILE_USER, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['ID_Nguoi_Dung','Ten','MatKhau','VaiTro','SoDienThoai','Email','ThoiGianTao','TrangThai']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        writer.writerow({'ID_Nguoi_Dung': new_id, 'Ten': ten, 'MatKhau': mat_khau, 'VaiTro': 'customer', 'SoDienThoai': so_dien_thoai, 'Email': email, 'ThoiGianTao': thoi_gian, 'TrangThai': 'Active'})
    return True

def cap_nhat_thong_tin_user(user_id, ten_moi, sdt_moi, email_moi, mat_khau_moi, vai_tro_moi="customer"):
    """Admin dùng hàm này để sửa thông tin bất kỳ user nào"""
    users = doc_danh_sach_user()
    updated = False
    for u in users:
        if str(u['ID_Nguoi_Dung']) == str(user_id):
            u['Ten'] = ten_moi
            u['SoDienThoai'] = sdt_moi
            u['Email'] = email_moi
            u['MatKhau'] = mat_khau_moi
            if str(user_id) != '9999': # Không cho sửa quyền của Super Admin
                u['VaiTro'] = vai_tro_moi
            updated = True
            break
            
    if updated:
        with open(FILE_USER, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['ID_Nguoi_Dung','Ten','MatKhau','VaiTro','SoDienThoai','Email','ThoiGianTao','TrangThai']
            writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(users)
    return updated

def xoa_user(user_id):
    users = doc_danh_sach_user()
    # Không xóa admin ID 9999
    users = [u for u in users if str(u['ID_Nguoi_Dung']) != str(user_id) or str(u['ID_Nguoi_Dung']) == '9999']
    with open(FILE_USER, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['ID_Nguoi_Dung','Ten','MatKhau','VaiTro','SoDienThoai','Email','ThoiGianTao','TrangThai']
        writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(users)

# ================= 3. LOGIC LỊCH CHIẾU (CÓ SỬA/XÓA) =================
def doc_toan_bo_lich():
    lich = []
    if not os.path.exists(FILE_LICH): return []
    with open(FILE_LICH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f); 
        for row in reader: lich.append(row)
    return lich

def them_lich_chieu(movie_id, ten_phim, ngay, gio, phong):
    # Check trùng
    for l in doc_toan_bo_lich():
        if (l['Ngay'] == ngay and l['Gio'] == gio and l['Phong'] == phong):
            return False, f"Trùng lịch tại {phong} lúc {gio} ngày {ngay}!"
    
    new_id = int(time.time())
    file_exists = os.path.isfile(FILE_LICH)
    with open(FILE_LICH, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['ID_Lich', 'MovieID', 'TenPhim', 'Ngay', 'Gio', 'Phong']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        writer.writerow({'ID_Lich': new_id, 'MovieID': movie_id, 'TenPhim': ten_phim, 'Ngay': ngay, 'Gio': gio, 'Phong': phong})
    return True, "Thêm lịch thành công!"

def cap_nhat_lich_chieu(id_lich, movie_id, ten_phim, ngay, gio, phong):
    all_lich = doc_toan_bo_lich()
    # Check trùng (trừ chính nó)
    for l in all_lich:
        if str(l['ID_Lich']) != str(id_lich):
            if (l['Ngay'] == ngay and l['Gio'] == gio and l['Phong'] == phong):
                return False, f"Trùng lịch tại {phong} lúc {gio}!"
    
    updated = False
    for l in all_lich:
        if str(l['ID_Lich']) == str(id_lich):
            l.update({'MovieID': movie_id, 'TenPhim': ten_phim, 'Ngay': ngay, 'Gio': gio, 'Phong': phong})
            updated = True; break
            
    if updated:
        with open(FILE_LICH, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['ID_Lich', 'MovieID', 'TenPhim', 'Ngay', 'Gio', 'Phong']
            writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(all_lich)
        return True, "Cập nhật thành công!"
    return False, "Lỗi khi cập nhật."

def xoa_lich_chieu(id_lich):
    lichs = doc_toan_bo_lich()
    lichs = [l for l in lichs if str(l['ID_Lich']) != str(id_lich)]
    with open(FILE_LICH, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['ID_Lich', 'MovieID', 'TenPhim', 'Ngay', 'Gio', 'Phong']
        writer = csv.DictWriter(f, fieldnames=fieldnames); writer.writeheader(); writer.writerows(lichs)

def lay_lich_chieu_theo_phim(movie_id):
    return [l for l in doc_toan_bo_lich() if str(l['MovieID']) == str(movie_id)]

def tu_dong_xep_lich(so_ngay=3):
    phims = doc_danh_sach_phim()
    if not phims: return False, "Không có phim!"
    phongs = ["Phòng 01", "Phòng 02", "Phòng VIP"]
    today = datetime.now()
    count = 0; ds_new = []
    
    for i in range(so_ngay):
        curr_date = (today + timedelta(days=i)).strftime("%d/%m/%Y")
        for phong in phongs:
            curr_t = datetime.strptime(f"{curr_date} 09:00", "%d/%m/%Y %H:%M")
            limit_t = datetime.strptime(f"{curr_date} 23:00", "%d/%m/%Y %H:%M")
            while curr_t < limit_t:
                p = random.choice(phims)
                try: dur = int(''.join(filter(str.isdigit, p['ThoiLuong'])))
                except: dur = 90
                
                ds_new.append({'ID_Lich': int(time.time())+count, 'MovieID': p['ID'], 'TenPhim': p['Ten'], 'Ngay': curr_date, 'Gio': curr_t.strftime("%H:%M"), 'Phong': phong})
                count += 1; curr_t += timedelta(minutes=dur+30)
                
    file_exists = os.path.isfile(FILE_LICH)
    with open(FILE_LICH, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['ID_Lich', 'MovieID', 'TenPhim', 'Ngay', 'Gio', 'Phong']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        writer.writerows(ds_new)
    return True, f"Đã xếp {count} suất!"

# ================= 4. LOGIC VÉ & DOANH THU =================
def luu_ve(user_id, movie_id, movie_name, seats, total_price, ngay, suat, phong):
    file_exists = os.path.isfile(FILE_VE)
    with open(FILE_VE, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ['UserID', 'MovieID', 'MovieName', 'Seats', 'TotalPrice', 'Time', 'NgayChieu', 'SuatChieu', 'PhongChieu']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        writer.writerow({'UserID': user_id, 'MovieID': movie_id, 'MovieName': movie_name, 'Seats': seats, 'TotalPrice': total_price, 'Time': time.strftime("%Y-%m-%d %H:%M:%S"), 'NgayChieu': ngay, 'SuatChieu': suat, 'PhongChieu': phong})

def lay_ghe_da_dat(movie_id, ngay, suat, phong):
    booked = []
    if not os.path.exists(FILE_VE): return []
    with open(FILE_VE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (str(row['MovieID'])==str(movie_id) and row.get('NgayChieu')==ngay and row.get('SuatChieu')==suat and row.get('PhongChieu')==phong):
                booked.extend(row['Seats'].split(','))
    return booked

def doc_lich_su_ve(user_id):
    h = []
    if not os.path.exists(FILE_VE): return []
    with open(FILE_VE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if str(row['UserID']) == str(user_id): h.append(row)
    return h

def thong_ke_doanh_thu():
    t = 0
    if not os.path.exists(FILE_VE): return 0
    with open(FILE_VE, mode='r', encoding='utf-8') as f:
        for row in csv.DictReader(f): t += int(row['TotalPrice'])
    return t