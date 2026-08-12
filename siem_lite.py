import re
import sqlite3
from collections import defaultdict

# ==========================================
# 1. PERSIAPAN ATURAN & DATABASE
# ==========================================

# Kita buat pola Regex: Cari kalimat "Failed password", lalu ambil IP address di akhirnya
pola_gagal = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)")

# Kita tentukan batas maksimal login gagal (kalau > 2 kali, berarti Brute-Force / Serangan)
BATAS_GAGAL = 2

# Siapkan fungsi untuk membuat dan terhubung ke Database SQLite
def setup_database():
    # Membuat file database bernama 'ancaman.db' secara otomatis
    conn = sqlite3.connect('ancaman.db')
    cursor = conn.cursor()
    # Membuat tabel untuk menyimpan IP penyerang jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daftar_blokir (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            jumlah_gagal INTEGER
        )
    ''')
    conn.commit()
    return conn

# ==========================================
# 2. LOGIKA DETEKSI ANCAMAN UTAMA
# ==========================================

def jalankan_siem(file_log):
    print(f"[*] Menjalankan SIEM Lite... Membaca {file_log}")
    
    # Siapkan tempat penghitung IP
    penghitung_ip = defaultdict(int)
    
    # Buka database
    db_conn = setup_database()
    cursor = db_conn.cursor()

    # Buka dan baca file log baris demi baris
    with open(file_log, 'r') as file:
        for baris in file:
            # Cocokkan setiap baris dengan pola Regex kita
            kecocokan = pola_gagal.search(baris)
            
            # Jika ada yang cocok (ada teks Failed password)
            if kecocokan:
                ip_penyerang = kecocokan.group(1) # Ambil IP-nya saja
                penghitung_ip[ip_penyerang] += 1  # Tambah hitungan gagal
                
    # ==========================================
    # 3. EVALUASI DAN SIMPAN KE DATABASE
    # ==========================================
    
    print("\n[*] Hasil Analisis:")
    # Cek semua IP yang gagal tadi
    for ip, total_gagal in penghitung_ip.items():
        if total_gagal > BATAS_GAGAL:
            print(f"[!] ANCAMAN TERDETEKSI: IP {ip} mencoba brute-force ({total_gagal} kali gagal).")
            
            # Simpan IP jahat ini ke database
            cursor.execute("INSERT INTO daftar_blokir (ip_address, jumlah_gagal) VALUES (?, ?)", (ip, total_gagal))
            db_conn.commit()
            print(f"    -> Tindakan: IP {ip} berhasil disimpan ke database blokir.")
        else:
            print(f"[-] Aman: IP {ip} hanya salah ketik password ({total_gagal} kali gagal).")

    db_conn.close()
    print("\n[*] Pemindaian selesai!")

# ==========================================
# 4. JALANKAN PROGRAM
# ==========================================
if __name__ == "__main__":
    # Panggil fungsinya dan masukkan nama file dummy kita
    jalankan_siem('auth_besar.log')