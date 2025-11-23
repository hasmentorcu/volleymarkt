import os

# --- 1. MODELLER (Haber Eklendi) ---
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
    def __str__(self): return self.isim
    class Meta: verbose_name_plural = "Kulüpler"

class Menajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=100)
    sirket_adi = models.CharField(max_length=100, blank=True)
    telefon = models.CharField(max_length=20, blank=True)
    def __str__(self): return self.isim

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
    def __str__(self): return f"{self.isim}"

class Transfer(models.Model):
    sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='transferler')
    sezon = models.CharField(max_length=20, verbose_name="Sezon")
    tarih = models.DateField(null=True, blank=True)
    eski_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='giden_transferler')
    yeni_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='gelen_transferler')
    tip = models.CharField(max_length=50, choices=[('Kiralık', 'Kiralık'), ('Bonservis', 'Bonservis'), ('Bedelsiz', 'Bedelsiz')], default='Bedelsiz')
    class Meta: ordering = ['-sezon', '-id']

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

# YENİ MODEL: HABER
class Haber(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Haber Başlığı")
    ozet = models.TextField(max_length=500, verbose_name="Kısa Özet")
    icerik = models.TextField(verbose_name="Haber İçeriği")
    resim = models.ImageField(upload_to='haberler/', verbose_name="Kapak Resmi")
    tarih = models.DateTimeField(auto_now_add=True)
    kategori = models.CharField(max_length=20, choices=[('Transfer', 'Transfer'), ('Mac', 'Maç Sonucu'), ('Ozel', 'Özel Haber')], default='Ozel')
    manset_mi = models.BooleanField(default=False, verbose_name="Manşette Göster")

    class Meta:
        ordering = ['-tarih']
        verbose_name_plural = "Haberler"
    
    def __str__(self): return self.baslik
"""

# --- 2. ADMIN (Haber Eklendi) ---
ADMIN_CODE = """from django.contrib import admin
from .models import Kulup, Menajer, Sporcu, PuanDurumu, Mac, Transfer, Haber

class TransferInline(admin.TabularInline):
    model = Transfer
    extra = 1
    fk_name = "sporcu"

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'kulup', 'piyasa_degeri')
    list_filter = ('mevki', 'kulup')
    inlines = [TransferInline]

@admin.register(Haber)
class HaberAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'kategori', 'tarih', 'manset_mi')
    list_filter = ('kategori', 'manset_mi')
    search_fields = ('baslik',)

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin): list_display = ('isim', 'sehir')

@admin.register(PuanDurumu)
class PuanDurumuAdmin(admin.ModelAdmin): list_display = ('kulup', 'puan')

@admin.register(Mac)
class MacAdmin(admin.ModelAdmin): list_display = ('tarih', 'ev_sahibi', 'skor', 'deplasman')

admin.site.register(Menajer)
"""

# --- 3. VIEWS (Grafik Verisi ve Haberler Eklendi) ---
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Kulup, MEVKILER, Menajer, Haber
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def anasayfa(request):
    # 1. SPORCULAR VE FİLTRELEME
    sporcular = Sporcu.objects.all()
    
    isim = request.GET.get('isim')
    if isim: sporcular = sporcular.filter(isim__icontains=isim)
    
    kulup_id = request.GET.get('kulup')
    if kulup_id: sporcular = sporcular.filter(kulup_id=kulup_id)
        
    mevki = request.GET.get('mevki')
    if mevki: sporcular = sporcular.filter(mevki=mevki)
        
    min_boy = request.GET.get('min_boy')
    if min_boy: sporcular = sporcular.filter(boy__gte=min_boy)
    max_boy = request.GET.get('max_boy')
    if max_boy: sporcular = sporcular.filter(boy__lte=max_boy)

    # 2. YAN VERİLER
    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    maclar = Mac.objects.all().order_by('tarih')[:5]
    
    # 3. HABERLER (Yeni)
    mansetler = Haber.objects.filter(manset_mi=True)[:5] # Sadece manşet işaretli son 5 haber
    son_haberler = Haber.objects.all()[:6] # Genel akış

    # 4. GRAFİK VERİLERİ (Yeni)
    # A) Mevki Dağılımı (Pasta Grafik)
    mevki_data = Sporcu.objects.values('mevki').annotate(total=Count('id'))
    mevki_labels = [m['mevki'] for m in mevki_data]
    mevki_counts = [m['total'] for m in mevki_data]

    # B) En Uzun 5 Oyuncu (Bar Grafik)
    en_uzunlar = Sporcu.objects.filter(boy__isnull=False).order_by('-boy')[:5]
    uzun_labels = [s.isim for s in en_uzunlar]
    uzun_values = [s.boy for s in en_uzunlar]

    # C) En Değerli 5 Oyuncu (Bar Grafik)
    en_degerliler = Sporcu.objects.filter(piyasa_degeri__isnull=False).order_by('-piyasa_degeri')[:5]
    deger_labels = [s.isim for s in en_degerliler]
    deger_values = [s.piyasa_degeri for s in en_degerliler]

    context = {
        'sporcular': sporcular,
        'puan_tablosu': puan_tablosu,
        'maclar': maclar,
        'kulupler': Kulup.objects.all(),
        'mevkiler': MEVKILER,
        'secili_isim': isim,
        'secili_kulup': int(kulup_id) if kulup_id else None,
        'secili_mevki': mevki,
        'secili_min_boy': min_boy,
        'secili_max_boy': max_boy,
        # Yeni Veriler
        'mansetler': mansetler,
        'son_haberler': son_haberler,
        'mevki_labels': mevki_labels,
        'mevki_counts': mevki_counts,
        'uzun_labels': uzun_labels,
        'uzun_values': uzun_values,
        'deger_labels': deger_labels,
        'deger_values': deger_values,
    }
    return render(request, 'index.html', context)

def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})

def haber_detay(request, pk):
    haber = get_object_or_404(Haber, pk=pk)
    # Benzer haberler (Kategorisi aynı olan diğer 3 haber)
    benzer_haberler = Haber.objects.filter(kategori=haber.kategori).exclude(id=haber.id)[:3]
    return render(request, 'haber_detay.html', {'haber': haber, 'benzer_haberler': benzer_haberler})

# --- KULLANICI PANELİ FONKSİYONLARI (Değişmedi, aynen kalıyor) ---
def giris_yap(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if hasattr(user, 'menajer'): return redirect('menajer_panel')
            elif hasattr(user, 'sporcu'): return redirect('profil_duzenle')
            else: return redirect('anasayfa')
        else: messages.error(request, "Hatalı giriş.")
    return render(request, 'giris.html')

def cikis_yap(request):
    logout(request)
    return redirect('anasayfa')

def kayit_ol(request):
    if request.method == "POST":
        kullanici_adi = request.POST['username']
        sifre = request.POST['password']
        isim = request.POST['isim']
        rol = request.POST['rol']
        if User.objects.filter(username=kullanici_adi).exists():
            messages.error(request, "Kullanıcı adı dolu.")
            return render(request, 'kayit.html')
        user = User.objects.create_user(username=kullanici_adi, password=sifre)
        if rol == 'sporcu': Sporcu.objects.create(user=user, isim=isim); login(request, user); return redirect('profil_duzenle')
        elif rol == 'menajer': Menajer.objects.create(user=user, isim=isim); login(request, user); return redirect('menajer_panel')
    return render(request, 'kayit.html')

@login_required
def profil_duzenle(request):
    try: sporcu = request.user.sporcu
    except: return redirect('anasayfa')
    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES, instance=sporcu)
        if form.is_valid(): form.save(); return redirect('sporcu_detay', pk=sporcu.id)
    else: form = SporcuForm(instance=sporcu)
    return render(request, 'profil_duzenle.html', {'form': form})

@login_required
def menajer_panel(request):
    try: menajer = request.user.menajer
    except: return redirect('anasayfa')
    oyuncular = Sporcu.objects.filter(menajer=menajer)
    return render(request, 'menajer_panel.html', {'menajer': menajer, 'oyuncular': oyuncular})

@login_required
def menajer_oyuncu_ekle(request):
    try: menajer = request.user.menajer
    except: return redirect('anasayfa')
    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES)
        if form.is_valid():
            yeni = form.save(commit=False)
            yeni.menajer = menajer
            yeni.save()
            return redirect('menajer_panel')
    else: form = SporcuForm()
    return render(request, 'menajer_form.html', {'form': form, 'baslik': 'Yeni Oyuncu'})

@login_required
def menajer_oyuncu_duzenle(request, pk):
    try: 
        menajer = request.user.menajer
        sporcu = get_object_or_404(Sporcu, pk=pk, menajer=menajer)
    except: return redirect('anasayfa')
    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES, instance=sporcu)
        if form.is_valid(): form.save(); return redirect('menajer_panel')
    else: form = SporcuForm(instance=sporcu)
    return render(request, 'menajer_form.html', {'form': form, 'baslik': 'Düzenle'})
"""

# --- 4. URLS (Haber Detay Eklendi) ---
URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    path('haber/<int:pk>/', haber_detay, name='haber_detay'), # YENİ
    
    path('giris/', giris_yap, name='giris'),
    path('kayit/', kayit_ol, name='kayit'),
    path('cikis/', cikis_yap, name='cikis'),
    
    path('profil-duzenle/', profil_duzenle, name='profil_duzenle'),
    path('menajer-panel/', menajer_panel, name='menajer_panel'),
    path('menajer/ekle/', menajer_oyuncu_ekle, name='menajer_oyuncu_ekle'),
    path('menajer/duzenle/<int:pk>/', menajer_oyuncu_duzenle, name='menajer_oyuncu_duzenle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# --- 5. HTML: HABER DETAY ---
HABER_DETAY_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ haber.baslik }} - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 font-sans pb-12">
    <nav class="bg-white shadow p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <a href="/" class="text-gray-500 hover:text-orange-500 text-sm">← Anasayfa</a>
        </div>
    </nav>

    <div class="container mx-auto px-4 max-w-4xl">
        <article class="bg-white rounded-xl shadow-lg overflow-hidden mb-12">
            <div class="h-96 relative">
                {% if haber.resim %}
                    <img src="{{ haber.resim.url }}" class="w-full h-full object-cover">
                {% else %}
                    <div class="w-full h-full bg-gray-300 flex items-center justify-center text-gray-500">Görsel Yok</div>
                {% endif %}
                <div class="absolute top-4 left-4 bg-orange-500 text-white px-3 py-1 rounded text-sm font-bold">{{ haber.get_kategori_display }}</div>
            </div>
            
            <div class="p-8 md:p-12">
                <h1 class="text-4xl font-bold text-gray-900 mb-4 leading-tight">{{ haber.baslik }}</h1>
                <div class="flex items-center text-gray-500 text-sm mb-8 border-b pb-4">
                    <span>📅 {{ haber.tarih|date:"d F Y, H:i" }}</span>
                    <span class="mx-2">•</span>
                    <span>VolleyMarkt Haber Merkezi</span>
                </div>
                
                <div class="prose prose-lg text-gray-700 max-w-none">
                    {{ haber.icerik|linebreaks }}
                </div>
            </div>
        </article>

        <h3 class="text-xl font-bold text-gray-800 mb-6 border-l-4 border-indigo-900 pl-4">İlginizi Çekebilir</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {% for benzer in benzer_haberler %}
            <a href="{% url 'haber_detay' benzer.id %}" class="bg-white rounded-lg shadow hover:shadow-md transition group">
                <div class="h-40 overflow-hidden rounded-t-lg">
                    {% if benzer.resim %}
                        <img src="{{ benzer.resim.url }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                    {% else %}
                        <div class="w-full h-full bg-gray-200"></div>
                    {% endif %}
                </div>
                <div class="p-4">
                    <h4 class="font-bold text-gray-900 group-hover:text-orange-600 transition line-clamp-2">{{ benzer.baslik }}</h4>
                    <p class="text-xs text-gray-500 mt-2">{{ benzer.tarih|date:"d M" }}</p>
                </div>
            </a>
            {% empty %}
                <p class="text-gray-400 text-sm">Benzer haber bulunamadı.</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# --- 6. HTML: INDEX GÜNCELLEME (Slider ve Grafikler) ---
INDEX_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt - Voleybolun Kalbi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .swiper { width: 100%; height: 400px; }
        .swiper-slide { text-align: center; font-size: 18px; background: #fff; display: flex; justify-content: center; align-items: center; }
        .swiper-slide img { display: block; width: 100%; height: 100%; object-fit: cover; }
    </style>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow p-4 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <div class="space-x-4 text-sm font-bold">
                {% if user.is_authenticated %}
                    <a href="{% url 'cikis' %}" class="text-red-500">Çıkış</a>
                {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900">Giriş Yap</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-4 py-8">
        
        {% if mansetler %}
        <div class="mb-12">
            <div class="swiper mySwiper rounded-2xl shadow-xl overflow-hidden">
                <div class="swiper-wrapper">
                    {% for haber in mansetler %}
                    <div class="swiper-slide relative">
                        {% if haber.resim %}
                            <img src="{{ haber.resim.url }}" alt="{{ haber.baslik }}">
                        {% else %}
                            <div class="w-full h-full bg-gray-800 flex items-center justify-center text-white">Görsel Yok</div>
                        {% endif %}
                        <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black via-black/70 to-transparent p-8 text-left">
                            <span class="bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded mb-2 inline-block">{{ haber.get_kategori_display }}</span>
                            <h2 class="text-3xl md:text-4xl font-bold text-white mb-2 leading-tight">{{ haber.baslik }}</h2>
                            <p class="text-gray-300 hidden md:block line-clamp-2">{{ haber.ozet }}</p>
                            <a href="{% url 'haber_detay' haber.id %}" class="inline-block mt-4 bg-white text-black px-4 py-2 rounded-lg font-bold hover:bg-gray-200 transition">Haberi Oku</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <div class="swiper-button-next text-white"></div>
                <div class="swiper-button-prev text-white"></div>
                <div class="swiper-pagination"></div>
            </div>
        </div>
        {% endif %}

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8">
            <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <input type="text" name="isim" value="{{ secili_isim|default:'' }}" placeholder="Oyuncu Ara..." class="border p-2 rounded w-full md:col-span-4">
                <select name="kulup" class="border p-2 rounded w-full"><option value="">Kulüp</option>{% for k in kulupler %}<option value="{{ k.id }}">{{ k.isim }}</option>{% endfor %}</select>
                <select name="mevki" class="border p-2 rounded w-full"><option value="">Mevki</option>{% for k,v in mevkiler %}<option value="{{ k }}">{{ v }}</option>{% endfor %}</select>
                <button type="submit" class="bg-indigo-900 text-white font-bold rounded p-2 md:col-span-2">Filtrele</button>
            </form>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div class="lg:col-span-2">
                <h2 class="text-xl font-bold text-gray-800 mb-4 border-l-4 border-orange-500 pl-3">Oyuncular</h2>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {% for sporcu in sporcular %}
                    <a href="{% url 'sporcu_detay' sporcu.id %}" class="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden group">
                        <div class="h-40 bg-gray-200 relative">
                            {% if sporcu.profil_fotografi %}
                                <img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover group-hover:scale-105 transition">
                            {% endif %}
                            <div class="absolute bottom-0 left-0 w-full bg-black/60 p-2 text-white text-sm font-bold truncate">{{ sporcu.isim }}</div>
                        </div>
                    </a>
                    {% empty %}
                        <p class="text-gray-500 col-span-3 text-center py-8">Sonuç bulunamadı.</p>
                    {% endfor %}
                </div>
            </div>

            <div class="space-y-8">
                <div class="bg-white rounded-xl shadow overflow-hidden">
                    <div class="bg-indigo-900 text-white p-3 font-bold text-center">Sultanlar Ligi</div>
                    <table class="w-full text-sm text-left">
                        {% for sira in puan_tablosu %}
                        <tr class="border-b hover:bg-gray-50"><td class="p-2">{{ forloop.counter }}. {{ sira.kulup.isim }}</td><td class="p-2 font-bold text-right">{{ sira.puan|floatformat:0 }}P</td></tr>
                        {% endfor %}
                    </table>
                </div>

                <div class="bg-white rounded-xl shadow p-4">
                    <h3 class="font-bold text-gray-800 mb-4">Son Gelişmeler</h3>
                    <div class="space-y-4">
                        {% for haber in son_haberler %}
                        <a href="{% url 'haber_detay' haber.id %}" class="flex gap-3 group">
                            <div class="w-16 h-16 bg-gray-200 rounded overflow-hidden flex-shrink-0">
                                {% if haber.resim %}<img src="{{ haber.resim.url }}" class="w-full h-full object-cover">{% endif %}
                            </div>
                            <div>
                                <h4 class="text-sm font-bold text-gray-900 group-hover:text-orange-500 line-clamp-2">{{ haber.baslik }}</h4>
                                <span class="text-xs text-gray-400">{{ haber.tarih|timesince }} önce</span>
                            </div>
                        </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <div class="mt-16 border-t pt-12">
            <h2 class="text-2xl font-bold text-center text-indigo-900 mb-8">📊 Lig İstatistikleri</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white p-4 rounded-xl shadow">
                    <h3 class="text-center font-bold text-gray-700 mb-4">Mevki Dağılımı</h3>
                    <canvas id="mevkiChart"></canvas>
                </div>
                
                <div class="bg-white p-4 rounded-xl shadow">
                    <h3 class="text-center font-bold text-gray-700 mb-4">En Uzun Oyuncular</h3>
                    <canvas id="boyChart"></canvas>
                </div>

                <div class="bg-white p-4 rounded-xl shadow">
                    <h3 class="text-center font-bold text-gray-700 mb-4">En Değerli Oyuncular</h3>
                    <canvas id="degerChart"></canvas>
                </div>
            </div>
        </div>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        var swiper = new Swiper(".mySwiper", {
            spaceBetween: 30,
            centeredSlides: true,
            autoplay: { delay: 3500, disableOnInteraction: false },
            pagination: { el: ".swiper-pagination", clickable: true },
            navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
        });
    </script>

    <script>
        // Django'dan gelen verileri JS değişkenlerine alıyoruz
        const mevkiData = {
            labels: {{ mevki_labels|safe }},
            datasets: [{
                data: {{ mevki_counts|safe }},
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        };

        const boyData = {
            labels: {{ uzun_labels|safe }},
            datasets: [{
                label: 'Boy (cm)',
                data: {{ uzun_values|safe }},
                backgroundColor: '#36A2EB'
            }]
        };

        const degerData = {
            labels: {{ deger_labels|safe }},
            datasets: [{
                label: 'Piyasa Değeri (€)',
                data: {{ deger_values|safe }},
                backgroundColor: '#4BC0C0'
            }]
        };

        // Grafikleri Çiz
        new Chart(document.getElementById('mevkiChart'), { type: 'pie', data: mevkiData });
        
        new Chart(document.getElementById('boyChart'), { 
            type: 'bar', 
            data: boyData,
            options: { indexAxis: 'y' } // Yatay Bar
        });

        new Chart(document.getElementById('degerChart'), { type: 'bar', data: degerData });
    </script>
</body>
</html>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Güncellendi: {path}")

def main():
    print("🚀 MEGA Güncelleme Başlıyor...\n")
    write_file('core/models.py', MODELS_CODE)
    write_file('core/admin.py', ADMIN_CODE)
    write_file('core/views.py', VIEWS_CODE)
    write_file('volleymarkt/urls.py', URLS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/haber_detay.html', HABER_DETAY_HTML)
    
    print("\n🎉 İŞLEM TAMAM! Şimdi şu komutları çalıştır:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")
    print("👉 NOT: Admin paneline girip 'Haber' eklemeyi unutma, yoksa manşet boş görünür.")

if __name__ == '__main__':
    main()