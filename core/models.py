from django.db import models
from django.contrib.auth.models import User

MEVKILER = (('PASOR', 'Pasör'), ('PASOR_CAPRAZI', 'Pasör Çaprazı'), ('SMACOR', 'Smaçör'), ('ORTA_OYUNCU', 'Orta Oyuncu'), ('LIBERO', 'Libero'))
LIGLER = (('SULTANLAR', 'Vodafone Sultanlar Ligi'), ('EFELER', 'AXA Sigorta Efeler Ligi'), ('KADIN_1', 'Kadınlar 1. Ligi'), ('ERKEK_1', 'Erkekler 1. Ligi'))

class Kulup(models.Model):
    isim = models.CharField(max_length=100); sehir = models.CharField(max_length=50); 
    lig = models.CharField(max_length=20, choices=LIGLER, default='SULTANLAR'); 
    kurulus_yili = models.PositiveIntegerField(null=True, blank=True); logo = models.ImageField(upload_to='kulupler/', null=True, blank=True)
    def __str__(self): return f"{self.isim} ({self.get_lig_display()})"
    class Meta: verbose_name_plural = "Kulüpler"

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

class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE); deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE); tarih = models.DateTimeField(); skor = models.CharField(max_length=10, blank=True, default="-"); salon = models.CharField(max_length=100, blank=True); hakemler = models.CharField(max_length=200, blank=True); set1 = models.CharField(max_length=10, blank=True); set2 = models.CharField(max_length=10, blank=True); set3 = models.CharField(max_length=10, blank=True); set4 = models.CharField(max_length=10, blank=True); set5 = models.CharField(max_length=10, blank=True); tamamlandi = models.BooleanField(default=False)
    class Meta: ordering = ['tarih']
    def __str__(self): return f"{self.ev_sahibi} vs {self.deplasman}"

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

class Tahmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tahminler'); mac = models.ForeignKey(Mac, on_delete=models.CASCADE, related_name='tahminler'); skor = models.CharField(max_length=5); puan_kazandi = models.IntegerField(default=0); hesaplandi = models.BooleanField(default=False); tarih = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('user', 'mac')

class Bildirim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bildirimler'); mesaj = models.CharField(max_length=255); okundu = models.BooleanField(default=False); tarih = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-tarih']
