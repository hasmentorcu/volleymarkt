from django.core.management.base import BaseCommand
from core.models import Kulup, PuanDurumu
import requests
from bs4 import BeautifulSoup
import re

class Command(BaseCommand):
    help = 'Puan durumunu çeker (Wikipedia başarısız olursa yedek veriyi kullanır)'

    def handle(self, *args, **kwargs):
        self.stdout.write("📡 Veri güncelleme işlemi başlatılıyor...")

        # 1. YÖNTEM: Wikipedia'dan Canlı Çekme Denemesi
        basari = self.scrape_wikipedia()

        # 2. YÖNTEM: Eğer canlı çekemezse, site boş kalmasın diye yedek veriyi yükle
        if not basari:
            self.stdout.write(self.style.WARNING("⚠️ Canlı veri çekilemedi. Yedek (Manuel) veri yükleniyor..."))
            self.load_backup_data()
        else:
            self.stdout.write(self.style.SUCCESS("🎉 İşlem canlı veri ile tamamlandı."))

    def scrape_wikipedia(self):
        """Wikipedia'dan veri çekmeye çalışır."""
        URL = "https://tr.wikipedia.org/wiki/2024-25_Sultanlar_Ligi"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"}
        
        try:
            self.stdout.write(f"🌐 {URL} adresine bağlanılıyor...")
            response = requests.get(URL, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return False

            soup = BeautifulSoup(response.content, "html.parser")
            tablolar = soup.select("table.wikitable")
            
            if not tablolar:
                return False

            hedef_tablo = None
            sutun_indeksleri = {}

            # Doğru tabloyu bulma algoritması
            for tablo in tablolar:
                baslik_satiri = tablo.find("tr")
                if not baslik_satiri: continue
                
                basliklar = [th.get_text(strip=True) for th in baslik_satiri.find_all(["th", "td"])]
                
                if any("Takım" in b for b in basliklar) and any(b in ["P", "Puan"] for b in basliklar):
                    hedef_tablo = tablo
                    for i, baslik in enumerate(basliklar):
                        b = baslik.replace('.', '').strip()
                        if "Takım" in b: sutun_indeksleri['takim'] = i
                        elif b == "O": sutun_indeksleri['oynanan'] = i
                        elif b == "G": sutun_indeksleri['galibiyet'] = i
                        elif b == "M": sutun_indeksleri['maglubiyet'] = i
                        elif b in ["P", "Puan"]: sutun_indeksleri['puan'] = i
                    break
            
            if not hedef_tablo or 'puan' not in sutun_indeksleri:
                return False

            satirlar = hedef_tablo.find_all("tr")[1:]
            count = 0
            
            for satir in satirlar:
                hucreler = satir.find_all(["td", "th"])
                if len(hucreler) < len(sutun_indeksleri): continue

                try:
                    idx_takim = sutun_indeksleri.get('takim')
                    ham_isim = hucreler[idx_takim].get_text(strip=True)
                    isim = re.sub(r'^\d+\s*', '', ham_isim).split('[')[0].strip()
                    
                    oynanan = hucreler[sutun_indeksleri['oynanan']].get_text(strip=True)
                    galibiyet = hucreler[sutun_indeksleri['galibiyet']].get_text(strip=True)
                    maglubiyet = hucreler[sutun_indeksleri['maglubiyet']].get_text(strip=True)
                    puan = hucreler[sutun_indeksleri['puan']].get_text(strip=True)

                    self.kaydet(isim, oynanan, galibiyet, maglubiyet, puan)
                    count += 1
                except:
                    continue
            
            return count > 0

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Hata: {e}"))
            return False

    def load_backup_data(self):
        """Wikipedia çalışmazsa bu veriler yüklenir."""
        yedek_liste = [
            {"isim": "Eczacıbaşı Dynavit", "O": 9, "G": 9, "M": 0, "P": 27},
            {"isim": "Fenerbahçe Opet", "O": 9, "G": 8, "M": 1, "P": 24},
            {"isim": "VakıfBank", "O": 9, "G": 8, "M": 1, "P": 23},
            {"isim": "THY", "O": 9, "G": 6, "M": 3, "P": 18},
            {"isim": "Galatasaray Daikin", "O": 9, "G": 6, "M": 3, "P": 17},
            {"isim": "Kuzeyboru", "O": 9, "G": 5, "M": 4, "P": 14},
            {"isim": "Muratpaşa Bld.", "O": 9, "G": 4, "M": 5, "P": 12},
            {"isim": "Aydın B.Şehir Bld.", "O": 9, "G": 3, "M": 6, "P": 10},
            {"isim": "Nilüfer Bld.", "O": 9, "G": 3, "M": 6, "P": 9},
            {"isim": "Beşiktaş Ayos", "O": 9, "G": 2, "M": 7, "P": 7},
            {"isim": "Sarıyer Bld.", "O": 9, "G": 0, "M": 9, "P": 1}
        ]
        
        for veri in yedek_liste:
            self.kaydet(veri["isim"], veri["O"], veri["G"], veri["M"], veri["P"])
            self.stdout.write(f"--> {veri['isim']} yüklendi.")

    def kaydet(self, isim, o, g, m, p):
        kulup, _ = Kulup.objects.get_or_create(isim=isim, defaults={'sehir': 'Türkiye'})
        # Virgül varsa noktaya çevir (Örn: 12,5 -> 12.5)
        p_str = str(p).replace(',', '.')
        
        PuanDurumu.objects.update_or_create(
            kulup=kulup,
            defaults={
                'oynanan': int(o),
                'galibiyet': int(g),
                'maglubiyet': int(m),
                'puan': int(float(p_str))
            }
        )