from django.core.management.base import BaseCommand
from core.models import Mac, Kulup
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Command(BaseCommand):
    help = 'Gelecek maç fikstürünü çeker'

    def handle(self, *args, **kwargs):
        self.stdout.write("📅 Fikstür Botu Başlatılıyor...")

        # Kaynak: TRT Spor Voleybol Fikstür Sayfası (Genellikle en temiz HTML buradadır)
        # Alternatif olarak voleybol federasyonu sitesi de kullanılabilir ama orası çok değişkendir.
        URL = "https://www.trtspor.com.tr/voleybol/fikstur"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        try:
            response = requests.get(URL, headers=headers, timeout=10)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR("❌ Fikstür kaynağına ulaşılamadı."))
                return

            soup = BeautifulSoup(response.content, "html.parser")
            
            # TRT Spor Fikstür Tablosunu Bul
            mac_satirlari = soup.select(".fixture-table tr")
            
            if not mac_satirlari:
                # Alternatif yapı (Bazen class isimleri değişir)
                mac_satirlari = soup.select("table tr")

            count = 0
            for satir in mac_satirlari:
                cols = satir.find_all("td")
                if len(cols) < 3: continue

                try:
                    # Verileri Ayıkla
                    # Genelde yapı: [Tarih] [Ev Sahibi] [Skor/Saat] [Deplasman]
                    tarih_str = cols[0].get_text(strip=True)
                    ev_sahibi_adi = cols[1].get_text(strip=True)
                    # Skor veya Saat (Oynanmamışsa saat yazar: 14:00, Oynanmışsa: 3-1)
                    durum_str = cols[2].get_text(strip=True) 
                    deplasman_adi = cols[3].get_text(strip=True)

                    # Tarihi Formatla (Örn: 24.11.2025 14:00)
                    # Bu kısım siteden siteye değişir, basit bir parser yazıyoruz:
                    try:
                        # Sadece gün/ay varsa yılı biz ekleyelim
                        if len(tarih_str) <= 5: 
                            yil = datetime.now().year
                            tarih_str = f"{tarih_str}.{yil}"
                        
                        # Saat bilgisi 'durum_str' içindeyse birleştir
                        if ":" in durum_str and "-" not in durum_str:
                            tam_tarih_str = f"{tarih_str} {durum_str}"
                            mac_tarihi = datetime.strptime(tam_tarih_str, "%d.%m.%Y %H:%M")
                            skor = "-"
                            biten_mac = False
                        else:
                            # Maç bitmiş olabilir veya saat belli değildir
                            tam_tarih_str = f"{tarih_str} 00:00"
                            mac_tarihi = datetime.strptime(tam_tarih_str, "%d.%m.%Y %H:%M")
                            skor = durum_str if "-" in durum_str else "-"
                            biten_mac = True if "-" in durum_str else False

                    except:
                        # Tarih formatı tutmazsa bugünün tarihini at (Hata vermesin)
                        mac_tarihi = datetime.now()
                        skor = "-"
                        biten_mac = False

                    # Kulüpleri Bul/Oluştur
                    ev_sahibi, _ = Kulup.objects.get_or_create(isim=self.temizle(ev_sahibi_adi))
                    deplasman, _ = Kulup.objects.get_or_create(isim=self.temizle(deplasman_adi))

                    # Maçı Kaydet (Varsa güncelle)
                    mac, created = Mac.objects.update_or_create(
                        ev_sahibi=ev_sahibi,
                        deplasman=deplasman,
                        tarih__date=mac_tarihi.date(), # Aynı gün aynı takımların maçı varsa onu güncelle
                        defaults={
                            'tarih': mac_tarihi,
                            'skor': skor,
                            'tamamlandi': biten_mac
                        }
                    )

                    if created:
                        self.stdout.write(f"➕ Yeni Maç: {ev_sahibi} vs {deplasman}")
                    count += 1

                except Exception as e:
                    continue

            self.stdout.write(self.style.SUCCESS(f"🎉 Fikstür Güncellendi: {count} maç işlendi."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Hata: {e}"))

    def temizle(self, isim):
        """Takım isimlerindeki gereksiz boşlukları ve ekleri siler"""
        isim = isim.replace("Voleybol", "").strip()
        return isim