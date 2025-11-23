from django.core.management.base import BaseCommand
from core.models import Sporcu, Kulup
import pandas as pd
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Excel dosyasından toplu oyuncu yükler'

    def handle(self, *args, **kwargs):
        self.stdout.write("📊 Excel Yükleyici Başlatılıyor...")

        # 1. Dosyayı Bul
        dosya_yolu = os.path.join(settings.BASE_DIR, 'oyuncular.xlsx')
        
        if not os.path.exists(dosya_yolu):
            self.stdout.write(self.style.ERROR("❌ Hata: 'oyuncular.xlsx' dosyası proje klasöründe bulunamadı!"))
            return

        # 2. Excel'i Oku
        try:
            df = pd.read_excel(dosya_yolu)
            self.stdout.write(f"📄 Toplam {len(df)} satır veri bulundu. İşleniyor...")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Excel okuma hatası: {e}"))
            return

        # 3. Mevki Haritası (Excel'deki Türkçeyi Kodlara Çevir)
        mevki_map = {
            'Pasör': 'PASOR',
            'Pasör Çaprazı': 'PASOR_CAPRAZI',
            'Smaçör': 'SMACOR',
            'Orta Oyuncu': 'ORTA_OYUNCU',
            'Libero': 'LIBERO'
        }

        basarili = 0
        
        # 4. Satır Satır İşle
        for index, row in df.iterrows():
            try:
                isim = str(row['Ad Soyad']).strip()
                kulup_adi = str(row['Kulüp']).strip()
                mevki_adi = str(row['Mevki']).strip()
                boy = row['Boy']

                # Boş satırsa atla
                if not isim or isim == 'nan':
                    continue

                # Kulübü Bul veya Oluştur
                kulup, _ = Kulup.objects.get_or_create(
                    isim=kulup_adi,
                    defaults={'sehir': 'Bilinmiyor'}
                )

                # Mevki Kodunu Bul
                mevki_kodu = mevki_map.get(mevki_adi, None)

                # Sporcuyu Kaydet (Varsa güncelle, yoksa oluştur)
                obj, created = Sporcu.objects.update_or_create(
                    isim=isim,
                    defaults={
                        'kulup': kulup,
                        'mevki': mevki_kodu,
                        'boy': int(boy) if pd.notna(boy) else None
                    }
                )

                durum = "Oluşturuldu" if created else "Güncellendi"
                # self.stdout.write(f"✅ {isim} -> {durum}")
                basarili += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Satır {index+2} hatası: {e}"))

        self.stdout.write(self.style.SUCCESS(f"🎉 İŞLEM TAMAM! Toplam {basarili} sporcu sisteme yüklendi."))