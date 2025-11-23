import os

# --- GÜNCELLENMİŞ MODEL DOSYASI (Sıralama Mantığı Değişti) ---
MODELS_CODE = """from django.db import models
from django.contrib.auth.models import User

MEVKILER = (
    ('PASOR', 'Pasör'),
    ('PASOR_CAPRAZI', 'Pasör Çaprazı'),
    ('SMACOR', 'Smaçör'),
    ('ORTA_OYUNCU', 'Orta Oyuncu'),
    ('LIBERO', 'Libero'),
)

class Kulup(models.Model):
    isim = models.CharField(max_length=100, verbose_name="Kulüp Adı")
    sehir = models.CharField(max_length=50, verbose_name="Şehir")
    kurulus_yili = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kuruluş Yılı")
    logo = models.ImageField(upload_to='kulupler/', null=True, blank=True, verbose_name="Kulüp Logosu")

    def __str__(self):
        return self.isim
    
    class Meta:
        verbose_name_plural = "Kulüpler"

class Menajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=100)
    sirket_adi = models.CharField(max_length=100, blank=True)
    telefon = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.isim

class Sporcu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=100)
    dogum_tarihi = models.DateField(null=True, blank=True)
    boy = models.PositiveIntegerField(help_text="cm", null=True, blank=True)
    kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular")
    menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True)
    mevki = models.CharField(max_length=20, choices=MEVKILER, null=True, blank=True)
    piyasa_degeri = models.PositiveIntegerField(null=True, blank=True, verbose_name="Piyasa Değeri (€)")
    smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True)
    blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True)
    profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True)
    video_linki = models.URLField(blank=True)

    def __str__(self):
        return f"{self.isim}"

class Transfer(models.Model):
    sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='transferler')
    sezon = models.CharField(max_length=20, verbose_name="Sezon")
    tarih = models.DateField(null=True, blank=True)
    eski_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='giden_transferler', verbose_name="Eski Kulüp")
    yeni_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='gelen_transferler', verbose_name="Yeni Kulüp")
    tip = models.CharField(max_length=50, choices=[('Kiralık', 'Kiralık'), ('Bonservis', 'Bonservis'), ('Bedelsiz', 'Bedelsiz')], default='Bedelsiz')
    
    class Meta:
        # İŞTE SİHİRLİ DOKUNUŞ BURADA:
        # '-sezon' diyerek yılları tersten sıralıyoruz (2024 -> 2011)
        ordering = ['-sezon', '-id']

class PuanDurumu(models.Model):
    kulup = models.OneToOneField(Kulup, on_delete=models.CASCADE)
    oynanan = models.PositiveIntegerField(default=0)
    galibiyet = models.PositiveIntegerField(default=0)
    maglubiyet = models.PositiveIntegerField(default=0)
    puan = models.FloatField(default=0)
    class Meta: ordering = ['-puan', '-galibiyet']

class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE)
    deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE)
    tarih = models.DateTimeField()
    skor = models.CharField(max_length=10, blank=True, default="-")
    class Meta: ordering = ['tarih']
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Modeller Güncellendi: {path}")

def main():
    print("🚀 Sıralama Ayarı Yapılıyor...\n")
    write_file('core/models.py', MODELS_CODE)
    print("\n🎉 İŞLEM TAMAM! Lütfen sunucuyu yeniden başlatın.")

if __name__ == '__main__':
    main()