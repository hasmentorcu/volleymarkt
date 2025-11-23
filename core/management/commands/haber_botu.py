from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Haber
import requests
import feedparser # RSS okumak için gerekli kütüphane
import datetime
from time import mktime

class Command(BaseCommand):
    help = 'RSS üzerinden garantili haber çeker'

    def handle(self, *args, **kwargs):
        self.stdout.write("📡 RSS Haber Botu Başlatılıyor...")
        
        # TRT Spor Voleybol RSS Adresi (Genellikle en güncel ve temiz kaynaktır)
        # Alternatif kaynaklar da eklenebilir.
        rss_url = "https://www.trtspor.com.tr/rss/voleybol.rss"

        try:
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                self.stdout.write(self.style.WARNING("⚠️ RSS kaynağında haber bulunamadı veya erişim sorunu var."))
                # Yedek Kaynak (Hürriyet Voleybol RSS)
                self.stdout.write("🔄 Yedek kaynağa geçiliyor (Hürriyet)...")
                feed = feedparser.parse("https://www.hurriyet.com.tr/rss/spor/voleybol")

            count = 0
            for entry in feed.entries[:10]: # Son 10 haber
                try:
                    baslik = entry.title
                    link = entry.link
                    ozet = entry.description if 'description' in entry else baslik
                    
                    # HTML etiketlerini temizle (RSS bazen <p> etiketiyle gelir)
                    ozet = self.clean_html(ozet)

                    # Haber zaten var mı?
                    if Haber.objects.filter(baslik=baslik).exists():
                        self.stdout.write(f"⏩ Zaten var: {baslik[:30]}...")
                        continue

                    # Resim Bulma (RSS'de genelde 'media_content' veya 'links' içindedir)
                    img_url = None
                    if 'media_content' in entry:
                        img_url = entry.media_content[0]['url']
                    elif 'links' in entry:
                        for l in entry.links:
                            if l['type'].startswith('image'):
                                img_url = l['href']
                                break
                    
                    # Eğer RSS'de resim yoksa, haber linkine gidip meta etiketinden çekmeye çalışalım
                    if not img_url:
                        img_url = self.get_image_from_meta(link)

                    # Kaydet
                    yeni_haber = Haber(
                        baslik=baslik,
                        ozet=ozet[:200] + "...",
                        icerik=f"{ozet}\n\nDevamı için: {link}", # RSS tam metin vermez, link veririz
                        kategori='Mac' if 'maç' in baslik.lower() or 'set' in baslik.lower() else 'Ozel',
                        manset_mi=True
                    )

                    # Resmi İndir
                    if img_url:
                        headers = {"User-Agent": "Mozilla/5.0"}
                        img_resp = requests.get(img_url, headers=headers, stream=True, timeout=10)
                        if img_resp.status_code == 200:
                            file_name = f"haber_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{count}.jpg"
                            yeni_haber.resim.save(file_name, ContentFile(img_resp.content), save=False)
                    
                    yeni_haber.save()
                    self.stdout.write(self.style.SUCCESS(f"✅ Eklendi: {baslik[:30]}..."))
                    count += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Hata (Haber): {e}"))
                    continue

            self.stdout.write(self.style.SUCCESS(f"🎉 Toplam {count} yeni haber eklendi."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Genel Hata: {e}"))

    def clean_html(self, raw_html):
        """Basit HTML temizleyici"""
        import re
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.strip()

    def get_image_from_meta(self, url):
        """Haber sayfasına gidip og:image etiketini çeker"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=5)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.content, 'html.parser')
            meta_img = soup.find("meta", property="og:image")
            if meta_img:
                return meta_img["content"]
            return None
        except:
            return None