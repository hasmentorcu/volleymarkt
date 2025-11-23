from django.db import models
from django.contrib.auth.models import User

MEVKILER = (('PASOR', 'Pasör'), ('PASOR_CAPRAZI', 'Pasör Çaprazı'), ('SMACOR', 'Smaçör'), ('ORTA_OYUNCU', 'Orta Oyuncu'), ('LIBERO', 'Libero'))

class Kulup(models.Model):
    isim = models.CharField(max_length=100); sehir = models.CharField(max_length=50); kurulus_yili = models.PositiveIntegerField(null=True, blank=True); logo = models.ImageField(upload_to='kulupler/', null=True, blank=True)
    def __str__(self): return self.isim

class Menajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True); isim = models.CharField(max_length=100); sirket_adi = models.CharField(max_length=100, blank=True); telefon = models.CharField(max_length=20, blank=True)
    def __str__(self): return self.isim

class Sporcu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True); isim = models.CharField(max_length=100); dogum_tarihi = models.DateField(null=True, blank=True); boy = models.PositiveIntegerField(null=True, blank=True); kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular"); menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True); mevki = models.CharField(max_length=20, choices=MEVKILER, null=True, blank=True); piyasa_degeri = models.PositiveIntegerField(null=True, blank=True); smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True); blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True); profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True); video_linki = models.URLField(blank=True)
    begeniler = models.ManyToManyField(User, related_name='begendigi_sporcular', blank=True)
    def __str__(self): return self.isim
    def begeni_sayisi(self): return self.begeniler.count()

class Transfer(models.Model):
    sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='transferler'); sezon = models.CharField(max_length=20); tarih = models.DateField(null=True, blank=True); eski_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='giden'); yeni_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='gelen'); tip = models.CharField(max_length=50, default='Bedelsiz')
    class Meta: ordering = ['-sezon', '-id']

class PuanDurumu(models.Model):
    kulup = models.OneToOneField(Kulup, on_delete=models.CASCADE); oynanan = models.PositiveIntegerField(default=0); galibiyet = models.PositiveIntegerField(default=0); maglubiyet = models.PositiveIntegerField(default=0); puan = models.FloatField(default=0)
    class Meta: ordering = ['-puan', '-galibiyet']

class Haber(models.Model):
    baslik = models.CharField(max_length=200); ozet = models.TextField(max_length=500); icerik = models.TextField(); resim = models.ImageField(upload_to='haberler/'); tarih = models.DateTimeField(auto_now_add=True); kategori = models.CharField(max_length=20, choices=[('Transfer', 'Transfer'), ('Mac', 'Maç Sonucu'), ('Ozel', 'Özel Haber')], default='Ozel'); manset_mi = models.BooleanField(default=False)
    class Meta: ordering = ['-tarih']

class Yorum(models.Model):
    yazan = models.ForeignKey(User, on_delete=models.CASCADE); haber = models.ForeignKey(Haber, on_delete=models.CASCADE, related_name='yorumlar', null=True, blank=True); sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='yorumlar', null=True, blank=True); metin = models.TextField(); tarih = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-tarih']

class Anket(models.Model):
    soru = models.CharField(max_length=200); aktif_mi = models.BooleanField(default=True); olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.soru

class Secenek(models.Model):
    anket = models.ForeignKey(Anket, on_delete=models.CASCADE, related_name='secenekler'); metin = models.CharField(max_length=200); oy_sayisi = models.PositiveIntegerField(default=0)
    def __str__(self): return self.metin

class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE, verbose_name="Ev Sahibi")
    deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE, verbose_name="Deplasman")
    tarih = models.DateTimeField(verbose_name="Tarih ve Saat")
    skor = models.CharField(max_length=10, blank=True, default="-", verbose_name="Maç Skoru", help_text="Örn: 3-1")
    salon = models.CharField(max_length=100, blank=True, verbose_name="Salon Adı", help_text="Örn: Burhan Felek")
    hakemler = models.CharField(max_length=200, blank=True, verbose_name="Hakemler", help_text="Örn: Nurper Özbar, Erol Akbulut")
    set1 = models.CharField(max_length=10, blank=True, verbose_name="1. Set", help_text="25-18")
    set2 = models.CharField(max_length=10, blank=True, verbose_name="2. Set", help_text="22-25")
    set3 = models.CharField(max_length=10, blank=True, verbose_name="3. Set", help_text="25-15")
    set4 = models.CharField(max_length=10, blank=True, verbose_name="4. Set")
    set5 = models.CharField(max_length=10, blank=True, verbose_name="5. Set") # Tie-break
    tamamlandi = models.BooleanField(default=False, verbose_name="Maç Bitti")
    class Meta: ordering = ['tarih']; verbose_name_plural = "Fikstür / Maçlar"
    def __str__(self): return f"{self.ev_sahibi} vs {self.deplasman}"

class Tahmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tahminler')
    mac = models.ForeignKey(Mac, on_delete=models.CASCADE, related_name='tahminler')
    SKOR_SECENEKLERI = [('3-0', '3-0'), ('3-1', '3-1'), ('3-2', '3-2'), ('0-3', '0-3'), ('1-3', '1-3'), ('2-3', '2-3')]
    skor = models.CharField(max_length=5, choices=SKOR_SECENEKLERI)
    puan_kazandi = models.IntegerField(default=0, help_text="Maç bitince hesaplanır")
    hesaplandi = models.BooleanField(default=False)
    tarih = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('user', 'mac')

# --- YENİ MODEL: BİLDİRİM ---
class Bildirim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bildirimler')
    mesaj = models.CharField(max_length=255)
    okundu = models.BooleanField(default=False)
    tarih = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-tarih']
