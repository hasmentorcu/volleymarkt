import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from core.models import Sporcu, Kulup
import unicodedata

class Command(BaseCommand):
    help = 'Klasördeki resimleri isimlerine göre eşleştirip yükler'

    def handle(self, *args, **kwargs):
        # 1. Yolları Tanımla
        base_dir = settings.BASE_DIR
        depo_dir = os.path.join(base_dir, 'resim_deposu')
        
        sporcu_dir = os.path.join(depo_dir, 'sporcular')
        kulup_dir = os.path.join(depo_dir, 'kulupler')

        if not os.path.exists(depo_dir):
            self.stdout.write(self.style.ERROR("❌ 'resim_deposu' klasörü bulunamadı! Lütfen oluşturun."))
            return

        self.stdout.write("📸 Görsel tarama başlatılıyor...")

        # 2. Kulüpleri Eşleştir
        if os.path.exists(kulup_dir):
            self.eslestir_ve_yukle(Kulup, kulup_dir, 'logo')
        
        # 3. Sporcuları Eşleştir
        if os.path.exists(sporcu_dir):
            self.eslestir_ve_yukle(Sporcu, sporcu_dir, 'profil_fotografi')

    def eslestir_ve_yukle(self, model, klasor_yolu, alan_adi):
        dosyalar = os.listdir(klasor_yolu)
        veritabanindaki_kayitlar = model.objects.all()
        
        sayac = 0
        
        for kayit in veritabanindaki_kayitlar:
            # Kaydın normalize edilmiş ismini bul (Zehra Güneş -> zehragunes)
            hedef_isim = self.normalize_name(kayit.isim)
            
            for dosya_adi in dosyalar:
                # Dosya ismini normalize et (zehra_gunes.jpg -> zehragunes)
                dosya_kok = os.path.splitext(dosya_adi)[0] # Uzantıyı at
                kaynak_isim = self.normalize_name(dosya_kok)
                
                # Eşleşme var mı?
                if hedef_isim in kaynak_isim or kaynak_isim in hedef_isim:
                    # Dosyayı Aç ve Django'ya Kaydet
                    tam_dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
                    
                    with open(tam_dosya_yolu, 'rb') as f:
                        # Eğer model Kulup ise 'logo' alanına, Sporcu ise 'profil_fotografi' alanına kaydet
                        getattr(kayit, alan_adi).save(dosya_adi, File(f), save=True)
                        
                    self.stdout.write(f"✅ {kayit.isim} için görsel yüklendi: {dosya_adi}")
                    sayac += 1
                    break # Bir kayıt için bir resim bulduysan diğer dosyalara bakma

        self.stdout.write(self.style.SUCCESS(f"🎉 Toplam {sayac} görsel güncellendi."))

    def normalize_name(self, text):
        """Türkçe karakterleri ve boşlukları temizler: 'Zehra Güneş' -> 'zehragunes'"""
        text = text.lower()
        text = text.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        text = text.replace(" ", "").replace("-", "").replace("_", "")
        return text