import time
import requests

def yenile_token():
    url = "https://orneklink.com/token_yenile"  # BURAYA kendi token yenileme linkini yaz
    while True:
        try:
            response = requests.get(url)
            print("Token yenilendi:", response.status_code)
        except Exception as e:
            print("Hata:", e)
        time.sleep(3600)  # 1 saatte bir çalışır

if __name__ == "__main__":
    yenile_token()
