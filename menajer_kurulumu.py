import os

# --- 1. VIEWS (Menajer Mantığı Eklendi) ---
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Kulup, MEVKILER, Menajer
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# --- GENEL SAYFALAR ---

def anasayfa(request):
    sporcular = Sporcu.objects.all()
    
    # Filtreleme
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

    # Yan Veriler
    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    maclar = Mac.objects.all().order_by('tarih')[:5]
    
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
    }
    return render(request, 'index.html', context)

def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})

# --- KULLANICI İŞLEMLERİ ---

def giris_yap(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Yönlendirme Mantığı
            if hasattr(user, 'menajer'):
                return redirect('menajer_panel')
            elif hasattr(user, 'sporcu'):
                return redirect('profil_duzenle')
            else:
                return redirect('anasayfa')
        else:
            messages.error(request, "Hatalı kullanıcı adı veya şifre.")
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
            messages.error(request, "Bu kullanıcı adı dolu.")
            return render(request, 'kayit.html')
            
        user = User.objects.create_user(username=kullanici_adi, password=sifre)
        
        if rol == 'sporcu': 
            Sporcu.objects.create(user=user, isim=isim)
            login(request, user)
            return redirect('profil_duzenle')
            
        elif rol == 'menajer': 
            Menajer.objects.create(user=user, isim=isim)
            login(request, user)
            return redirect('menajer_panel')
            
    return render(request, 'kayit.html')

# --- MENAJER VE SPORCU PANELLERİ ---

@login_required
def profil_duzenle(request):
    # Sporcu Kendi Profilini Düzenler
    try:
        sporcu = request.user.sporcu
    except Sporcu.DoesNotExist:
        messages.warning(request, "Bu sayfaya erişim yetkiniz yok.")
        return redirect('anasayfa')

    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES, instance=sporcu)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil güncellendi.")
            return redirect('sporcu_detay', pk=sporcu.id)
    else:
        form = SporcuForm(instance=sporcu)
    return render(request, 'profil_duzenle.html', {'form': form})

@login_required
def menajer_panel(request):
    # Menajer Dashboard
    try:
        menajer = request.user.menajer
    except Menajer.DoesNotExist:
        messages.warning(request, "Sadece menajerler girebilir.")
        return redirect('anasayfa')
    
    # Menajerin kendi oyuncularını getir
    oyuncular = Sporcu.objects.filter(menajer=menajer)
    return render(request, 'menajer_panel.html', {'menajer': menajer, 'oyuncular': oyuncular})

@login_required
def menajer_oyuncu_ekle(request):
    # Menajer Yeni Oyuncu Ekler
    try:
        menajer = request.user.menajer
    except Menajer.DoesNotExist:
        return redirect('anasayfa')

    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES)
        if form.is_valid():
            yeni_sporcu = form.save(commit=False)
            yeni_sporcu.menajer = menajer # Otomatik olarak bu menajere bağla
            yeni_sporcu.save()
            messages.success(request, f"{yeni_sporcu.isim} portföyünüze eklendi!")
            return redirect('menajer_panel')
    else:
        form = SporcuForm()
    
    return render(request, 'menajer_form.html', {'form': form, 'baslik': 'Yeni Oyuncu Ekle'})

@login_required
def menajer_oyuncu_duzenle(request, pk):
    # Menajer Mevcut Oyuncusunu Düzenler
    try:
        menajer = request.user.menajer
        sporcu = get_object_or_404(Sporcu, pk=pk, menajer=menajer) # Güvenlik: Sadece kendi oyuncusuysa
    except:
        return redirect('anasayfa')

    if request.method == 'POST':
        form = SporcuForm(request.POST, request.FILES, instance=sporcu)
        if form.is_valid():
            form.save()
            messages.success(request, "Oyuncu bilgileri güncellendi.")
            return redirect('menajer_panel')
    else:
        form = SporcuForm(instance=sporcu)
    
    return render(request, 'menajer_form.html', {'form': form, 'baslik': f'{sporcu.isim} Düzenle'})
"""

# --- 2. URLS (Yeni Yollar Eklendi) ---
URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import (anasayfa, sporcu_detay, giris_yap, kayit_ol, cikis_yap, 
                        profil_duzenle, menajer_panel, menajer_oyuncu_ekle, menajer_oyuncu_duzenle)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    
    # Kimlik
    path('giris/', giris_yap, name='giris'),
    path('kayit/', kayit_ol, name='kayit'),
    path('cikis/', cikis_yap, name='cikis'),
    
    # Paneller
    path('profil-duzenle/', profil_duzenle, name='profil_duzenle'),
    path('menajer-panel/', menajer_panel, name='menajer_panel'),
    path('menajer/ekle/', menajer_oyuncu_ekle, name='menajer_oyuncu_ekle'),
    path('menajer/duzenle/<int:pk>/', menajer_oyuncu_duzenle, name='menajer_oyuncu_duzenle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# --- 3. HTML TASARIMLARI (Menajer Ekranları) ---

MENAJER_PANEL_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Menajer Paneli</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    <nav class="bg-indigo-900 text-white p-4 mb-8">
        <div class="container mx-auto flex justify-between items-center">
            <div class="font-bold text-xl">Menajer Paneli | {{ menajer.isim }}</div>
            <div class="space-x-4">
                <a href="/" class="hover:text-orange-300">Siteyi Görüntüle</a>
                <a href="{% url 'cikis' %}" class="bg-red-600 px-3 py-1 rounded hover:bg-red-700">Çıkış</a>
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-4">
        {% if messages %}
            {% for message in messages %}
                <div class="bg-green-100 text-green-800 p-4 rounded mb-6 border border-green-200">{{ message }}</div>
            {% endfor %}
        {% endif %}

        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-bold text-gray-800">Oyuncu Portföyüm</h1>
            <a href="{% url 'menajer_oyuncu_ekle' %}" class="bg-orange-500 text-white px-6 py-2 rounded-lg font-bold hover:bg-orange-600 shadow-md flex items-center gap-2">
                + Yeni Oyuncu Ekle
            </a>
        </div>

        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
                    <tr>
                        <th class="p-4 border-b">Fotoğraf</th>
                        <th class="p-4 border-b">İsim</th>
                        <th class="p-4 border-b">Kulüp</th>
                        <th class="p-4 border-b">Mevki</th>
                        <th class="p-4 border-b text-center">İşlemler</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    {% for sporcu in oyuncular %}
                    <tr class="hover:bg-gray-50">
                        <td class="p-3 w-16">
                            {% if sporcu.profil_fotografi %}
                                <img src="{{ sporcu.profil_fotografi.url }}" class="w-10 h-10 rounded-full object-cover">
                            {% else %}
                                <div class="w-10 h-10 bg-gray-200 rounded-full"></div>
                            {% endif %}
                        </td>
                        <td class="p-3 font-medium text-gray-900">{{ sporcu.isim }}</td>
                        <td class="p-3 text-gray-600">{{ sporcu.kulup.isim|default:"-" }}</td>
                        <td class="p-3 text-gray-600">{{ sporcu.get_mevki_display }}</td>
                        <td class="p-3 text-center">
                            <a href="{% url 'menajer_oyuncu_duzenle' sporcu.id %}" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm border border-indigo-200 px-3 py-1 rounded hover:bg-indigo-50">Düzenle</a>
                            <a href="{% url 'sporcu_detay' sporcu.id %}" target="_blank" class="ml-2 text-gray-400 hover:text-gray-600 text-sm">Görüntüle</a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="p-8 text-center text-gray-500">
                            Henüz portföyünüzde oyuncu yok. <br>
                            <span class="text-sm">Yukarıdaki butona tıklayarak ekleyebilirsiniz.</span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

MENAJER_FORM_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ baslik }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans pb-12">
    <div class="max-w-2xl mx-auto mt-10">
        <div class="bg-white rounded-xl shadow-lg p-8">
            <div class="flex justify-between items-center mb-6 border-b pb-4">
                <h1 class="text-2xl font-bold text-gray-900">{{ baslik }}</h1>
                <a href="{% url 'menajer_panel' %}" class="text-gray-500 hover:text-red-500 text-sm">İptal</a>
            </div>
            
            <form method="POST" enctype="multipart/form-data" class="space-y-6">
                {% csrf_token %}
                
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Profil Fotoğrafı</label>
                    {{ form.profil_fotografi }}
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Ad Soyad</label>
                        {{ form.isim }}
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Kulüp</label>
                        {{ form.kulup }}
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Mevki</label>
                        {{ form.mevki }}
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Boy (cm)</label>
                        {{ form.boy }}
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Smaç (cm)</label>
                        {{ form.smac_yuksekligi }}
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Blok (cm)</label>
                        {{ form.blok_yuksekligi }}
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Video Linki</label>
                    {{ form.video_linki }}
                </div>

                <button type="submit" class="w-full bg-indigo-900 text-white font-bold py-3 rounded-lg hover:bg-indigo-800 transition shadow-md">
                    Kaydet
                </button>
            </form>
        </div>
    </div>
</body>
</html>
"""

# Navbar Güncellemesi (Menajer Paneli Linki Eklendi)
NAVBAR_HTML = """
    <nav class="bg-white shadow p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <div class="flex items-center space-x-4">
                {% if user.is_authenticated %}
                    
                    {% if user.menajer %}
                         <a href="{% url 'menajer_panel' %}" class="bg-indigo-900 text-white px-4 py-2 rounded hover:bg-indigo-800 text-sm font-bold flex items-center gap-2">
                            💼 Menajer Paneli
                        </a>
                    {% elif user.sporcu %}
                         <a href="{% url 'profil_duzenle' %}" class="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600 text-sm font-bold flex items-center gap-2">
                            ✏️ Profilimi Düzenle
                        </a>
                    {% endif %}

                    <a href="{% url 'cikis' %}" class="text-gray-500 hover:text-red-500 text-sm">Çıkış</a>
                {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900 font-medium hover:underline">Giriş Yap</a>
                    <a href="{% url 'kayit' %}" class="bg-indigo-900 text-white px-4 py-2 rounded hover:bg-indigo-800 text-sm">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </nav>
"""

# Index dosyasını yeniden yazarken bu Navbar'ı kullanacağız
INDEX_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    {NAVBAR_HTML}

    <div class="container mx-auto px-4 mb-12">
        <div class="bg-white p-6 rounded-xl shadow-md mb-8 border border-gray-200">
            <h2 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">🔍 Detaylı Oyuncu Arama</h2>
            <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="col-span-1 md:col-span-4">
                    <input type="text" name="isim" value="{{{{ secili_isim|default:'' }}}}" placeholder="Oyuncu adı ara..." class="w-full border p-2 rounded focus:ring-2 focus:ring-orange-500 outline-none">
                </div>
                <div>
                    <select name="kulup" class="w-full border p-2 rounded bg-white">
                        <option value="">Tüm Kulüpler</option>
                        {{% for kulup in kulupler %}}
                            <option value="{{{{ kulup.id }}}}" {{% if kulup.id == secili_kulup %}}selected{{% endif %}}>{{{{ kulup.isim }}}}</option>
                        {{% endfor %}}
                    </select>
                </div>
                <div>
                    <select name="mevki" class="w-full border p-2 rounded bg-white">
                        <option value="">Tüm Mevkiler</option>
                        {{% for kod, ad in mevkiler %}}
                            <option value="{{{{ kod }}}}" {{% if kod == secili_mevki %}}selected{{% endif %}}>{{{{ ad }}}}</option>
                        {{% endfor %}}
                    </select>
                </div>
                <div class="flex gap-2">
                    <input type="number" name="min_boy" value="{{{{ secili_min_boy|default:'' }}}}" placeholder="Min cm" class="w-1/2 border p-2 rounded">
                    <input type="number" name="max_boy" value="{{{{ secili_max_boy|default:'' }}}}" placeholder="Max cm" class="w-1/2 border p-2 rounded">
                </div>
                <div class="flex gap-2">
                    <button type="submit" class="bg-indigo-900 text-white px-4 py-2 rounded hover:bg-indigo-800 flex-1 font-bold">Ara</button>
                    <a href="/" class="bg-gray-200 text-gray-600 px-3 py-2 rounded hover:bg-gray-300 flex items-center justify-center">↺</a>
                </div>
            </form>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-3">
                <div class="flex justify-between items-center mb-6">
                    <h1 class="text-2xl font-bold text-gray-800 border-l-4 border-orange-500 pl-4">Oyuncular</h1>
                    <span class="text-sm text-gray-500 bg-white px-3 py-1 rounded shadow-sm">{{{{ sporcular|length }}}} Sonuç</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {{% for sporcu in sporcular %}}
                    <a href="{{% url 'sporcu_detay' sporcu.id %}}" class="block bg-white rounded-xl shadow hover:shadow-lg transition duration-300 group">
                        <div class="h-56 overflow-hidden bg-gray-200 relative">
                            {{% if sporcu.profil_fotografi %}}
                                <img src="{{{{ sporcu.profil_fotografi.url }}}}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                            {{% else %}}
                                <div class="w-full h-full flex items-center justify-center text-gray-400">Görsel Yok</div>
                            {{% endif %}}
                            <div class="absolute bottom-0 left-0 bg-gradient-to-t from-black to-transparent w-full p-4 pt-8">
                                <h2 class="text-white font-bold text-lg">{{{{ sporcu.isim }}}}</h2>
                                <p class="text-orange-300 text-xs">{{{{ sporcu.kulup.isim|default:"-" }}}}</p>
                            </div>
                        </div>
                        <div class="p-4 flex justify-between items-center text-sm text-gray-600">
                            <span>{{{{ sporcu.get_mevki_display }}}}</span>
                            <span class="font-bold">{{{{ sporcu.boy }}}} cm</span>
                        </div>
                    </a>
                    {{% empty %}}
                        <p class="text-gray-500">Kayıt bulunamadı.</p>
                    {{% endfor %}}
                </div>
            </div>

            <div class="md:col-span-1 space-y-8">
                <div class="bg-white rounded-xl shadow overflow-hidden">
                    <div class="bg-indigo-900 text-white p-3 font-bold text-center">Sultanlar Ligi</div>
                    <table class="w-full text-sm text-left text-gray-600">
                        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                            <tr><th class="px-4 py-3">Kulüp</th><th class="px-2 py-3 text-center">P</th></tr>
                        </thead>
                        <tbody>
                            {{% for sira in puan_tablosu %}}
                            <tr class="border-b hover:bg-gray-50">
                                <td class="px-4 py-2 font-medium">{{{{ forloop.counter }}}}. {{{{ sira.kulup.isim }}}}</td>
                                <td class="px-2 py-2 text-center font-bold text-indigo-900">{{{{ sira.puan|floatformat:0 }}}}</td>
                            </tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                </div>
                <div class="bg-white rounded-xl shadow p-4">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2">Fikstür</h3>
                    <div class="space-y-4">
                        {{% for mac in maclar %}}
                        <div class="text-sm border-b pb-2 last:border-0">
                            <div class="text-xs text-gray-400 mb-1">{{{{ mac.tarih|date:"d M - H:i" }}}}</div>
                            <div class="flex justify-between">
                                <span class="font-medium">{{{{ mac.ev_sahibi.isim }}}}</span>
                                <span class="font-bold bg-gray-100 px-2 rounded">{{{{ mac.skor }}}}</span>
                                <span class="font-medium text-right">{{{{ mac.deplasman.isim }}}}</span>
                            </div>
                        </div>
                        {{% empty %}}
                            <p class="text-xs text-gray-400">Maç yok.</p>
                        {{% endfor %}}
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
    print("🚀 Menajer Paneli Yükleniyor...\n")
    write_file('core/views.py', VIEWS_CODE)
    write_file('volleymarkt/urls.py', URLS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/menajer_panel.html', MENAJER_PANEL_HTML)
    write_file('core/templates/menajer_form.html', MENAJER_FORM_HTML)
    print("\n🎉 İŞLEM TAMAM! 'python manage.py runserver' diyerek devam et.")

if __name__ == '__main__':
    main()