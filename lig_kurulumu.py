import os

# --- 1. GÜNCELLENMİŞ MODELLER (Mac ve PuanDurumu Eklendi) ---

MODELS_CODE = """from django.db import models

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
    isim = models.CharField(max_length=100, verbose_name="Menajer Adı Soyadı")
    sirket_adi = models.CharField(max_length=100, verbose_name="Şirket Adı", blank=True)
    telefon = models.CharField(max_length=20, blank=True, verbose_name="İletişim")

    def __str__(self):
        return self.isim
    
    class Meta:
        verbose_name_plural = "Menajerler"

class Sporcu(models.Model):
    isim = models.CharField(max_length=100, verbose_name="Ad Soyad")
    dogum_tarihi = models.DateField(verbose_name="Doğum Tarihi")
    boy = models.PositiveIntegerField(help_text="cm", verbose_name="Boy")
    kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular", verbose_name="Mevcut Kulübü")
    menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Menajeri")
    mevki = models.CharField(max_length=20, choices=MEVKILER, verbose_name="Mevki")
    smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True, verbose_name="Smaç")
    blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True, verbose_name="Blok")
    profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True)
    video_linki = models.URLField(blank=True, verbose_name="YouTube Linki")

    def __str__(self):
        return f"{self.isim}"
    
    class Meta:
        verbose_name_plural = "Sporcular"

# --- YENİ EKLENENLER ---

class PuanDurumu(models.Model):
    kulup = models.OneToOneField(Kulup, on_delete=models.CASCADE, verbose_name="Kulüp")
    oynanan = models.PositiveIntegerField(default=0, verbose_name="O")
    galibiyet = models.PositiveIntegerField(default=0, verbose_name="G")
    maglubiyet = models.PositiveIntegerField(default=0, verbose_name="M")
    puan = models.PositiveIntegerField(default=0, verbose_name="P")

    class Meta:
        ordering = ['-puan', '-galibiyet'] # Puanı yüksek olan üstte durur
        verbose_name_plural = "Puan Durumu"
    
    def __str__(self):
        return f"{self.kulup.isim} - {self.puan} Puan"

class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE, verbose_name="Ev Sahibi")
    deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE, verbose_name="Deplasman")
    tarih = models.DateTimeField(verbose_name="Maç Tarihi ve Saati")
    skor = models.CharField(max_length=10, blank=True, default="-", help_text="Örn: 3-1", verbose_name="Skor")
    
    class Meta:
        ordering = ['tarih']
        verbose_name_plural = "Fikstür / Maçlar"

    def __str__(self):
        return f"{self.ev_sahibi} vs {self.deplasman}"
"""

ADMIN_CODE = """from django.contrib import admin
from .models import Kulup, Menajer, Sporcu, PuanDurumu, Mac

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('isim', 'sehir')

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'kulup')
    list_filter = ('mevki', 'kulup')

@admin.register(PuanDurumu)
class PuanDurumuAdmin(admin.ModelAdmin):
    list_display = ('kulup', 'oynanan', 'galibiyet', 'maglubiyet', 'puan')
    ordering = ('-puan',)

@admin.register(Mac)
class MacAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'ev_sahibi', 'skor', 'deplasman')
    list_filter = ('tarih',)

admin.site.register(Menajer)
"""

VIEWS_CODE = """from django.shortcuts import render, get_object_or_404
from .models import Sporcu, PuanDurumu, Mac
from django.utils import timezone

def anasayfa(request):
    sporcular = Sporcu.objects.all()
    
    # Puan durumunu çek (En yüksek puanlı en üstte)
    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    
    # Gelecek maçları çek (Bugün ve sonrası)
    # Not: Basitlik için tüm maçları çekiyoruz, istersen filtre ekleyebiliriz.
    maclar = Mac.objects.all().order_by('tarih')[:5] # En yakın 5 maç

    context = {
        'sporcular': sporcular,
        'puan_tablosu': puan_tablosu,
        'maclar': maclar
    }
    return render(request, 'index.html', context)

def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})
"""

# --- 2. GÜNCELLENMİŞ TASARIM (Sidebar Eklendi) ---

INDEX_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    
    <nav class="bg-white shadow p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <div class="space-x-4">
                <a href="/admin" class="text-sm font-medium text-gray-500 hover:text-indigo-900">Yönetici Paneli</a>
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-4 mb-12">
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            
            <div class="md:col-span-3">
                <h1 class="text-2xl font-bold text-gray-800 mb-6 border-l-4 border-orange-500 pl-4">Öne Çıkan Sporcular</h1>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {% for sporcu in sporcular %}
                    <a href="{% url 'sporcu_detay' sporcu.id %}" class="block bg-white rounded-xl shadow hover:shadow-lg transition duration-300 group">
                        <div class="h-56 overflow-hidden bg-gray-200 relative">
                            {% if sporcu.profil_fotografi %}
                                <img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                            {% else %}
                                <div class="w-full h-full flex items-center justify-center text-gray-400">Görsel Yok</div>
                            {% endif %}
                            <div class="absolute bottom-0 left-0 bg-gradient-to-t from-black to-transparent w-full p-4 pt-8">
                                <h2 class="text-white font-bold text-lg">{{ sporcu.isim }}</h2>
                                <p class="text-orange-300 text-xs">{{ sporcu.kulup.isim }}</p>
                            </div>
                        </div>
                        <div class="p-4 flex justify-between items-center text-sm text-gray-600">
                            <span>{{ sporcu.get_mevki_display }}</span>
                            <span class="font-bold">{{ sporcu.boy }} cm</span>
                        </div>
                    </a>
                    {% empty %}
                        <p class="text-gray-500">Henüz sporcu eklenmedi.</p>
                    {% endfor %}
                </div>
            </div>

            <div class="md:col-span-1 space-y-8">
                
                <div class="bg-white rounded-xl shadow overflow-hidden">
                    <div class="bg-indigo-900 text-white p-3 font-bold text-center">
                        Sultanlar Ligi
                    </div>
                    <table class="w-full text-sm text-left text-gray-600">
                        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                            <tr>
                                <th class="px-4 py-3">Kulüp</th>
                                <th class="px-2 py-3 text-center">O</th>
                                <th class="px-2 py-3 text-center">P</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for sira in puan_tablosu %}
                            <tr class="border-b hover:bg-gray-50">
                                <td class="px-4 py-2 font-medium text-gray-900">
                                    {{ forloop.counter }}. {{ sira.kulup.isim }}
                                </td>
                                <td class="px-2 py-2 text-center">{{ sira.oynanan }}</td>
                                <td class="px-2 py-2 text-center font-bold text-indigo-900">{{ sira.puan }}</td>
                            </tr>
                            {% empty %}
                            <tr><td colspan="3" class="p-4 text-center text-xs text-gray-400">Veri Girilmedi</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="bg-white rounded-xl shadow p-4">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2">Fikstür</h3>
                    <div class="space-y-4">
                        {% for mac in maclar %}
                        <div class="text-sm">
                            <div class="text-xs text-gray-400 mb-1">{{ mac.tarih|date:"d M Y - H:i" }}</div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-900">{{ mac.ev_sahibi.isim }}</span>
                                <span class="bg-gray-100 px-2 py-1 rounded text-xs font-bold">{{ mac.skor }}</span>
                                <span class="font-medium text-gray-900">{{ mac.deplasman.isim }}</span>
                            </div>
                        </div>
                        {% empty %}
                            <p class="text-xs text-gray-400">Planlanmış maç yok.</p>
                        {% endfor %}
                    </div>
                </div>

            </div>

        </div>
    </div>
</body>
</html>
"""

# --- ÇALIŞTIRMA ---

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Güncellendi: {path}")

def main():
    print("🚀 Lig Modülü Yükleniyor...\n")
    
    write_file('core/models.py', MODELS_CODE)
    write_file('core/admin.py', ADMIN_CODE)
    write_file('core/views.py', VIEWS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    
    print("\n🎉 GÜNCELLEME TAMAMLANDI!")
    print("⚠️ LÜTFEN ŞU KOMUTLARI ÇALIŞTIR (Veritabanını güncellemek için):")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")

if __name__ == '__main__':
    main()