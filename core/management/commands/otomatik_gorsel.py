from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Sporcu, Kulup
import requests

class Command(BaseCommand):
    help = 'Büyük harf ve kimlik sorununu çözen final bot'

    def handle(self, *args, **kwargs):
        self.stdout.write("📡 DÜZELTİCİ MOD Başlatılıyor...")

        sporcular = Sporcu.objects.all()
        self.stdout.write(f"--- {len(sporcular)} Sporcu taranıyor ---")

        for sporcu in sporcular:
            # 1. İSMİ DÜZELT (Hande BALADIN -> Hande Baladın)
            # Python'un title() fonksiyonu Türkçe karakterlerde bazen şaşırır ama Wikipedia bunu tolere eder.
            # "İLKİN" -> "İlkin" gibi basit çeviri yapıyoruz.
            aranacak_isim = sporcu.isim.title() 
            
            self.stdout.write(f"🔍 Aranıyor: {aranacak_isim} (Orijinal: {sporcu.isim})")
            
            dogru_baslik = self.wikipedia_search(aranacak_isim)
            
            if dogru_baslik:
                img_url = self.get_wiki_image(dogru_baslik)
                if img_url:
                    # Dosya adını da düzgün yapalım
                    dosya_adi = f"{aranacak_isim.replace(' ', '_')}.jpg"
                    self.save_image(sporcu.profil_fotografi, img_url, dosya_adi)
                    self.stdout.write(self.style.SUCCESS(f"✅ {sporcu.isim} -> FOTOĞRAF YÜKLENDİ"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ {sporcu.isim}: Sayfa bulundu ({dogru_baslik}) ama görsel yok."))
            else:
                # Bir de "(voleybolcu)" ekleyerek şansımızı deneyelim
                dogru_baslik = self.wikipedia_search(f"{aranacak_isim} (voleybolcu)")
                if dogru_baslik:
                     img_url = self.get_wiki_image(dogru_baslik)
                     if img_url:
                        self.save_image(sporcu.profil_fotografi, img_url, f"{aranacak_isim}.jpg")
                        self.stdout.write(self.style.SUCCESS(f"✅ {sporcu.isim} -> İkinci denemede bulundu!"))
                     else:
                        self.stdout.write(self.style.WARNING(f"⚠️ {sporcu.isim}: İkinci denemede görsel yok."))
                else:
                    self.stdout.write(self.style.ERROR(f"❌ {sporcu.isim}: Bulunamadı."))

    def wikipedia_search(self, query):
        """Wikipedia'da arama yap (HEADER EKLENDİ!)"""
        url = "https://tr.wikipedia.org/w/api.php"
        # Wikipedia Botları engellememesi için User-Agent ŞARTTIR
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VolleyBot/1.0"}
        
        params = {
            "action": "opensearch",
            "search": query,
            "limit": 1,
            "namespace": 0,
            "format": "json"
        }
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            data = r.json()
            if len(data) > 1 and len(data[1]) > 0:
                return data[1][0] # En iyi eşleşen başlığı döndür
            return None
        except Exception as e:
            # Hata varsa görelim
            print(f"Bağlantı Hatası: {e}")
            return None

    def get_wiki_image(self, title):
        url = "https://tr.wikipedia.org/w/api.php"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VolleyBot/1.0"}
        params = {
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "format": "json",
            "pithumbsize": 600,
            "origin": "*"
        }
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            data = r.json()
            pages = data.get("query", {}).get("pages", {})
            for pid, pdata in pages.items():
                if pid == "-1": return None
                if "thumbnail" in pdata:
                    return pdata["thumbnail"]["source"]
            return None
        except:
            return None

    def save_image(self, field, url, filename):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, stream=True)
            if r.status_code == 200:
                field.save(filename, ContentFile(r.content), save=True)
        except:
            pass