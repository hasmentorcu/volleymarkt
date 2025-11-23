import os
import sys

# --- İÇERİKLER ---

MODELS_CONTENT = """from django.db import models

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
    boy = models.PositiveIntegerField(help_text="Santimetre cinsinden (Örn: 190)", verbose_name="Boy (cm)")
    kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular", verbose_name="Mevcut Kulübü")
    menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Menajeri")
    mevki = models.CharField(max_length=20, choices=MEVKILER, verbose_name="Mevki")
    smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True, verbose_name="Smaç Yüksekliği (cm)")
    blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True, verbose_name="Blok Yüksekliği (cm)")
    profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True)
    video_linki = models.URLField(blank=True, verbose_name="YouTube Video Linki")

    def __str__(self):
        return f"{self.isim} ({self.kulup})"
    
    class Meta:
        verbose_name_plural = "Sporcular"
"""

ADMIN_CONTENT = """from django.contrib import admin
from .models import Kulup, Menajer, Sporcu

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('isim', 'sehir', 'kurulus_yili')
    search_fields = ('isim',)

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'boy', 'kulup', 'menajer')
    list_filter = ('mevki', 'kulup')
    search_fields = ('isim', 'kulup__isim')

admin.site.register(Menajer)
"""

VIEWS_CONTENT = """from django.shortcuts import render
from .models import Sporcu

def anasayfa(request):
    sporcular = Sporcu.objects.all()
    context = {'sporcular': sporcular}
    return render(request, 'index.html', context)
"""

URLS_CONTENT = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import anasayfa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    <nav class="bg-white shadow p-4 mb-8">
        <div class="container mx-auto flex justify-between items-center">
            <div class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></div>
            <a href="/admin" class="text-gray-500 hover:text-indigo-900">Yönetici Girişi</a>
        </div>
    </nav>
    <div class="container mx-auto px-4">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 border-l-4 border-orange-500 pl-4">Öne Çıkan Sporcular</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {% for sporcu in sporcular %}
            <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
                <div class="h-64 overflow-hidden bg-gray-200 flex justify-center items-center">
                    {% if sporcu.profil_fotografi %}
                        <img src="{{ sporcu.profil_fotografi.url }}" alt="{{ sporcu.isim }}" class="w-full h-full object-cover">
                    {% else %}
                        <span class="text-gray-400">Fotoğraf Yok</span>
                    {% endif %}
                </div>
                <div class="p-6">
                    <div class="flex justify-between items-start mb-2">
                        <div>
                            <h2 class="text-xl font-bold text-gray-900">{{ sporcu.isim }}</h2>
                            <p class="text-sm text-gray-500">{{ sporcu.get_mevki_display }}</p>
                        </div>
                        <span class="bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                            {{ sporcu.kulup.isim }}
                        </span>
                    </div>
                    <div class="grid grid-cols-3 gap-2 mt-4 text-center border-t pt-4">
                        <div>
                            <div class="text-lg font-bold text-indigo-900">{{ sporcu.boy }}</div>
                            <div class="text-xs text-gray-500">Boy (cm)</div>
                        </div>
                        <div>
                            <div class="text-lg font-bold text-indigo-900">{{ sporcu.smac_yuksekligi|default:"-" }}</div>
                            <div class="text-xs text-gray-500">Smaç</div>
                        </div>
                        <div>
                            <div class="text-lg font-bold text-indigo-900">{{ sporcu.blok_yuksekligi|default:"-" }}</div>
                            <div class="text-xs text-gray-500">Blok</div>
                        </div>
                    </div>
                </div>
            </div>
            {% empty %}
                <p>Henüz kayıtlı sporcu yok. Lütfen Admin panelinden ekleyin.</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# --- YARDIMCI FONKSİYONLAR ---

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Oluşturuldu: {path}")

def update_settings():
    settings_path = 'volleymarkt/settings.py'
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # App ekleme
    if "'core'," not in content:
        content = content.replace(
            "    'django.contrib.staticfiles',",
            "    'django.contrib.staticfiles',\n    'core',"
        )
        print("✅ Ayar Güncellendi: 'core' uygulaması settings.py'a eklendi.")

    # Medya ayarları ekleme
    if "MEDIA_ROOT" not in content:
        content += "\n\n# Medya Ayarları (Otomatik Eklendi)\nimport os\nMEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"
        print("✅ Ayar Güncellendi: Medya yolları settings.py'a eklendi.")

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)

# --- ANA İŞLEM ---

def main():
    print("🚀 VolleyMarkt Kurulumu Başlıyor...\n")

    # Klasör Kontrolü
    if not os.path.exists('manage.py'):
        print("❌ HATA: Bu dosyayı manage.py ile aynı klasörde çalıştırmalısın!")
        return

    # Dosyaları Oluştur
    create_file('core/models.py', MODELS_CONTENT)
    create_file('core/admin.py', ADMIN_CONTENT)
    create_file('core/views.py', VIEWS_CONTENT)
    create_file('core/templates/index.html', HTML_CONTENT)
    create_file('volleymarkt/urls.py', URLS_CONTENT)

    # Ayarları Güncelle
    update_settings()

    print("\n🎉 KURULUM TAMAMLANDI!")
    print("------------------------------------------------")
    print("Şimdi şu komutları sırasıyla çalıştır:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()