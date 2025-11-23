from django.core.management.base import BaseCommand
from core.models import Sporcu, Kulup
import requests
from bs4 import BeautifulSoup
import re

class Command(BaseCommand):
    help = 'Wikipedia takım sayfalarından esnek arama ile kadroları çeker'

    def handle(self, *args, **kwargs):
        self.stdout.write("📡 ESNEK KADRO AVCISI Başlatılıyor...")

        # HEDEF LİSTESİ
        hedefler = [
            ("VakıfBank", "https://tr.wikipedia.org/wiki/Vak%C4%B1fBank_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
            ("Fenerbahçe Opet", "https://tr.wikipedia.org/wiki/Fenerbah%C3%A7e_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
            ("Eczacıbaşı Dynavit", "https://tr.wikipedia.org/wiki/Eczac%C4%B1ba%C5%9F%C4%B1_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
            ("Galatasaray Daikin", "https://tr.wikipedia.org/wiki/Galatasaray_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
            ("THY", "https://tr.wikipedia.org/wiki/T%C3%BCrk_Hava_Yollar%C4%B1_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
            ("Kuzeyboru", "https://tr.wikipedia.org/wiki/Kuzeyboru_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
             ("Sarıyer Bld", "https://tr.wikipedia.org/wiki/Sar%C4%B1yer_Belediyespor_(kad%C4%B1n_voleybol_tak%C4%B1m%C4%B1)"),
        ]

        for takim_adi, url in hedefler:
            self.stdout.write(f"\n🌍 {takim_adi} taranıyor...")
            self.kadro_cek(takim_adi, url)

    def kadro_cek(self, takim_adi, url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            
            kulup, _ = Kulup.objects.get_or_create(isim=takim_adi, defaults={'sehir': 'İstanbul'})

            # Tüm tabloları çek
            tablolar = soup.find_all("table") # Sadece .wikitable değil, hepsine bak
            
            hedef_tablo = None
            sutun_map = {} 

            # Eş anlamlı kelimeler sözlüğü
            anahtar_kelimeler = {
                'isim': ['adı', 'ad', 'oyuncu', 'sporcu', 'isim', 'ad soyad'],
                'mevki': ['mevki', 'pozisyon', 'görev', 'rol'],
                'boy': ['boy', 'boyu']
            }

            for tablo in tablolar:
                baslik_satiri = tablo.find("tr")
                if not baslik_satiri: continue
                
                # Başlıkları temizle ve küçük harfe çevir
                basliklar = [th.get_text(strip=True).lower() for th in baslik_satiri.find_all(["th", "td"])]
                
                # Puan durumu tablosunu yanlışlıkla almamak için "O" (Oynanan) veya "P" (Puan) varsa atla
                if "p" in basliklar and "o" in basliklar and "av" in basliklar:
                    continue

                # Tablo içinde İSİM ve (MEVKİ veya BOY) geçiyor mu?
                isim_var = any(k in b for b in basliklar for k in anahtar_kelimeler['isim'])
                mevki_var = any(k in b for b in basliklar for k in anahtar_kelimeler['mevki'])
                
                if isim_var and mevki_var:
                    hedef_tablo = tablo
                    # Sütun yerlerini haritala
                    for i, b in enumerate(basliklar):
                        if any(k in b for k in anahtar_kelimeler['isim']): sutun_map['isim'] = i
                        elif any(k in b for k in anahtar_kelimeler['mevki']): sutun_map['mevki'] = i
                        elif any(k in b for k in anahtar_kelimeler['boy']): sutun_map['boy'] = i
                    break
            
            if not hedef_tablo:
                self.stdout.write(self.style.WARNING(f"⚠️ {takim_adi}: Uygun tablo bulunamadı."))
                return

            self.stdout.write(f"   -> Tablo bulundu! Oyuncular işleniyor...")

            # Satırları İşle
            satirlar = hedef_tablo.find_all("tr")[1:] 
            count = 0

            for satir in satirlar:
                cols = satir.find_all(["td", "th"])
                
                # İsim sütunu kaçıncı sıradaysa o kadar sütun var mı kontrol et
                gerekli_uzunluk = sutun_map.get('isim', 1) + 1
                if len(cols) < gerekli_uzunluk: continue

                try:
                    # İsim
                    idx_isim = sutun_map.get('isim', 1)
                    # Bazen isim içinde bayrak resmi olur, sadece metni al
                    isim = cols[idx_isim].get_text(strip=True)
                    isim = re.sub(r'\[.*?\]', '', isim).strip() # [1] sil
                    isim = re.sub(r'^\d+\s*', '', isim).strip() # Baştaki forma numarasını sil (varsa)

                    if len(isim) < 3: continue # Çok kısaysa isim değildir

                    # Mevki
                    mevki_raw = "Bilinmiyor"
                    if 'mevki' in sutun_map and len(cols) > sutun_map['mevki']:
                        mevki_raw = cols[sutun_map['mevki']].get_text(strip=True)
                    
                    mevki_kod = self.mevki_bul(mevki_raw)

                    # Boy
                    boy = None
                    if 'boy' in sutun_map and len(cols) > sutun_map['boy']:
                        boy_str = cols[sutun_map['boy']].get_text(strip=True)
                        boy_str = re.sub(r'[^\d,\.]', '', boy_str).replace(',', '.') # Sadece sayı ve nokta kalsın
                        try:
                            boy_float = float(boy_str)
                            if 1.50 < boy_float < 2.50: # Metre ise (1.90)
                                boy = int(boy_float * 100)
                            elif 150 < boy_float < 250: # CM ise (190)
                                boy = int(boy_float)
                        except:
                            boy = None

                    # Kaydet
                    sporcu, created = Sporcu.objects.update_or_create(
                        isim=isim,
                        defaults={
                            'kulup': kulup,
                            'mevki': mevki_kod,
                            'boy': boy
                        }
                    )
                    count += 1

                except Exception as e:
                    continue

            self.stdout.write(self.style.SUCCESS(f"✅ {takim_adi}: {count} oyuncu eklendi."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Hata: {e}"))

    def mevki_bul(self, text):
        text = text.lower()
        if "çapraz" in text: return "PASOR_CAPRAZI"
        if "pasör" in text: return "PASOR"
        if "smaçör" in text: return "SMACOR"
        if "orta" in text or "blokör" in text: return "ORTA_OYUNCU"
        if "libero" in text: return "LIBERO"
        return "SMACOR" # Varsayılan