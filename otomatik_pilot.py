import os
import time
import datetime

def calistir():
    while True:
        simdi = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n⏰ Saat {simdi}: Güncelleme Başlıyor...")
        
        # Master Botu Çalıştır
        os.system("python manage.py tam_guncelleme")
        
        print(f"✅ Bitti. Bir sonraki güncelleme 1 saat sonra.")
        
        # 3600 Saniye (1 Saat) Bekle
        time.sleep(3600) 

if __name__ == "__main__":
    print("✈️ OTOMATİK PİLOT DEVREDE (Durdurmak için pencereyi kapatın)")
    calistir()

    import os
import time
import datetime
import sys

def calistir():
    python_exe = sys.executable 
    print("⏱️ OTOMATİK FİKSTÜR VE GÜNCELLEME SİSTEMİ DEVREDE")
    print(f"📂 Çalışma Dizini: {os.getcwd()}")
    print("---------------------------------------------------")
    
    while True:
        simdi = datetime.datetime.now()
        saat_str = simdi.strftime("%H:%M:%S")
        
        print(f"\n🔄 [{saat_str}] Güncelleme Döngüsü Başladı...")

        # 1. Fikstürü Çek (Maç saatleri, yeni maçlar)
        print("   >> 📅 Fikstür taranıyor...")
        os.system(f'"{python_exe}" manage.py fikstur_botu')

        # 2. Haberleri Çek (Sıcak gelişmeler)
        print("   >> 📰 Haberler taranıyor...")
        os.system(f'"{python_exe}" manage.py haber_botu')

        # 3. Puan Durumunu Güncelle (Maç bittiyse puan değişir)
        # Bunu her seferinde yapmak yerine saat başı yapabiliriz ama şimdilik hepsini yapsın.
        print("   >> 🏆 Puan durumu taranıyor...")
        os.system(f'"{python_exe}" manage.py guncelle')

        print(f"✅ [{saat_str}] Döngü tamamlandı. 15 dakika beklenecek.")
        print("---------------------------------------------------")
        
        # 15 Dakika Bekle (15 x 60 = 900 Saniye)
        time.sleep(900) 

if __name__ == "__main__":
    try:
        calistir()
    except KeyboardInterrupt:
        print("\n🛑 Sistem kullanıcı tarafından durduruldu.")