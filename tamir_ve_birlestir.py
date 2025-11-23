import os

# ==========================================
# 1. ORTAK PARÇALAR
# ==========================================
NAVBAR_HTML = """
<nav class="bg-white/95 backdrop-blur-md shadow-md sticky top-0 z-50 font-sans border-t-4 border-orange-500">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="flex items-center gap-2 group">
                <div class="w-11 h-11 bg-gradient-to-br from-orange-500 via-red-500 to-purple-600 rounded-2xl rotate-3 flex items-center justify-center text-white font-extrabold text-2xl shadow-lg group-hover:rotate-12 transition">V</div>
                <div class="flex flex-col">
                    <span class="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-orange-600 leading-none">Volley<span class="text-orange-500">Markt</span></span>
                    <span class="text-[10px] text-gray-400 tracking-[0.2em] uppercase font-bold">Türkiye</span>
                </div>
            </a>
            <div class="hidden md:flex space-x-1 items-center bg-gray-100/50 p-1 rounded-full">
                <a href="/" class="px-4 py-2 rounded-full text-gray-700 font-bold hover:bg-white hover:text-orange-600 hover:shadow-sm transition">Anasayfa</a>
                <a href="/haberler/" class="px-4 py-2 rounded-full text-gray-700 font-bold hover:bg-white hover:text-orange-600 hover:shadow-sm transition">Haberler</a>
                <a href="/#oyuncular" class="px-4 py-2 rounded-full text-gray-700 font-bold hover:bg-white hover:text-orange-600 hover:shadow-sm transition">Oyuncular</a>
            </div>
            <div class="flex items-center gap-3">
                {% if user.is_authenticated %}
                    {% if user.menajer %}<a href="/menajer-panel/" class="bg-indigo-900 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">💼 Panel</a>
                    {% elif user.sporcu %}<a href="/profil-duzenle/" class="bg-orange-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">✏️ Profil</a>{% endif %}
                    <a href="/cikis/" class="text-red-500 font-bold text-sm">Çıkış</a>
                {% else %}
                    <a href="/giris/" class="text-indigo-900 font-bold">Giriş</a>
                    <a href="/kayit/" class="bg-indigo-900 text-white px-5 py-2 rounded-full font-bold text-sm">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
"""

FOOTER_HTML = """
<footer class="bg-gradient-to-b from-gray-900 to-indigo-950 text-gray-300 mt-24 border-t-4 border-orange-500">
    <div class="container mx-auto px-4 py-16">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div class="col-span-1 md:col-span-2">
                <h2 class="text-3xl font-extrabold text-white mb-4">Volley<span class="text-orange-500">Markt</span></h2>
                <p class="text-sm leading-relaxed mb-6 opacity-80">Türkiye'nin en gelişmiş voleybol veri platformu.</p>
                <div class="flex gap-4">
                    <a href="#" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-orange-500 hover:text-white transition">𝕏</a>
                    <a href="#" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-orange-500 hover:text-white transition">📷</a>
                </div>
            </div>
            <div>
                <h3 class="text-white font-bold text-lg mb-4 border-b-2 border-orange-500 pb-2 inline-block">Hızlı Linkler</h3>
                <ul class="space-y-2 text-sm">
                    <li><a href="/" class="hover:text-orange-400 transition">→ Anasayfa</a></li>
                    <li><a href="/haberler/" class="hover:text-orange-400 transition">→ Haber Merkezi</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-white font-bold text-lg mb-4 border-b-2 border-orange-500 pb-2 inline-block">İletişim</h3>
                <p class="text-sm">İstanbul, Türkiye</p>
                <p class="text-sm mt-2">info@volleymarkt.com</p>
            </div>
        </div>
        <div class="border-t border-white/10 mt-12 pt-8 text-center text-xs opacity-50">&copy; 2025 VolleyMarkt. Tüm hakları saklıdır.</div>
    </div>
</footer>
"""

# ==========================================
# 2. VIEWS CODE (Hatasız)
# ==========================================
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Kulup, MEVKILER, Menajer, Haber, Yorum, Anket, Secenek
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def anasayfa(request):
    sporcular = Sporcu.objects.all()
    isim = request.GET.get('isim'); kulup_id = request.GET.get('kulup'); mevki = request.GET.get('mevki'); min_boy = request.GET.get('min_boy'); max_boy = request.GET.get('max_boy')
    
    if isim: sporcular = sporcular.filter(isim__icontains=isim)
    if kulup_id: sporcular = sporcular.filter(kulup_id=kulup_id)
    if mevki: sporcular = sporcular.filter(mevki=mevki)
    if min_boy: sporcular = sporcular.filter(boy__gte=min_boy)
    if max_boy: sporcular = sporcular.filter(boy__lte=max_boy)

    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    maclar = Mac.objects.all().order_by('tarih')[:5]
    tum_sporcular = Sporcu.objects.all().order_by('isim')
    
    mansetler_raw = list(Haber.objects.filter(manset_mi=True)[:10])
    reklam_1 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/FF5733/FFFFFF?text=REKLAM+ALANI+1', 'link': '#'}
    reklam_2 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/33FF57/FFFFFF?text=REKLAM+ALANI+2', 'link': '#'}
    mansetler = []
    sayac = 0
    for h in mansetler_raw:
        mansetler.append(h); sayac += 1
        if sayac == 2: mansetler.append(reklam_1)
        if sayac == 5: mansetler.append(reklam_2)

    son_haberler = Haber.objects.all().order_by('-tarih')[:6]
    aktif_anket = Anket.objects.filter(aktif_mi=True).last()

    mevki_data = Sporcu.objects.values('mevki').annotate(total=Count('id'))
    mevki_labels = [m['mevki'] for m in mevki_data]; mevki_counts = [m['total'] for m in mevki_data]
    en_uzunlar = Sporcu.objects.filter(boy__isnull=False).order_by('-boy')[:5]
    uzun_labels = [s.isim for s in en_uzunlar]; uzun_values = [s.boy for s in en_uzunlar]
    en_degerliler = Sporcu.objects.filter(piyasa_degeri__isnull=False).order_by('-piyasa_degeri')[:5]
    deger_labels = [s.isim for s in en_degerliler]; deger_values = [s.piyasa_degeri for s in en_degerliler]

    context = {
        'sporcular': sporcular, 'tum_sporcular': tum_sporcular, 'puan_tablosu': puan_tablosu, 'maclar': maclar,
        'kulupler': Kulup.objects.all(), 'mevkiler': MEVKILER, 'secili_isim': isim, 'secili_kulup': int(kulup_id) if kulup_id else None,
        'secili_mevki': mevki, 'secili_min_boy': min_boy, 'secili_max_boy': max_boy,
        'mansetler': mansetler, 'son_haberler': son_haberler, 'aktif_anket': aktif_anket,
        'mevki_labels': mevki_labels, 'mevki_counts': mevki_counts,
        'uzun_labels': uzun_labels, 'uzun_values': uzun_values,
        'deger_labels': deger_labels, 'deger_values': deger_values,
    }
    return render(request, 'index.html', context)

def karsilastir(request):
    id1 = request.GET.get('p1'); id2 = request.GET.get('p2')
    if not id1 or not id2: return redirect('anasayfa')
    p1 = get_object_or_404(Sporcu, id=id1); p2 = get_object_or_404(Sporcu, id=id2)
    
    def kiyasla(val1, val2):
        v1 = val1 if val1 is not None else 0
        v2 = val2 if val2 is not None else 0
        if v1 == 0 and v2 == 0: return 0
        if v1 > v2: return 1
        elif v2 > v1: return 2
        return 0

    analiz = {'boy': kiyasla(p1.boy, p2.boy), 'smac': kiyasla(p1.smac_yuksekligi, p2.smac_yuksekligi),
              'blok': kiyasla(p1.blok_yuksekligi, p2.blok_yuksekligi), 'deger': kiyasla(p1.piyasa_degeri, p2.piyasa_degeri)}
    return render(request, 'karsilastir.html', {'p1': p1, 'p2': p2, 'analiz': analiz})

def oy_ver(request, anket_id):
    if request.method == 'POST':
        s = get_object_or_404(Secenek, id=request.POST.get('secenek'))
        s.oy_sayisi += 1; s.save(); messages.success(request, "Oyunuz kaydedildi!")
    return redirect('anasayfa')
def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    if request.method == 'POST':
        if 'yorum_yaz' in request.POST and request.user.is_authenticated: Yorum.objects.create(yazan=request.user, sporcu=sporcu, metin=request.POST.get('metin'))
        elif 'begen' in request.POST and request.user.is_authenticated:
            if request.user in sporcu.begeniler.all(): sporcu.begeniler.remove(request.user)
            else: sporcu.begeniler.add(request.user)
        return redirect('sporcu_detay', pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})
def haber_detay(request, pk): h = get_object_or_404(Haber, pk=pk); b = Haber.objects.filter(kategori=h.kategori).exclude(id=h.id)[:3]; return render(request, 'haber_detay.html', {'haber': h, 'benzer_haberler': b})
def tum_haberler(request): return render(request, 'haberler.html', {'haberler': Haber.objects.all().order_by('-tarih')})
def mac_detay(request, pk): return render(request, 'mac_detay.html', {'mac': get_object_or_404(Mac, pk=pk)})
def giris_yap(request):
    if request.method=="POST":
        f=AuthenticationForm(request, data=request.POST)
        if f.is_valid(): u=f.get_user(); login(request, u); return redirect('menajer_panel' if hasattr(u,'menajer') else 'profil_duzenle' if hasattr(u,'sporcu') else 'anasayfa')
    return render(request, 'giris.html')
def cikis_yap(request): logout(request); return redirect('anasayfa')
def kayit_ol(request):
    if request.method=="POST":
        u=request.POST['username']; p=request.POST['password']; r=request.POST['rol']
        user=User.objects.create_user(username=u, password=p)
        if r=='sporcu': Sporcu.objects.create(user=user, isim=request.POST['isim'])
        else: Menajer.objects.create(user=user, isim=request.POST['isim'])
        login(request, user); return redirect('anasayfa')
    return render(request, 'kayit.html')
@login_required
def profil_duzenle(request):
    try: s=request.user.sporcu
    except: return redirect('anasayfa')
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES, instance=s); f.save() if f.is_valid() else None; return redirect('sporcu_detay', pk=s.id)
    return render(request, 'profil_duzenle.html', {'form': SporcuForm(instance=s)})
@login_required
def menajer_panel(request): return render(request, 'menajer_panel.html', {'menajer': request.user.menajer, 'oyuncular': Sporcu.objects.filter(menajer=request.user.menajer)})
@login_required
def menajer_oyuncu_ekle(request):
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES); y=f.save(commit=False); y.menajer=request.user.menajer; y.save(); return redirect('menajer_panel')
    return render(request, 'menajer_form.html', {'form': SporcuForm(), 'baslik': 'Yeni'})
@login_required
def menajer_oyuncu_duzenle(request, pk):
    s=get_object_or_404(Sporcu, pk=pk, menajer=request.user.menajer)
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES, instance=s); f.save(); return redirect('menajer_panel')
    return render(request, 'menajer_form.html', {'form': SporcuForm(instance=s), 'baslik': 'Düzenle'})
"""

# ==========================================
# 3. HTML ŞABLONLARI (İsimleri Düzeltildi)
# ==========================================

INDEX_HTML_RAW = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; }
        .swiper { width: 100%; height: 100%; }
        .swiper-slide { display: flex; justify-content: center; align-items: center; background: #000; }
        .swiper-slide img { width: 100%; height: 100%; object-fit: cover; opacity: 0.85; }
    </style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    __NAVBAR__
    <main class="flex-grow container mx-auto px-4 py-8">
        {% if messages %}<div class="mb-6">{% for m in messages %}<div class="p-4 rounded-lg bg-green-100 text-green-800 shadow-sm">✅ {{ m }}</div>{% endfor %}</div>{% endif %}

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
            <div class="lg:col-span-3 h-[450px] relative rounded-[2rem] shadow-2xl overflow-hidden bg-black">
                {% if mansetler %}
                <div class="swiper mySwiper h-full"><div class="swiper-wrapper">
                    {% for item in mansetler %}
                        {% if item.is_ad %}
                            <div class="swiper-slide relative bg-gray-900"><img src="{{ item.image }}" class="opacity-60"><div class="absolute top-4 right-4 bg-white/20 text-white px-2 py-1 rounded text-xs">REKLAM</div></div>
                        {% else %}
                            <div class="swiper-slide relative">
                                {% if item.resim %}<img src="{{ item.resim.url }}">{% endif %}
                                <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black p-8 text-left">
                                    <span class="bg-orange-600 text-white text-xs font-bold px-3 py-1 rounded-full">{{ item.get_kategori_display }}</span>
                                    <h2 class="text-3xl font-extrabold text-white">{{ item.baslik }}</h2>
                                </div>
                            </div>
                        {% endif %}
                    {% endfor %}
                </div><div class="swiper-button-next text-white"></div><div class="swiper-button-prev text-white"></div><div class="swiper-pagination"></div></div>
                {% else %}<div class="flex items-center justify-center h-full text-white font-bold text-xl">Haber Bekleniyor...</div>{% endif %}
            </div>
            <div class="hidden lg:block lg:col-span-1 h-[450px] bg-gray-200 rounded-[2rem] flex items-center justify-center shadow-xl"><span class="text-gray-400 font-bold">REKLAM ALANI</span></div>
        </div>

        <div class="bg-gradient-to-r from-indigo-900 to-blue-900 rounded-[2rem] shadow-xl p-8 mb-12 text-white relative overflow-hidden">
            <div class="relative z-10">
                <h2 class="text-2xl font-bold mb-6 flex items-center gap-3"><span class="bg-orange-500 p-2 rounded-lg">⚔️</span> Oyuncu Karşılaştır</h2>
                <form action="/karsilastir/" method="GET" class="flex flex-col md:flex-row gap-4 items-center">
                    <select name="p1" class="w-full p-4 rounded-xl text-gray-900 font-bold"><option value="">1. Oyuncuyu Seç</option>{% for s in tum_sporcular %}<option value="{{ s.id }}">{{ s.isim }}</option>{% endfor %}</select>
                    <div class="text-orange-500 font-black text-2xl bg-white rounded-full w-12 h-12 flex items-center justify-center shadow-lg">VS</div>
                    <select name="p2" class="w-full p-4 rounded-xl text-gray-900 font-bold"><option value="">2. Oyuncuyu Seç</option>{% for s in tum_sporcular %}<option value="{{ s.id }}">{{ s.isim }}</option>{% endfor %}</select>
                    <button class="bg-orange-500 text-white font-bold py-4 px-10 rounded-xl shadow-lg hover:bg-orange-600 transition">KIYASLA</button>
                </form>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div class="lg:col-span-3">
                <div class="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 mb-8">
                    <h3 class="font-bold text-gray-800 mb-4">🔍 Filtrele</h3>
                    <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <input type="text" name="isim" value="{{ secili_isim|default:'' }}" placeholder="İsim..." class="border p-3 rounded-xl w-full md:col-span-4 bg-gray-50">
                        <select name="kulup" class="border p-3 rounded-xl w-full bg-gray-50"><option value="">Kulüp</option>{% for k in kulupler %}<option value="{{ k.id }}">{{ k.isim }}</option>{% endfor %}</select>
                        <select name="mevki" class="border p-3 rounded-xl w-full bg-gray-50"><option value="">Mevki</option>{% for k,v in mevkiler %}<option value="{{ k }}">{{ v }}</option>{% endfor %}</select>
                        <div class="flex gap-2"><input type="number" name="min_boy" placeholder="Min" class="border p-3 rounded-xl w-1/2 bg-gray-50"><input type="number" name="max_boy" placeholder="Max" class="border p-3 rounded-xl w-1/2 bg-gray-50"></div>
                        <button class="bg-indigo-900 text-white font-bold rounded-xl p-3 hover:bg-indigo-800">Filtrele</button>
                    </form>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
                    {% for sporcu in sporcular %}
                    <a href="/sporcu/{{ sporcu.id }}/" class="bg-white rounded-3xl shadow hover:shadow-2xl transition group overflow-hidden border-2 border-transparent hover:border-orange-200">
                        <div class="h-60 bg-gray-200 relative">
                            {% if sporcu.profil_fotografi %}<img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">{% endif %}
                            <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-indigo-900 p-4 pt-10">
                                <h3 class="text-white font-bold text-lg">{{ sporcu.isim }}</h3>
                                <p class="text-orange-300 text-xs font-bold">{{ sporcu.kulup.isim }}</p>
                            </div>
                        </div>
                        <div class="p-4 flex justify-between items-center text-sm">
                            <span class="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">{{ sporcu.get_mevki_display }}</span>
                            <span class="font-bold text-indigo-900">{{ sporcu.boy }} cm</span>
                        </div>
                    </a>
                    {% endfor %}
                </div>
            </div>

            <div class="space-y-8">
                {% if aktif_anket %}
                <div class="bg-white rounded-[2rem] shadow-xl border border-orange-100 p-6 relative overflow-hidden">
                    <h3 class="text-lg font-extrabold text-indigo-900 mb-4 relative z-10">📊 Haftanın Anketi</h3>
                    <p class="text-gray-700 font-bold mb-4 relative z-10">{{ aktif_anket.soru }}</p>
                    <form action="/oy-ver/{{ aktif_anket.id }}/" method="POST" class="relative z-10 space-y-3">
                        {% csrf_token %}
                        {% for secenek in aktif_anket.secenekler.all %}
                        <label class="flex items-center justify-between bg-gray-50 hover:bg-orange-50 p-3 rounded-xl cursor-pointer transition border border-gray-200 hover:border-orange-300 group">
                            <div class="flex items-center gap-3"><input type="radio" name="secenek" value="{{ secenek.id }}" class="w-4 h-4 text-orange-600"><span class="text-sm font-medium">{{ secenek.metin }}</span></div>
                            <span class="text-xs font-bold text-gray-400">{{ secenek.oy_sayisi }}</span>
                        </label>
                        {% endfor %}
                        <button class="w-full bg-indigo-900 text-white py-3 rounded-xl font-bold text-sm hover:bg-indigo-800 mt-4 shadow-lg">OY VER</button>
                    </form>
                </div>
                {% endif %}

                <div class="bg-white rounded-[2rem] shadow-lg overflow-hidden border border-indigo-50">
                    <div class="bg-indigo-900 text-white p-5 font-bold text-center">🏆 Sultanlar Ligi</div>
                    <table class="w-full text-sm">{% for s in puan_tablosu %}<tr class="border-b hover:bg-indigo-50 transition"><td class="p-4 font-medium">{{ forloop.counter }}. {{ s.kulup.isim }}</td><td class="p-4 font-bold text-right text-indigo-900">{{ s.puan|floatformat:0 }}</td></tr>{% endfor %}</table>
                </div>
                
                <div class="bg-white rounded-[2rem] shadow-lg p-6 border border-gray-100">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2">📅 Fikstür</h3>
                    <div class="space-y-3">
                        {% for mac in maclar %}
                        <a href="/mac/{{ mac.id }}/" class="block text-sm border-b border-dashed border-gray-200 pb-3 last:border-0 last:pb-0 hover:bg-orange-50 transition p-2 rounded-lg group">
                            <div class="text-xs text-orange-600 font-bold mb-1">{{ mac.tarih|date:"d M • H:i" }}</div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700 w-1/3 text-right truncate">{{ mac.ev_sahibi.isim }}</span>
                                <span class="font-bold bg-indigo-100 text-indigo-900 px-2 py-0.5 rounded mx-1 text-xs">{{ mac.skor }}</span>
                                <span class="font-medium text-gray-700 w-1/3 truncate">{{ mac.deplasman.isim }}</span>
                            </div>
                        </a>
                        {% empty %}<p class="text-xs text-gray-400 text-center">Maç yok.</p>{% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <div class="mt-24 border-t pt-12">
            <h2 class="text-3xl font-extrabold text-center text-indigo-900 mb-12">İstatistik Merkezi</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white p-6 rounded-3xl shadow-lg"><canvas id="mevkiChart"></canvas></div>
                <div class="bg-white p-6 rounded-3xl shadow-lg"><canvas id="boyChart"></canvas></div>
                <div class="bg-white p-6 rounded-3xl shadow-lg"><canvas id="degerChart"></canvas></div>
            </div>
        </div>
    </main>
    __FOOTER__
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>new Swiper(".mySwiper", { autoplay: { delay: 4000 }, pagination: { clickable: true } });</script>
    <script>
        const mevkiData = { labels: {{ mevki_labels|safe }}, datasets: [{ data: {{ mevki_counts|safe }}, backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'] }] };
        const boyData = { labels: {{ uzun_labels|safe }}, datasets: [{ label: 'Boy', data: {{ uzun_values|safe }}, backgroundColor: '#36A2EB' }] };
        const degerData = { labels: {{ deger_labels|safe }}, datasets: [{ label: 'Değer', data: {{ deger_values|safe }}, backgroundColor: '#4BC0C0' }] };
        new Chart(document.getElementById('mevkiChart'), { type: 'doughnut', data: mevkiData });
        new Chart(document.getElementById('boyChart'), { type: 'bar', data: boyData, options: { indexAxis: 'y' } });
        new Chart(document.getElementById('degerChart'), { type: 'bar', data: degerData });
    </script>
</body>
</html>
"""

DETAY_HTML_RAW = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ sporcu.isim }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>body { font-family: 'Outfit', sans-serif; }</style>
</head>
<body class="bg-gray-100 flex flex-col min-h-screen">
    __NAVBAR__
    <main class="flex-grow container mx-auto px-4 py-8">
        <div class="text-sm text-gray-500 mb-4"><a href="/">Anasayfa</a> / Oyuncu Profili</div>
        <div class="bg-white rounded-[2rem] shadow-xl overflow-hidden flex flex-col md:flex-row mb-8 border border-gray-100">
            <div class="md:w-1/3 bg-gray-200 relative min-h-[450px]">
                {% if sporcu.profil_fotografi %}<img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover absolute inset-0">{% endif %}
                <div class="absolute bottom-4 right-4 z-10"><form method="POST">{% csrf_token %}<button name="begen" class="bg-white/90 backdrop-blur text-red-500 px-6 py-3 rounded-full shadow-lg font-bold hover:scale-105 transition flex items-center gap-2 text-lg">❤️ {{ sporcu.begeni_sayisi }}</button></form></div>
            </div>
            <div class="p-8 md:w-2/3">
                <h1 class="text-5xl font-extrabold text-gray-900 mb-4">{{ sporcu.isim }}</h1>
                <div class="flex gap-3 mb-8"><span class="bg-indigo-100 text-indigo-800 px-4 py-1 rounded-full font-bold">{{ sporcu.kulup.isim }}</span><span class="bg-orange-100 text-orange-800 px-4 py-1 rounded-full font-bold">{{ sporcu.get_mevki_display }}</span></div>
                <div class="grid grid-cols-3 gap-6 mb-8 text-center">
                    <div class="bg-gray-50 p-6 rounded-2xl border border-gray-200"><div class="text-3xl font-black text-indigo-900">{{ sporcu.boy }}</div><div class="text-xs font-bold text-gray-500 mt-1 uppercase">Boy (cm)</div></div>
                    <div class="bg-gray-50 p-6 rounded-2xl border border-gray-200"><div class="text-3xl font-black text-indigo-900">{{ sporcu.smac_yuksekligi|default:"-" }}</div><div class="text-xs font-bold text-gray-500 mt-1 uppercase">Smaç</div></div>
                    <div class="bg-gray-50 p-6 rounded-2xl border border-gray-200"><div class="text-3xl font-black text-indigo-900">€ {{ sporcu.piyasa_degeri|default:"-" }}</div><div class="text-xs font-bold text-gray-500 mt-1 uppercase">Değer</div></div>
                </div>
                <h3 class="font-bold text-gray-900 mb-4 text-xl">Kariyer Geçmişi</h3>
                <table class="w-full text-sm text-left text-gray-600 mb-8"><thead class="bg-gray-50 text-gray-500 uppercase text-xs"><tr><th class="p-3">Sezon</th><th class="p-3">Eski</th><th class="p-3">Yeni</th></tr></thead><tbody>{% for t in sporcu.transferler.all %}<tr class="border-b"><td class="p-3 font-bold text-indigo-900">{{ t.sezon }}</td><td class="p-3">{{ t.eski_kulup.isim|default:"-" }}</td><td class="p-3 font-bold">{{ t.yeni_kulup.isim|default:"-" }}</td></tr>{% endfor %}</tbody></table>
                {% if sporcu.video_linki %}<a href="{{ sporcu.video_linki }}" target="_blank" class="block w-full bg-red-600 text-white text-center py-4 rounded-xl font-bold hover:bg-red-700 transition">▶ Tanıtım Videosunu İzle</a>{% endif %}
            </div>
        </div>
        <div class="max-w-4xl mx-auto mt-16">
            <h3 class="text-3xl font-bold text-indigo-900 mb-8 flex items-center gap-3">💬 Taraftar Yorumları</h3>
            {% if user.is_authenticated %}
            <form method="POST" class="mb-10 bg-white p-6 rounded-[2rem] shadow-lg border border-indigo-50">{% csrf_token %}<input type="hidden" name="yorum_yaz" value="1"><textarea name="metin" rows="3" class="w-full border-2 border-gray-100 p-4 rounded-xl focus:outline-none focus:border-orange-400 transition resize-none" placeholder="Oyuncu hakkında ne düşünüyorsun?"></textarea><div class="text-right mt-3"><button class="bg-orange-500 text-white px-8 py-3 rounded-xl font-bold hover:bg-orange-600 transition shadow-lg shadow-orange-500/30">Yorumu Gönder</button></div></form>
            {% else %}<div class="bg-indigo-50 p-6 rounded-xl text-indigo-900 font-medium mb-8 border border-indigo-100">Yorum yapmak için <a href="/giris/" class="font-bold underline text-orange-600">giriş yapmalısınız.</a></div>{% endif %}
            <div class="space-y-6">{% for yorum in sporcu.yorumlar.all %}<div class="bg-white p-6 rounded-2xl shadow-sm flex gap-5 border border-gray-50 hover:shadow-md transition"><div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl shrink-0 shadow-md">{{ yorum.yazan.username.0|upper }}</div><div><div class="flex items-center gap-3 mb-2"><span class="font-bold text-gray-900 text-lg">{{ yorum.yazan.username }}</span><span class="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">{{ yorum.tarih|timesince }} önce</span></div><p class="text-gray-700 leading-relaxed">{{ yorum.metin }}</p></div></div>{% empty %}<p class="text-gray-400 text-center py-8 italic">Henüz yorum yapılmamış.</p>{% endfor %}</div>
        </div>
    </main>
    __FOOTER__
</body>
</html>
"""

KARSILASTIR_HTML_RAW = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Karşılaştırma</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>body { font-family: 'Outfit', sans-serif; } .winner { background-color: #dcfce7; border-color: #22c55e; color: #15803d; font-weight: bold; } .loser { background-color: #fee2e2; border-color: #ef4444; opacity: 0.7; }</style>
</head>
<body class="bg-gray-100 flex flex-col min-h-screen">
    __NAVBAR__
    <main class="flex-grow container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-center text-indigo-900 mb-2">⚔️ Karşılaştırma</h1>
        <div class="flex justify-center items-center gap-4 mb-8"><span class="text-xl font-bold text-gray-600">{{ p1.isim }}</span><span class="bg-orange-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">VS</span><span class="text-xl font-bold text-gray-600">{{ p2.isim }}</span></div>
        <div class="grid grid-cols-2 gap-4 md:gap-12 max-w-4xl mx-auto">
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="h-64 bg-gray-200 relative">{% if p1.profil_fotografi %}<img src="{{ p1.profil_fotografi.url }}" class="w-full h-full object-cover">{% endif %}<div class="absolute bottom-0 left-0 w-full bg-black/60 p-2 text-center text-white font-bold">{{ p1.isim }}</div></div>
                <div class="p-4 space-y-2">
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.boy == 1 %}winner{% elif analiz.boy == 2 %}loser{% endif %}"><span>Boy</span><span>{{ p1.boy }} cm</span></div>
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.smac == 1 %}winner{% elif analiz.smac == 2 %}loser{% endif %}"><span>Smaç</span><span>{{ p1.smac_yuksekligi|default:"-" }}</span></div>
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.deger == 1 %}winner{% elif analiz.deger == 2 %}loser{% endif %}"><span>Değer</span><span>€ {{ p1.piyasa_degeri|default:"-" }}</span></div>
                </div>
            </div>
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="h-64 bg-gray-200 relative">{% if p2.profil_fotografi %}<img src="{{ p2.profil_fotografi.url }}" class="w-full h-full object-cover">{% endif %}<div class="absolute bottom-0 left-0 w-full bg-black/60 p-2 text-center text-white font-bold">{{ p2.isim }}</div></div>
                <div class="p-4 space-y-2">
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.boy == 2 %}winner{% elif analiz.boy == 1 %}loser{% endif %}"><span>Boy</span><span>{{ p2.boy }} cm</span></div>
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.smac == 2 %}winner{% elif analiz.smac == 1 %}loser{% endif %}"><span>Smaç</span><span>{{ p2.smac_yuksekligi|default:"-" }}</span></div>
                    <div class="flex justify-between items-center p-3 border rounded {% if analiz.deger == 2 %}winner{% elif analiz.deger == 1 %}loser{% endif %}"><span>Değer</span><span>€ {{ p2.piyasa_degeri|default:"-" }}</span></div>
                </div>
            </div>
        </div>
    </main>
    __FOOTER__
</body>
</html>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path} Yazıldı.")

def main():
    print("🚀 HATASIZ BİRLEŞTİRME BAŞLIYOR...\n")
    
    # 1. Views'ı yaz
    write_file('core/views.py', VIEWS_CODE)
    
    # 2. HTML'leri Birleştir ve Yaz
    index_full = INDEX_HTML_RAW.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML)
    detay_full = DETAY_HTML_RAW.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML)
    karsilastir_full = KARSILASTIR_HTML_RAW.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML)
    
    write_file('core/templates/index.html', index_full)
    write_file('core/templates/detay.html', detay_full)
    write_file('core/templates/karsilastir.html', karsilastir_full)
    
    print("\n🎉 İŞLEM TAMAM! Siteyi yenile. Header, Footer ve VS Modu artık hatasız.")

if __name__ == '__main__':
    main()