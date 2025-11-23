import os

# --- 1. VIEWS (Karşılaştırma Mantığı) ---
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Kulup, MEVKILER, Menajer, Haber
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

# --- MEVCUT FONKSİYONLAR (Kısaltıldı, aynen korunuyor) ---
def anasayfa(request):
    # ... (Eski kodlar aynen kalıyor) ...
    sporcular = Sporcu.objects.all()
    # (Filtreleme kodları burada...)
    isim = request.GET.get('isim')
    if isim: sporcular = sporcular.filter(isim__icontains=isim)
    
    # ... (Grafik ve Haber kodları burada...)
    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    maclar = Mac.objects.all().order_by('tarih')[:5]
    mansetler = Haber.objects.filter(manset_mi=True)[:5]
    son_haberler = Haber.objects.all()[:6]

    # VS MODU İÇİN TÜM SPORCULARI LİSTELE (Selectbox için)
    tum_sporcular = Sporcu.objects.all().order_by('isim')

    context = {
        'sporcular': sporcular, # Filtrelenmiş liste
        'tum_sporcular': tum_sporcular, # Karşılaştırma için tam liste
        'puan_tablosu': puan_tablosu,
        'maclar': maclar,
        'kulupler': Kulup.objects.all(),
        'mevkiler': MEVKILER,
        'mansetler': mansetler,
        'son_haberler': son_haberler,
        # ... (Diğer context verileri) ...
    }
    return render(request, 'index.html', context)

# --- YENİ: KARŞILAŞTIRMA SAYFASI ---
def karsilastir(request):
    id1 = request.GET.get('p1')
    id2 = request.GET.get('p2')

    if not id1 or not id2:
        messages.warning(request, "Lütfen karşılaştırmak için iki oyuncu seçin.")
        return redirect('anasayfa')

    p1 = get_object_or_404(Sporcu, id=id1)
    p2 = get_object_or_404(Sporcu, id=id2)

    # Karşılaştırma Mantığı (Kazananı Belirle)
    # 0: Eşit, 1: p1 kazanır, 2: p2 kazanır
    
    def kiyasla(val1, val2):
        if not val1 and not val2: return 0
        if not val1: return 2
        if not val2: return 1
        if val1 > val2: return 1
        elif val2 > val1: return 2
        return 0

    analiz = {
        'boy': kiyasla(p1.boy, p2.boy),
        'smac': kiyasla(p1.smac_yuksekligi, p2.smac_yuksekligi),
        'blok': kiyasla(p1.blok_yuksekligi, p2.blok_yuksekligi),
        'deger': kiyasla(p1.piyasa_degeri, p2.piyasa_degeri),
    }

    return render(request, 'karsilastir.html', {'p1': p1, 'p2': p2, 'analiz': analiz})

# ... (Diğer tüm view fonksiyonları: sporcu_detay, giris_yap, haber_detay vb. aynen kalmalı) ...
def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})
def haber_detay(request, pk):
    haber = get_object_or_404(Haber, pk=pk)
    benzer_haberler = Haber.objects.filter(kategori=haber.kategori).exclude(id=haber.id)[:3]
    return render(request, 'haber_detay.html', {'haber': haber, 'benzer_haberler': benzer_haberler})
def giris_yap(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user(); login(request, user)
            if hasattr(user, 'menajer'): return redirect('menajer_panel')
            elif hasattr(user, 'sporcu'): return redirect('profil_duzenle')
            else: return redirect('anasayfa')
        else: messages.error(request, "Hatalı giriş.")
    return render(request, 'giris.html')
def cikis_yap(request): logout(request); return redirect('anasayfa')
def kayit_ol(request):
    if request.method == "POST":
        kullanici_adi = request.POST['username']; sifre = request.POST['password']; isim = request.POST['isim']; rol = request.POST['rol']
        if User.objects.filter(username=kullanici_adi).exists(): messages.error(request, "Kullanıcı adı dolu."); return render(request, 'kayit.html')
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
        if form.is_valid(): yeni = form.save(commit=False); yeni.menajer = menajer; yeni.save(); return redirect('menajer_panel')
    else: form = SporcuForm()
    return render(request, 'menajer_form.html', {'form': form, 'baslik': 'Yeni Oyuncu'})
@login_required
def menajer_oyuncu_duzenle(request, pk):
    try: menajer = request.user.menajer; sporcu = get_object_or_404(Sporcu, pk=pk, menajer=menajer)
    except: return redirect('anasayfa')
    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES, instance=sporcu)
        if form.is_valid(): form.save(); return redirect('menajer_panel')
    else: form = SporcuForm(instance=sporcu)
    return render(request, 'menajer_form.html', {'form': form, 'baslik': 'Düzenle'})
"""

# --- 2. URLS (Yeni Yol Eklendi) ---
URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    path('haber/<int:pk>/', haber_detay, name='haber_detay'),
    path('karsilastir/', karsilastir, name='karsilastir'), # YENİ
    
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

# --- 3. HTML: KARŞILAŞTIRMA SAYFASI ---
KARSILASTIR_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ p1.isim }} vs {{ p2.isim }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .winner { background-color: #dcfce7; border-color: #22c55e; color: #15803d; font-weight: bold; }
        .loser { background-color: #fee2e2; border-color: #ef4444; opacity: 0.7; }
    </style>
</head>
<body class="bg-gray-100 font-sans pb-12">
    <nav class="bg-white shadow p-4 mb-8">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <a href="/" class="text-gray-500 hover:text-orange-500">← Geri</a>
        </div>
    </nav>

    <div class="container mx-auto px-4">
        <h1 class="text-3xl font-bold text-center text-indigo-900 mb-2">⚔️ Karşılaştırma</h1>
        <div class="flex justify-center items-center gap-4 mb-8">
            <span class="text-xl font-bold text-gray-600">{{ p1.isim }}</span>
            <span class="bg-orange-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">VS</span>
            <span class="text-xl font-bold text-gray-600">{{ p2.isim }}</span>
        </div>

        <div class="grid grid-cols-2 gap-4 md:gap-12 max-w-4xl mx-auto">
            
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="h-64 bg-gray-200 relative">
                    {% if p1.profil_fotografi %}
                        <img src="{{ p1.profil_fotografi.url }}" class="w-full h-full object-cover">
                    {% else %}
                        <div class="w-full h-full flex items-center justify-center text-gray-400">Görsel Yok</div>
                    {% endif %}
                    <div class="absolute bottom-0 left-0 w-full bg-black/60 p-2 text-center text-white font-bold">{{ p1.isim }}</div>
                </div>
                <div class="p-4 space-y-2">
                    <div class="text-center text-sm text-gray-500 mb-4">{{ p1.kulup.isim }} | {{ p1.get_mevki_display }}</div>
                    
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.boy == 1 %}winner{% elif analiz.boy == 2 %}loser{% endif %}">
                        <span>Boy</span>
                        <span>{{ p1.boy }} cm</span>
                    </div>
                    
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.smac == 1 %}winner{% elif analiz.smac == 2 %}loser{% endif %}">
                        <span>Smaç</span>
                        <span>{{ p1.smac_yuksekligi|default:"-" }} cm</span>
                    </div>

                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.blok == 1 %}winner{% elif analiz.blok == 2 %}loser{% endif %}">
                        <span>Blok</span>
                        <span>{{ p1.blok_yuksekligi|default:"-" }} cm</span>
                    </div>

                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.deger == 1 %}winner{% elif analiz.deger == 2 %}loser{% endif %}">
                        <span>Değer</span>
                        <span>€ {{ p1.piyasa_degeri|default:"-" }}</span>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="h-64 bg-gray-200 relative">
                    {% if p2.profil_fotografi %}
                        <img src="{{ p2.profil_fotografi.url }}" class="w-full h-full object-cover">
                    {% else %}
                        <div class="w-full h-full flex items-center justify-center text-gray-400">Görsel Yok</div>
                    {% endif %}
                    <div class="absolute bottom-0 left-0 w-full bg-black/60 p-2 text-center text-white font-bold">{{ p2.isim }}</div>
                </div>
                <div class="p-4 space-y-2">
                    <div class="text-center text-sm text-gray-500 mb-4">{{ p2.kulup.isim }} | {{ p2.get_mevki_display }}</div>
                    
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.boy == 2 %}winner{% elif analiz.boy == 1 %}loser{% endif %}">
                        <span>Boy</span>
                        <span>{{ p2.boy }} cm</span>
                    </div>
                    
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.smac == 2 %}winner{% elif analiz.smac == 1 %}loser{% endif %}">
                        <span>Smaç</span>
                        <span>{{ p2.smac_yuksekligi|default:"-" }} cm</span>
                    </div>

                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.blok == 2 %}winner{% elif analiz.blok == 1 %}loser{% endif %}">
                        <span>Blok</span>
                        <span>{{ p2.blok_yuksekligi|default:"-" }} cm</span>
                    </div>

                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.deger == 2 %}winner{% elif analiz.deger == 1 %}loser{% endif %}">
                        <span>Değer</span>
                        <span>€ {{ p2.piyasa_degeri|default:"-" }}</span>
                    </div>
                </div>
            </div>

        </div>
        
        <div class="text-center mt-8">
            <a href="/" class="bg-indigo-900 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-800">Yeni Karşılaştırma Yap</a>
        </div>
    </div>
</body>
</html>
"""

# --- 4. HTML: INDEX'E EKLEME (VS Kutusu) ---
# Index sayfasının en üstüne Karşılaştırma kutusu ekliyoruz
INDEX_HTML_PART = """
        <div class="bg-gradient-to-r from-indigo-900 to-purple-900 rounded-xl shadow-xl p-6 mb-8 text-white">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
                <span class="bg-orange-500 p-1 rounded text-xs">YENİ</span> ⚔️ Oyuncu Karşılaştır
            </h2>
            <form action="{% url 'karsilastir' %}" method="GET" class="flex flex-col md:flex-row gap-4 items-center">
                <div class="flex-1 w-full">
                    <select name="p1" class="w-full p-3 rounded-lg text-gray-800 focus:outline-none border-2 border-transparent focus:border-orange-500">
                        <option value="">1. Oyuncuyu Seç</option>
                        {% for s in tum_sporcular %}
                            <option value="{{ s.id }}">{{ s.isim }} ({{ s.kulup.isim }})</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="font-black text-2xl text-orange-500 bg-white rounded-full w-10 h-10 flex items-center justify-center shadow-lg">VS</div>
                
                <div class="flex-1 w-full">
                    <select name="p2" class="w-full p-3 rounded-lg text-gray-800 focus:outline-none border-2 border-transparent focus:border-orange-500">
                        <option value="">2. Oyuncuyu Seç</option>
                        {% for s in tum_sporcular %}
                            <option value="{{ s.id }}">{{ s.isim }} ({{ s.kulup.isim }})</option>
                        {% endfor %}
                    </select>
                </div>
                
                <button type="submit" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-8 rounded-lg shadow-md transition w-full md:w-auto">
                    Kıyasla
                </button>
            </form>
        </div>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Güncellendi: {path}")

def main():
    print("🚀 VS MODU Yükleniyor...\n")
    write_file('core/views.py', VIEWS_CODE)
    write_file('volleymarkt/urls.py', URLS_CODE)
    write_file('core/templates/karsilastir.html', KARSILASTIR_HTML)
    
    # Index dosyasını okuyup VS kutusunu doğru yere ekleyelim
    with open('core/templates/index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Eğer zaten eklenmediyse ekle
    if "VS MODU KUTUSU" not in index_content:
        # Navbar'dan hemen sonraya ekle
        search_str = '<div class="container mx-auto px-4 py-8">'
        if search_str in index_content:
            new_content = index_content.replace(search_str, search_str + INDEX_HTML_PART)
            write_file('core/templates/index.html', new_content)
            print("✅ Index sayfasına VS kutusu eklendi.")
    
    print("\n🎉 İŞLEM TAMAM! 'python manage.py runserver' ile test et.")

if __name__ == '__main__':
    main()