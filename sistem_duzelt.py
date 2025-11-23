import os

# --- 1. AYARLAR (Türkçe Dil ve Saat) ---
def update_settings():
    settings_path = 'volleymarkt/settings.py'
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dili ve Saati Değiştir
    content = content.replace("LANGUAGE_CODE = 'en-us'", "LANGUAGE_CODE = 'tr'")
    content = content.replace("TIME_ZONE = 'UTC'", "TIME_ZONE = 'Europe/Istanbul'")
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Ayarlar: Dil Türkçe, Saat İstanbul yapıldı.")

# --- 2. URLS (Haberler Sayfası Eklendi) ---
URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('haberler/', tum_haberler, name='tum_haberler'), # YENİ
    path('haber/<int:pk>/', haber_detay, name='haber_detay'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    path('karsilastir/', karsilastir, name='karsilastir'),
    
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

# --- 3. VIEWS (Tüm Haberler Eklendi) ---
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Kulup, MEVKILER, Menajer, Haber
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

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
    tum_sporcular = Sporcu.objects.all().order_by('isim') # VS modu için
    
    # 3. HABERLER VE REKLAM MANTIĞI
    mansetler_raw = list(Haber.objects.filter(manset_mi=True)[:10])
    reklam_1 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/FF5733/FFFFFF?text=REKLAM+ALANI+1', 'link': '#'}
    reklam_2 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/33FF57/FFFFFF?text=REKLAM+ALANI+2', 'link': '#'}
    
    mansetler = []
    sayac = 0
    for h in mansetler_raw:
        mansetler.append(h)
        sayac += 1
        if sayac == 2: mansetler.append(reklam_1)
        if sayac == 5: mansetler.append(reklam_2)

    son_haberler = Haber.objects.all().order_by('-tarih')[:6]

    # 4. GRAFİK VERİLERİ
    mevki_data = Sporcu.objects.values('mevki').annotate(total=Count('id'))
    mevki_labels = [m['mevki'] for m in mevki_data]
    mevki_counts = [m['total'] for m in mevki_data]

    en_uzunlar = Sporcu.objects.filter(boy__isnull=False).order_by('-boy')[:5]
    uzun_labels = [s.isim for s in en_uzunlar]
    uzun_values = [s.boy for s in en_uzunlar]

    en_degerliler = Sporcu.objects.filter(piyasa_degeri__isnull=False).order_by('-piyasa_degeri')[:5]
    deger_labels = [s.isim for s in en_degerliler]
    deger_values = [s.piyasa_degeri for s in en_degerliler]

    context = {
        'sporcular': sporcular,
        'tum_sporcular': tum_sporcular,
        'puan_tablosu': puan_tablosu,
        'maclar': maclar,
        'kulupler': Kulup.objects.all(),
        'mevkiler': MEVKILER,
        'secili_isim': isim,
        'secili_kulup': int(kulup_id) if kulup_id else None,
        'secili_mevki': mevki,
        'secili_min_boy': min_boy,
        'secili_max_boy': max_boy,
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

def tum_haberler(request):
    # Tüm haberleri listele
    haberler = Haber.objects.all().order_by('-tarih')
    return render(request, 'haberler.html', {'haberler': haberler})

def karsilastir(request):
    id1 = request.GET.get('p1')
    id2 = request.GET.get('p2')
    if not id1 or not id2:
        messages.warning(request, "Lütfen karşılaştırmak için iki oyuncu seçin.")
        return redirect('anasayfa')
    p1 = get_object_or_404(Sporcu, id=id1)
    p2 = get_object_or_404(Sporcu, id=id2)
    def kiyasla(v1, v2):
        if not v1 and not v2: return 0
        if not v1: return 2
        if not v2: return 1
        if v1 > v2: return 1
        elif v2 > v1: return 2
        return 0
    analiz = {
        'boy': kiyasla(p1.boy, p2.boy),
        'smac': kiyasla(p1.smac_yuksekligi, p2.smac_yuksekligi),
        'blok': kiyasla(p1.blok_yuksekligi, p2.blok_yuksekligi),
        'deger': kiyasla(p1.piyasa_degeri, p2.piyasa_degeri),
    }
    return render(request, 'karsilastir.html', {'p1': p1, 'p2': p2, 'analiz': analiz})

# --- Diğer Standart Views ---
def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})
def haber_detay(request, pk):
    haber = get_object_or_404(Haber, pk=pk)
    benzer = Haber.objects.filter(kategori=haber.kategori).exclude(id=haber.id)[:3]
    return render(request, 'haber_detay.html', {'haber': haber, 'benzer_haberler': benzer})
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
        if form.is_valid(): y=form.save(commit=False); y.menajer=menajer; y.save(); return redirect('menajer_panel')
    else: form = SporcuForm()
    return render(request, 'menajer_form.html', {'form': form, 'baslik': 'Yeni'})
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

# --- 4. HTML PARÇALARI (Header & Footer) ---
NAVBAR_HTML = """
<nav class="bg-white shadow-md sticky top-0 z-50 font-sans">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="flex items-center gap-2 group">
                <div class="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg group-hover:rotate-12 transition transform">V</div>
                <div class="flex flex-col">
                    <span class="text-xl font-extrabold text-indigo-900 leading-none">Volley<span class="text-orange-500">Markt</span></span>
                    <span class="text-[10px] text-gray-400 tracking-widest uppercase font-semibold">Türkiye</span>
                </div>
            </a>

            <div class="hidden md:flex space-x-8">
                <a href="/" class="text-gray-700 hover:text-orange-500 font-bold transition border-b-2 border-transparent hover:border-orange-500 py-1">Anasayfa</a>
                <a href="{% url 'tum_haberler' %}" class="text-gray-700 hover:text-orange-500 font-bold transition border-b-2 border-transparent hover:border-orange-500 py-1">Haberler</a>
                <a href="/?isim=&kulup=&mevki=&min_boy=&max_boy=" class="text-gray-700 hover:text-orange-500 font-bold transition border-b-2 border-transparent hover:border-orange-500 py-1">Oyuncular</a>
                <a href="#puan-durumu" class="text-gray-700 hover:text-orange-500 font-bold transition border-b-2 border-transparent hover:border-orange-500 py-1">Puan Durumu</a>
            </div>

            <div class="flex items-center gap-3">
                {% if user.is_authenticated %}
                    {% if user.menajer %}
                        <a href="{% url 'menajer_panel' %}" class="bg-indigo-900 text-white px-4 py-2 rounded-lg hover:bg-indigo-800 text-sm font-bold shadow flex items-center gap-2">💼 Panel</a>
                    {% elif user.sporcu %}
                        <a href="{% url 'profil_duzenle' %}" class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 text-sm font-bold shadow flex items-center gap-2">✏️ Profil</a>
                    {% endif %}
                    <a href="{% url 'cikis' %}" class="text-gray-400 hover:text-red-500 font-medium text-sm">Çıkış</a>
                {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900 font-bold hover:text-orange-500 transition">Giriş</a>
                    <a href="{% url 'kayit' %}" class="bg-indigo-50 text-indigo-900 px-4 py-2 rounded-lg hover:bg-indigo-100 font-bold text-sm transition border border-indigo-200">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
"""

FOOTER_HTML = """
<footer class="bg-gray-900 text-gray-300 mt-20 border-t-4 border-orange-500">
    <div class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="col-span-1 md:col-span-2">
                <h2 class="text-2xl font-bold text-white mb-4">Volley<span class="text-orange-500">Markt</span></h2>
                <p class="text-sm leading-relaxed mb-6 max-w-md">
                    Türkiye'nin en kapsamlı voleybol veri tabanı. Sultanlar Ligi ve Efeler Ligi'nden güncel transferler, 
                    istatistikler, maç sonuçları ve oyuncu profilleri tek adreste.
                </p>
                <div class="flex gap-4">
                    <a href="#" class="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-500 hover:text-white transition text-lg">𝕏</a>
                    <a href="#" class="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-pink-600 hover:text-white transition text-lg">📷</a>
                    <a href="#" class="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-red-600 hover:text-white transition text-lg">▶</a>
                </div>
            </div>
            <div>
                <h3 class="text-white font-bold text-lg mb-4 border-b border-gray-700 pb-2 inline-block">Hızlı Erişim</h3>
                <ul class="space-y-2 text-sm">
                    <li><a href="/" class="hover:text-orange-400 transition">→ Anasayfa</a></li>
                    <li><a href="{% url 'tum_haberler' %}" class="hover:text-orange-400 transition">→ Haber Merkezi</a></li>
                    <li><a href="#" class="hover:text-orange-400 transition">→ Puan Durumu</a></li>
                    <li><a href="#" class="hover:text-orange-400 transition">→ Transferler</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-white font-bold text-lg mb-4 border-b border-gray-700 pb-2 inline-block">İletişim</h3>
                <ul class="space-y-3 text-sm">
                    <li class="flex items-center gap-3"><span class="text-orange-500">📍</span> İstanbul, Türkiye</li>
                    <li class="flex items-center gap-3"><span class="text-orange-500">📧</span> info@volleymarkt.com</li>
                    <li class="flex items-center gap-3"><span class="text-orange-500">📞</span> +90 (212) 555 00 00</li>
                </ul>
            </div>
        </div>
        <div class="border-t border-gray-800 mt-12 pt-8 text-center text-xs text-gray-500">
            &copy; 2025 VolleyMarkt Turkey. Tüm hakları saklıdır. Veriler TVF ve Wikipedia kaynaklıdır.
        </div>
    </div>
</footer>
"""

# --- 5. YENİ INDEX HTML (Her Şey Dahil) ---
INDEX_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt - Türkiye'nin Voleybol Platformu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        .swiper {{ width: 100%; height: 100%; }}
        .swiper-slide {{ display: flex; justify-content: center; align-items: center; background: #000; }}
        .swiper-slide img {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }}
    </style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    {NAVBAR_HTML}

    <main class="flex-grow container mx-auto px-4 py-8">
        
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
            <div class="lg:col-span-3 h-[400px] md:h-[500px] relative rounded-2xl shadow-xl overflow-hidden bg-black">
                {{% if mansetler %}}
                <div class="swiper mySwiper h-full">
                    <div class="swiper-wrapper">
                        {{% for item in mansetler %}}
                            {{% if item.is_ad %}}
                                <div class="swiper-slide relative bg-gray-900">
                                    <img src="{{{{ item.image }}}}" alt="Reklam">
                                    <div class="absolute top-4 right-4 bg-white/20 text-white px-2 py-1 rounded text-xs border border-white/30">REKLAM</div>
                                </div>
                            {{% else %}}
                                <div class="swiper-slide relative">
                                    {{% if item.resim %}}<img src="{{{{ item.resim.url }}}}" alt="{{{{ item.baslik }}}}">{{% endif %}}
                                    <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black via-black/80 to-transparent p-8 md:p-12 text-left">
                                        <span class="bg-orange-600 text-white text-xs font-bold px-3 py-1 rounded-full mb-3 inline-block uppercase tracking-wide shadow">{{{{ item.get_kategori_display }}}}</span>
                                        <h2 class="text-2xl md:text-4xl font-extrabold text-white mb-3 leading-tight drop-shadow-lg">{{{{ item.baslik }}}}</h2>
                                        <a href="{{% url 'haber_detay' item.id %}}" class="inline-flex items-center gap-2 text-white border-b-2 border-orange-500 pb-1 hover:text-orange-400 transition font-bold text-sm">Haberi Oku <span>→</span></a>
                                    </div>
                                </div>
                            {{% endif %}}
                        {{% endfor %}}
                    </div>
                    <div class="swiper-button-next text-white/80 hover:text-white"></div>
                    <div class="swiper-button-prev text-white/80 hover:text-white"></div>
                    <div class="swiper-pagination"></div>
                </div>
                {{% else %}}
                    <div class="flex items-center justify-center h-full text-white font-bold text-xl">Haber bekleniyor...</div>
                {{% endif %}}
            </div>
            <div class="hidden lg:block lg:col-span-1 h-[500px]">
                <div class="bg-gray-200 h-full rounded-xl flex items-center justify-center relative group overflow-hidden shadow-lg">
                    <img src="https://via.placeholder.com/400x600/222/FFF?text=SPONSOR" class="w-full h-full object-cover">
                    <div class="absolute top-2 right-2 bg-black/30 text-white text-[10px] px-2 rounded">REKLAM</div>
                </div>
            </div>
        </div>

        <div class="bg-gradient-to-r from-indigo-900 to-blue-900 rounded-2xl shadow-xl p-6 md:p-8 mb-12 text-white relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-16 -mt-16 blur-2xl"></div>
            <div class="relative z-10">
                <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
                    <span class="bg-orange-500 text-white p-1.5 rounded-lg shadow-lg">⚔️</span> Oyuncu Karşılaştır
                </h2>
                <form action="{{% url 'karsilastir' %}}" method="GET" class="flex flex-col md:flex-row gap-4 items-center">
                    <select name="p1" class="w-full p-4 rounded-xl text-gray-900 font-medium focus:outline-none focus:ring-4 focus:ring-orange-500/50">
                        <option value="">1. Oyuncuyu Seç</option>
                        {{% for s in tum_sporcular %}}<option value="{{{{ s.id }}}}">{{{{ s.isim }}}} ({{{{ s.kulup.isim }}}})</option>{{% endfor %}}
                    </select>
                    <div class="bg-white text-orange-600 font-black text-xl rounded-full w-12 h-12 flex items-center justify-center shadow-lg shrink-0">VS</div>
                    <select name="p2" class="w-full p-4 rounded-xl text-gray-900 font-medium focus:outline-none focus:ring-4 focus:ring-orange-500/50">
                        <option value="">2. Oyuncuyu Seç</option>
                        {{% for s in tum_sporcular %}}<option value="{{{{ s.id }}}}">{{{{ s.isim }}}} ({{{{ s.kulup.isim }}}})</option>{{% endfor %}}
                    </select>
                    <button type="submit" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-10 rounded-xl shadow-lg transition w-full md:w-auto hover:scale-105">Kıyasla</button>
                </form>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div class="lg:col-span-3">
                <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                    <h3 class="font-bold text-gray-800 mb-4 flex items-center gap-2">🔍 Detaylı Arama</h3>
                    <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <input type="text" name="isim" value="{{{{ secili_isim|default:'' }}}}" placeholder="İsim Ara..." class="border p-2.5 rounded-lg w-full md:col-span-4 focus:border-indigo-500 outline-none">
                        <select name="kulup" class="border p-2.5 rounded-lg w-full bg-white"><option value="">Kulüp</option>{{% for k in kulupler %}}<option value="{{{{ k.id }}}}" {{% if k.id == secili_kulup %}}selected{{% endif %}}>{{{{ k.isim }}}}</option>{{% endfor %}}</select>
                        <select name="mevki" class="border p-2.5 rounded-lg w-full bg-white"><option value="">Mevki</option>{{% for k,v in mevkiler %}}<option value="{{{{ k }}}}" {{% if k == secili_mevki %}}selected{{% endif %}}>{{{{ v }}}}</option>{{% endfor %}}</select>
                        <div class="flex gap-2"><input type="number" name="min_boy" value="{{{{ secili_min_boy|default:'' }}}}" placeholder="Min" class="w-1/2 border p-2.5 rounded-lg"><input type="number" name="max_boy" value="{{{{ secili_max_boy|default:'' }}}}" placeholder="Max" class="w-1/2 border p-2.5 rounded-lg"></div>
                        <button type="submit" class="bg-indigo-900 text-white font-bold rounded-lg p-2.5">Ara</button>
                    </form>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
                    {{% for sporcu in sporcular %}}
                    <a href="{{% url 'sporcu_detay' sporcu.id %}}" class="bg-white rounded-xl shadow-sm hover:shadow-xl transition duration-300 group overflow-hidden border border-gray-100">
                        <div class="h-56 bg-gray-200 relative">
                            {{% if sporcu.profil_fotografi %}}<img src="{{{{ sporcu.profil_fotografi.url }}}}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-700">{{% endif %}}
                            <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/80 to-transparent p-4 pt-10">
                                <h3 class="text-white font-bold text-lg leading-none">{{{{ sporcu.isim }}}}</h3>
                                <p class="text-orange-400 text-xs font-bold mt-1">{{{{ sporcu.kulup.isim|default:"-" }}}}</p>
                            </div>
                        </div>
                        <div class="p-3 flex justify-between items-center text-sm bg-white">
                            <span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-bold">{{{{ sporcu.get_mevki_display }}}}</span>
                            <span class="font-bold text-indigo-900">{{{{ sporcu.boy }}}} cm</span>
                        </div>
                    </a>
                    {{% empty %}}<p class="col-span-3 text-center text-gray-400 py-12">Sonuç yok.</p>{{% endfor %}}
                </div>
            </div>

            <div class="space-y-8">
                <div id="puan-durumu" class="bg-white rounded-xl shadow overflow-hidden border border-gray-200">
                    <div class="bg-indigo-900 text-white p-4 font-bold text-center uppercase tracking-widest text-sm">Sultanlar Ligi</div>
                    <table class="w-full text-sm">
                        {{% for sira in puan_tablosu %}}
                        <tr class="border-b hover:bg-indigo-50 transition"><td class="p-3 font-medium flex gap-2"><span class="text-gray-400 w-4">{{{{ forloop.counter }}}}.</span> {{{{ sira.kulup.isim }}}}</td><td class="p-3 font-bold text-right text-indigo-900">{{{{ sira.puan|floatformat:0 }}}}</td></tr>
                        {{% endfor %}}
                    </table>
                </div>

                <div class="bg-white rounded-xl shadow border border-gray-200 p-5">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2 uppercase text-xs tracking-wide text-gray-500">Son Haberler</h3>
                    <div class="space-y-4">
                        {{% for haber in son_haberler %}}
                        <a href="{{% url 'haber_detay' haber.id %}}" class="flex gap-3 group">
                            <div class="w-16 h-16 bg-gray-200 rounded-lg overflow-hidden shrink-0">
                                {{% if haber.resim %}}<img src="{{{{ haber.resim.url }}}}" class="w-full h-full object-cover group-hover:scale-110 transition">{{% endif %}}
                            </div>
                            <div>
                                <h4 class="text-sm font-bold text-gray-800 group-hover:text-orange-600 leading-snug mb-1 line-clamp-2">{{{{ haber.baslik }}}}</h4>
                                <span class="text-[10px] text-gray-400">{{{{ haber.tarih|date:"d F Y" }}}}</span>
                            </div>
                        </a>
                        {{% endfor %}}
                        <a href="{{% url 'tum_haberler' %}}" class="block text-center text-sm font-bold text-indigo-600 hover:text-indigo-800 mt-4">Tüm Haberleri Gör →</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="mt-16 border-t pt-12">
            <h2 class="text-2xl font-bold text-center text-indigo-900 mb-10">📊 Lig İstatistikleri</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white p-6 rounded-xl shadow border border-gray-100"><h3 class="text-center font-bold text-gray-600 mb-4">Mevki Dağılımı</h3><canvas id="mevkiChart"></canvas></div>
                <div class="bg-white p-6 rounded-xl shadow border border-gray-100"><h3 class="text-center font-bold text-gray-600 mb-4">En Uzunlar</h3><canvas id="boyChart"></canvas></div>
                <div class="bg-white p-6 rounded-xl shadow border border-gray-100"><h3 class="text-center font-bold text-gray-600 mb-4">En Değerliler</h3><canvas id="degerChart"></canvas></div>
            </div>
        </div>
    </main>

    {FOOTER_HTML}

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        new Swiper(".mySwiper", {{ spaceBetween: 0, effect: "fade", autoplay: {{ delay: 4000 }}, pagination: {{ el: ".swiper-pagination", clickable: true }}, navigation: {{ nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" }} }});
        new Chart(document.getElementById('mevkiChart'), {{ type: 'doughnut', data: {{ labels: {{ mevki_labels|safe }}, datasets: [{{ data: {{ mevki_counts|safe }}, backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'] }}] }} }});
        new Chart(document.getElementById('boyChart'), {{ type: 'bar', data: {{ labels: {{ uzun_labels|safe }}, datasets: [{{ label: 'Boy', data: {{ uzun_values|safe }}, backgroundColor: '#36A2EB' }}] }}, options: {{ indexAxis: 'y' }} }});
        new Chart(document.getElementById('degerChart'), {{ type: 'bar', data: {{ labels: {{ deger_labels|safe }}, datasets: [{{ label: 'Değer (€)', data: {{ deger_values|safe }}, backgroundColor: '#4BC0C0' }}] }} }});
    </script>
</body>
</html>
"""

# --- 6. YENİ SAYFA: HABERLER.HTML ---
HABERLER_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Tüm Haberler - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    {NAVBAR_HTML}

    <main class="flex-grow container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-indigo-900 mb-8 border-l-8 border-orange-500 pl-4">Haber Merkezi</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {{% for haber in haberler %}}
            <a href="{{% url 'haber_detay' haber.id %}}" class="bg-white rounded-xl shadow hover:shadow-xl transition duration-300 group overflow-hidden flex flex-col h-full">
                <div class="h-56 overflow-hidden relative">
                    {{% if haber.resim %}}
                        <img src="{{{{ haber.resim.url }}}}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                    {{% else %}}
                        <div class="w-full h-full bg-gray-200 flex items-center justify-center text-gray-400">Görsel Yok</div>
                    {{% endif %}}
                    <div class="absolute top-3 right-3 bg-white/90 text-indigo-900 text-xs font-bold px-2 py-1 rounded shadow">{{{{ haber.get_kategori_display }}}}</div>
                </div>
                <div class="p-6 flex flex-col flex-grow">
                    <div class="text-xs text-gray-400 mb-2 flex items-center gap-1">
                        <span>📅</span> {{{{ haber.tarih|date:"d F Y" }}}}
                        <span>•</span>
                        <span>{{{{ haber.tarih|date:"H:i" }}}}</span>
                    </div>
                    <h2 class="text-xl font-bold text-gray-900 mb-3 leading-snug group-hover:text-orange-600 transition">{{{{ haber.baslik }}}}</h2>
                    <p class="text-gray-600 text-sm line-clamp-3 mb-4 flex-grow">{{{{ haber.ozet }}}}</p>
                    <span class="text-indigo-600 font-bold text-sm flex items-center gap-1">Devamını Oku <span>→</span></span>
                </div>
            </a>
            {{% endfor %}}
        </div>
    </main>

    {FOOTER_HTML}
</body>
</html>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Güncellendi: {path}")

def main():
    print("🚀 SİSTEM RESTORASYONU BAŞLATILIYOR...\n")
    
    update_settings() # Settings'i düzelt
    write_file('volleymarkt/urls.py', URLS_CODE) # URL'leri ekle
    write_file('core/views.py', VIEWS_CODE) # View'ları güncelle
    write_file('core/templates/index.html', INDEX_HTML) # Ana sayfayı onar
    write_file('core/templates/haberler.html', HABERLER_HTML) # Yeni sayfayı ekle
    
    print("\n🎉 İŞLEM TAMAM! Siteyi yenile (F5). Her şey Türkçe ve yerli yerinde olmalı.")

if __name__ == '__main__':
    main()