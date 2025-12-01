# data.py
import csv
import os

PHIM_CSV = "movies.csv"
VE_CSV = "ve.csv"


def load_phim():
    """Đọc danh sách phim từ phim.csv"""
    movies = []
    with open(PHIM_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append(row)
    return movies


def load_ve():
    """Đọc danh sách vé đã đặt"""
    if not os.path.exists(VE_CSV):
        return []

    tickets = []
    with open(VE_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickets.append(row)
    return tickets


def ghe_da_dat(id_phim, suat_chieu):
    """Lấy danh sách ghế đã đặt của phim + suất"""
    tickets = load_ve()
    return [t["ghe"] for t in tickets if t["id_phim"] == id_phim and t["suat"] == suat_chieu]


def luu_ve(id_phim, ten_phim, suat, ghe, gia):
    """Lưu vé mới xuống CSV"""
    file_exists = os.path.exists(VE_CSV)

    with open(VE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["id_phim", "ten_phim", "suat", "ghe", "gia"])

        writer.writerow([id_phim, ten_phim, suat, ghe, gia])
