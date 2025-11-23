import os

# --- 1. VIEWS GÜNCELLEMESİ (Reklam Mantığı) ---
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
    # ... (Filtreleme kodları aynen kalıyor, burayı kısaltıyorum) ...
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

    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    maclar = Mac.objects.all().order_by('tarih')[:5]
    
    # HABERLER VE REKLAM MANTIĞI
    mansetler_raw = list(Haber.objects.filter(manset_mi=True)[:10]) # Ham haber listesi
    
    # Reklam Objeleri (Sanki habermiş gibi davranacaklar)
    reklam_1 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/FF5733/FFFFFF?text=REKLAM+ALANI+1', 'link': '#'}
    reklam_2 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/33FF57/FFFFFF?text=REKLAM+ALANI+2', 'link': '#'}
    
    manset_listesi = []
    haber_sayaci = 0
    
    for haber in mansetler_raw:
        manset_listesi.append(haber)
        haber_sayaci += 1
        
        # 2 haberden sonra 1. reklamı koy
        if haber_sayaci == 2:
            manset_listesi.append(reklam_1)
            
        # 5 haberden sonra 2. reklamı koy
        if haber_sayaci == 5:
            manset_listesi.append(reklam_2)

    son_haberler = Haber.objects.all()[:6]

    # GRAFİKLER
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
        'puan_tablosu': puan_tablosu,
        'maclar': maclar,
        'kulupler': Kulup.objects.all(),
        'mevkiler': MEVKILER,
        'secili_isim': isim,
        'secili_kulup': int(kulup_id) if kulup_id else None,
        'secili_mevki': mevki,
        'secili_min_boy': min_boy,
        'secili_max_boy': max_boy,
        'mansetler': manset_listesi, # Güncellenmiş liste
        'son_haberler': son_haberler,
        'mevki_labels': mevki_labels,
        'mevki_counts': mevki_counts,
        'uzun_labels': uzun_labels,
        'uzun_values': uzun_values,
        'deger_labels': deger_labels,
        'deger_values': deger_values,
    }
    return render(request, 'index.html', context)

# --- (Diğer view fonksiyonları aynen kalıyor: sporcu_detay, giris_yap vb.) ---
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
            user = form.get_user()
            login(request, user)
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

# --- 2. HTML GÜNCELLEMESİ (Reklam Alanları) ---
INDEX_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .swiper { width: 100%; height: 100%; } /* Slider yüksekliğini container belirlesin */
        .swiper-slide { text-align: center; font-size: 18px; background: #000; display: flex; justify-content: center; align-items: center; }
        .swiper-slide img { display: block; width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }
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
        
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
            
            <div class="lg:col-span-3 h-[450px] relative rounded-2xl shadow-xl overflow-hidden bg-black">
                {% if mansetler %}
                <div class="swiper mySwiper h-full">
                    <div class="swiper-wrapper">
                        {% for item in mansetler %}
                            {% if item.is_ad %}
                                <div class="swiper-slide relative bg-gray-900">
                                    <img src="{{ item.image }}" alt="Reklam">
                                    <div class="absolute top-2 right-2 bg-white/20 text-white px-2 py-1 rounded text-xs border border-white/30">REKLAM</div>
                                    <a href="{{ item.link }}" class="absolute inset-0 z-10"></a>
                                </div>
                            {% else %}
                                <div class="swiper-slide relative">
                                    {% if item.resim %}
                                        <img src="{{ item.resim.url }}" alt="{{ item.baslik }}">
                                    {% else %}
                                        <div class="w-full h-full bg-gray-800 flex items-center justify-center text-white">Görsel Yok</div>
                                    {% endif %}
                                    <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black via-black/80 to-transparent p-8 text-left">
                                        <span class="bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded mb-2 inline-block">{{ item.get_kategori_display }}</span>
                                        <h2 class="text-2xl md:text-4xl font-bold text-white mb-2 leading-tight shadow-black drop-shadow-md">{{ item.baslik }}</h2>
                                        <a href="{% url 'haber_detay' item.id %}" class="inline-block mt-2 text-white border-b border-orange-500 pb-1 hover:text-orange-400 transition text-sm font-bold">Haberi Oku →</a>
                                    </div>
                                </div>
                            {% endif %}
                        {% endfor %}
                    </div>
                    <div class="swiper-button-next text-white/70 hover:text-white"></div>
                    <div class="swiper-button-prev text-white/70 hover:text-white"></div>
                    <div class="swiper-pagination"></div>
                </div>
                {% else %}
                    <div class="flex items-center justify-center h-full text-white">Henüz haber girilmedi.</div>
                {% endif %}
            </div>

            <div class="lg:col-span-1 h-[450px] flex flex-col gap-4">
                <div class="bg-gray-200 h-full rounded-xl flex items-center justify-center relative group overflow-hidden shadow-lg">
                    <img src="https://via.placeholder.com/400x500/333333/FFFFFF?text=SPONSOR+ALANI" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                    <div class="absolute top-2 right-2 bg-black/30 text-white text-[10px] px-2 rounded">REKLAM</div>
                    <a href="#" class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition"></a>
                </div>
            </div>
        </div>

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
                        <p class="text-gray-500 col-span-3 text-center py-8">Sonuç yok.</p>
                    {% endfor %}
                </div>
            </div>

            <div class="space-y-8">
                <div class="bg-white rounded-xl shadow overflow-hidden">
                    <div class="bg-indigo-900 text-white p-3 font-bold text-center">Puan Durumu</div>
                    <table class="w-full text-sm text-left">
                        {% for sira in puan_tablosu %}
                        <tr class="border-b hover:bg-gray-50"><td class="p-2">{{ forloop.counter }}. {{ sira.kulup.isim }}</td><td class="p-2 font-bold text-right">{{ sira.puan|floatformat:0 }}P</td></tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>

        <div class="mt-16 border-t pt-12">
            <h2 class="text-2xl font-bold text-center text-indigo-900 mb-8">📊 İstatistikler</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white p-4 rounded-xl shadow"><canvas id="mevkiChart"></canvas></div>
                <div class="bg-white p-4 rounded-xl shadow"><canvas id="boyChart"></canvas></div>
                <div class="bg-white p-4 rounded-xl shadow"><canvas id="degerChart"></canvas></div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        var swiper = new Swiper(".mySwiper", {
            spaceBetween: 0,
            effect: "fade", // Daha şık geçiş
            autoplay: { delay: 4000, disableOnInteraction: false },
            pagination: { el: ".swiper-pagination", clickable: true },
            navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
        });
    </script>
    <script>
        const mevkiData = { labels: {{ mevki_labels|safe }}, datasets: [{ data: {{ mevki_counts|safe }}, backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'] }] };
        const boyData = { labels: {{ uzun_labels|safe }}, datasets: [{ label: 'Boy (cm)', data: {{ uzun_values|safe }}, backgroundColor: '#36A2EB' }] };
        const degerData = { labels: {{ deger_labels|safe }}, datasets: [{ label: 'Değer (€)', data: {{ deger_values|safe }}, backgroundColor: '#4BC0C0' }] };
        new Chart(document.getElementById('mevkiChart'), { type: 'pie', data: mevkiData });
        new Chart(document.getElementById('boyChart'), { type: 'bar', data: boyData, options: { indexAxis: 'y' } });
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
    print("🚀 REKLAMLI TASARIM Yükleniyor...\n")
    write_file('core/views.py', VIEWS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    print("\n🎉 İŞLEM TAMAM! Önce 'python manage.py haber_botu' ile haber çek.")
    print("Sonra 'python manage.py runserver' ile siteyi aç.")

if __name__ == '__main__':
    main()