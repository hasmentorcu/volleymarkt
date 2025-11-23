from django.core.management.base import BaseCommand
from django.core.management import call_command
import time

class Command(BaseCommand):
    help = 'Tüm botları sırasıyla çalıştıran Ana Bot'

    def handle(self, *args, **kwargs):
        baslangic = time.time()
        self.stdout.write(self.style.SUCCESS("🚀 TAM GÜNCELLEME BAŞLATILIYOR..."))
        self.stdout.write("--------------------------------------------------")

        # 1. ADIM: KADROLARI ÇEK (Yeni oyuncular gelsin)
        self.stdout.write(self.style.WARNING("1️⃣  KADRO AVCISI Çalışıyor..."))
        call_command('kadro_botu')
        self.stdout.write("--------------------------------------------------")

        # 2. ADIM: FOTOĞRAFLARI BUL (Yeni gelenlerin fotosu yok, bulalım)
        self.stdout.write(self.style.WARNING("2️⃣  GÖRSEL AVCISI Çalışıyor..."))
        call_command('otomatik_gorsel')
        self.stdout.write("--------------------------------------------------")

        # 3. ADIM: TRANSFER GEÇMİŞİNİ ÇEK
        self.stdout.write(self.style.WARNING("3️⃣  TRANSFER BOTU Çalışıyor..."))
        call_command('transfer_botu')
        self.stdout.write("--------------------------------------------------")

        # 4. ADIM: LİG PUAN DURUMUNU GÜNCELLE
        self.stdout.write(self.style.WARNING("4️⃣  LİG BOTU Çalışıyor..."))
        call_command('guncelle') # veya 'siralama_duzelt' de ekleyebilirsin
        self.stdout.write("--------------------------------------------------")

        bitis = time.time()
        sure = round(bitis - baslangic, 2)
        
        self.stdout.write(self.style.SUCCESS(f"🎉 TÜM İŞLEMLER TAMAMLANDI! (Süre: {sure} saniye)"))