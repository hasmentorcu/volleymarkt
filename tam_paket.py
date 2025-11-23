import os

# --- 1. PROJE İÇERİKLERİ (Tüm Kodlar Burada) ---

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

ADMIN_CODE = """from django.contrib import admin
from .models import Kulup, Menajer, Sporcu

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('isim', 'sehir', 'kurulus_yili')

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'boy', 'kulup')
    list_filter = ('mevki', 'kulup')

admin.site.register(Menajer)
"""

VIEWS_CODE = """from django.shortcuts import render, get_object_or_404
from .models import Sporcu

def anasayfa(request):
    sporcular = Sporcu.objects.all()
    return render(request, 'index.html', {'sporcular': sporcular})

def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})
"""

URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import anasayfa, sporcu_detay

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

INDEX_HTML = """<!DOCTYPE html>
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
            <a href="/admin" class="text-gray-500 hover:text-indigo-900">Admin</a>
        </div>
    </nav>
    <div class="container mx-auto px-4">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 border-l-4 border-orange-500 pl-4">Öne Çıkan Sporcular</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {% for sporcu in sporcular %}
            <a href="{% url 'sporcu_detay' sporcu.id %}" class="block bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition duration-300 transform hover:-translate-y-1">
                <div class="h-64 overflow-hidden bg-gray-200 flex justify-center items-center relative">
                    {% if sporcu.profil_fotografi %}
                        <img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover">
                    {% else %}
                        <span class="text-gray-400">Fotoğraf Yok</span>
                    {% endif %}
                    <div class="absolute top-0 right-0 bg-orange-500 text-white text-xs font-bold px-2 py-1 m-2 rounded">DETAY</div>
                </div>
                <div class="p-6">
                    <div class="flex justify-between items-start mb-2">
                        <div>
                            <h2 class="text-xl font-bold text-gray-900">{{ sporcu.isim }}</h2>
                            <p class="text-sm text-gray-500">{{ sporcu.get_mevki_display }}</p>
                        </div>
                        <span class="bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-0.5 rounded">{{ sporcu.kulup.isim }}</span>
                    </div>
                </div>
            </a>
            {% empty %}
                <p>Henüz kayıtlı sporcu yok. Admin panelinden ekleyiniz.</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

DETAY_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ sporcu.isim }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    <nav class="bg-white shadow p-4 mb-8">
        <div class="container mx-auto">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <span class="text-gray-400 mx-2">/</span>
            <span class="text-gray-600">Profil</span>
        </div>
    </nav>
    <div class="container mx-auto px-4">
        <div class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col md:flex-row">
            <div class="md:w-1/3 bg-gray-200 h-96 md:h-auto">
                {% if sporcu.profil_fotografi %}
                    <img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover">
                {% else %}
                    <div class="w-full h-full flex items-center justify-center text-gray-500">Fotoğraf Yok</div>
                {% endif %}
            </div>
            <div class="p-8 md:w-2/3">
                <h1 class="text-4xl font-bold text-gray-900">{{ sporcu.isim }}</h1>
                <p class="text-xl text-orange-500 font-medium mt-1">{{ sporcu.kulup.isim }}</p>
                <div class="grid grid-cols-3 gap-4 mt-8 text-center bg-gray-50 p-4 rounded-lg border border-gray-100">
                    <div>
                        <div class="text-2xl font-bold text-indigo-900">{{ sporcu.boy }}</div>
                        <div class="text-xs text-gray-500">Boy (cm)</div>
                    </div>
                    <div>
                        <div class="text-2xl font-bold text-indigo-900">{{ sporcu.smac_yuksekligi|default:"-" }}</div>
                        <div class="text-xs text-gray-500">Smaç</div>
                    </div>
                    <div>
                        <div class="text-2xl font-bold text-indigo-900">{{ sporcu.blok_yuksekligi|default:"-" }}</div>
                        <div class="text-xs text-gray-500">Blok</div>
                    </div>
                </div>
                <div class="mt-8">
                     <h3 class="font-bold text-gray-900 border-b pb-2 mb-2">Video</h3>
                     {% if sporcu.video_linki %}
                        <a href="{{ sporcu.video_linki }}" target="_blank" class="inline-block bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition">▶ YouTube'da İzle</a>
                     {% else %}
                        <p class="text-gray-400">Video eklenmemiş.</p>
                     {% endif %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- 2. YARDIMCI FONKSİYONLAR ---

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Yazıldı: {path}")

def update_settings():
    path = 'volleymarkt/settings.py'
    if not os.path.exists(path):
        print("❌ HATA: settings.py bulunamadı!")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Core app ekle
    if "'core'," not in content:
        content = content.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [\n    'core',")
        print("✅ Settings: 'core' uygulaması eklendi.")
    
    # Media ayarı ekle
    if "MEDIA_ROOT" not in content:
        content += "\nimport os\nMEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"
        print("✅ Settings: Medya ayarları eklendi.")
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# --- 3. ÇALIŞTIRMA ---

def main():
    print("🚀 Tam Paket Kurulumu Başlıyor...\n")
    
    if not os.path.exists('manage.py'):
        print("❌ HATA: Lütfen bu dosyayı manage.py ile aynı klasörde çalıştır.")
        return

    # Dosyaları yaz
    write_file('core/__init__.py', '') # Boş dosya
    write_file('core/models.py', MODELS_CODE)
    write_file('core/admin.py', ADMIN_CODE)
    write_file('core/views.py', VIEWS_CODE)
    write_file('volleymarkt/urls.py', URLS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/detay.html', DETAY_HTML)
    
    # Ayarları düzelt
    update_settings()
    
    print("\n🎉 İŞLEM TAMAM! Şimdi şu komutu çalıştır:")
    print("python manage.py runserver")

if __name__ == '__main__':
    main()