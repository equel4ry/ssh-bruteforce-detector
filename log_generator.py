import random
from datetime import datetime, timedelta

def generate_realistic_logs(filename="auth_besar.log", num_lines=10000):
    print(f"[*] Sedang membuat {num_lines} baris log realistis...")
    
    users = ["root", "admin", "guest", "ubuntu", "oracle", "postgres"]
    # Bikin beberapa IP normal (karyawan/user biasa)
    normal_ips = [f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}" for _ in range(50)]
    
    # Bikin IP Penyerang (hacker)
    attacker_ips = ["192.168.1.100", "10.0.0.55", "172.16.0.4", "203.0.113.42", "45.33.32.156"]
    
    start_time = datetime(2026, 8, 12, 8, 0, 0)
    
    with open(filename, "w") as f:
        for _ in range(num_lines):
            # Waktu maju beberapa detik setiap baris log
            start_time += timedelta(seconds=random.randint(1, 10))
            time_str = start_time.strftime("%b %d %H:%M:%S")
            pid = random.randint(1000, 9999)
            
            # 85% aktivitas normal, 15% aktivitas serangan (brute-force)
            if random.random() > 0.15:
                ip = random.choice(normal_ips)
                user = random.choice(users)
                # User normal kadang berhasil, kadang salah ketik password
                status = random.choices(["Accepted password", "Failed password"], weights=[0.8, 0.2])[0]
            else:
                ip = random.choice(attacker_ips)
                user = "root"
                status = "Failed password" # Hacker biasanya gagal terus saat brute-force
                
            log_line = f"{time_str} server sshd[{pid}]: {status} for {user} from {ip} port {random.randint(30000, 65000)} ssh2\n"
            f.write(log_line)
            
    print(f"[+] Selesai! File '{filename}' berhasil dibuat.")

if __name__ == "__main__":
    # Ini akan membuat file log berisi 10.000 baris!
    generate_realistic_logs()