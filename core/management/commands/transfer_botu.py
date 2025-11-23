from django.core.management.base import BaseCommand
from core.models import Sporcu, Kulup, Transfer
import requests
from bs4 import BeautifulSoup
import re

class Command(BaseCommand):
    help = 'Wikipedia transfer geçmişini Regex (Kalıp Arama) ile çeker'

    def handle(self, *args, **kwargs):
        sporcular = Sporcu.objects.all()
        self.stdout.write(f"📡 {len(sporcular)} sporcu için Hassas Tarama başlatılıyor...")

        for sporcu in sporcular:
            # Temizlik: Önce eski transferleri sil (Yineleme olmasın)
            sporcu.transferler.all().delete()
            self.scrape_player_history(sporcu)

    def scrape_player_history(self, sporcu):
        wiki_name = sporcu.isim.replace(" ", "_")
        url = f"https://tr.wikipedia.org/wiki/{wiki_name}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200: return

            soup = BeautifulSoup(response.content, "html.parser")
            infobox = soup.find("table", {"class": "infobox"})
            
            if not infobox:
                self.stdout.write(self.style.WARNING(f"⚠️ {sporcu.isim}: Bilgi kutusu yok."))
                return

            # Tüm tablo satırlarını metin olarak al
            text_data = infobox.get_text(separator="\n")
            lines = text_data.split("\n")
            
            # Transfer Kalıbını Tanımla (Regex)
            # Örn: "2011-2014" veya "2023-" veya "2015" gibi başlayan satırlar
            # \d{4} = 4 haneli rakam
            regex_pattern = re.compile(r"^(\d{4}[-–—]?\d{0,4})\s+(.*)")

            transfer_count = 0
            yakalanan_bolge = False # "Profesyonel kariyer" başlığından sonrasını okumak için

            for line in lines:
                line = line.strip()
                
                # Başlangıç noktasını bul
                if "kariyer" in line.lower() or "oynadığı takımlar" in line.lower():
                    yakalanan_bolge = True
                    continue
                
                # Milli takım kısmına geldiysek dur
                if "millî" in line.lower() or "milli" in line.lower():
                    yakalanan_bolge = False
                    break

                if yakalanan_bolge and len(line) > 5:
                    # Satır bizim kalıba uyuyor mu? (Yıl ile mi başlıyor?)
                    match = regex_pattern.match(line)
                    if match:
                        sezon = match.group(1).strip()
                        takim = match.group(2).strip()

                        # Bazı temizlikler
                        takim = re.sub(r'\[.*?\]', '', takim) # [1] gibi notları sil
                        takim = takim.replace("→", "").strip()

                        # Takım ismi çok kısaysa veya sayıysa (maç sayısıdır) atla
                        if len(takim) < 3 or takim.isdigit():
                            continue

                        self.save_transfer(sporcu, sezon, takim)
                        transfer_count += 1

            if transfer_count > 0:
                self.stdout.write(self.style.SUCCESS(f"✅ {sporcu.isim}: {transfer_count} transfer bulundu."))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ {sporcu.isim}: Hiç transfer bulunamadı (Format farklı olabilir)."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Hata ({sporcu.isim}): {e}"))

    def save_transfer(self, sporcu, sezon, takim_adi):
        # Kiralık mı?
        tip = 'Bonservis'
        if 'kiralık' in takim_adi.lower():
            tip = 'Kiralık'
            takim_adi = takim_adi.replace('(kiralık)', '').replace('kiralık', '').replace('(', '').replace(')', '').strip()

        kulup, _ = Kulup.objects.get_or_create(isim=takim_adi, defaults={'sehir': 'Bilinmiyor'})
        
        Transfer.objects.create(
            sporcu=sporcu,
            sezon=sezon,
            yeni_kulup=kulup,
            tip=tip
        )