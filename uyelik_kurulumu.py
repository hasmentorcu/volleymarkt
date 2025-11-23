import os

# --- 1. GÜNCELLENMİŞ MODELLER (User Bağlantısı Eklendi) ---

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

    def __str__(self):
        return self.isim
    
    class Meta:
        verbose_name_plural = "Kulüpler"

class Menajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı Hesabı")
    isim = models.CharField(max_length=100, verbose_name="Menajer Adı Soyadı")
    sirket_adi = models.CharField(max_length=100, verbose_name="Şirket Adı", blank=True)
    telefon = models.CharField(max_length=20, blank=True, verbose_name="İletişim")

    def __str__(self):
        return self.isim
    
    class Meta:
        verbose_name_plural = "Menajerler"

class Sporcu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı Hesabı")
    isim = models.CharField(max_length=100, verbose_name="Ad Soyad")
    dogum_tarihi = models.DateField(verbose_name="Doğum Tarihi", null=True, blank=True)
    boy = models.PositiveIntegerField(help_text="cm", verbose_name="Boy", null=True, blank=True)
    kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular", verbose_name="Mevcut Kulübü")
    menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Menajeri")
    mevki = models.CharField(max_length=20, choices=MEVKILER, verbose_name="Mevki", null=True, blank=True)
    smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True, verbose_name="Smaç")
    blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True, verbose_name="Blok")
    profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True)
    video_linki = models.URLField(blank=True, verbose_name="YouTube Linki")

    def __str__(self):
        return f"{self.isim}"
    
    class Meta:
        verbose_name_plural = "Sporcular"

class PuanDurumu(models.Model):
    kulup = models.OneToOneField(Kulup, on_delete=models.CASCADE, verbose_name="Kulüp")
    oynanan = models.PositiveIntegerField(default=0)
    galibiyet = models.PositiveIntegerField(default=0)
    maglubiyet = models.PositiveIntegerField(default=0)
    puan = models.FloatField(default=0)

    class Meta:
        ordering = ['-puan', '-galibiyet']
    
    def __str__(self):
        return f"{self.kulup.isim}"

class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE)
    deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE)
    tarih = models.DateTimeField()
    skor = models.CharField(max_length=10, blank=True, default="-")
    
    class Meta:
        ordering = ['tarih']
"""

# --- 2. YENİ VIEWS (Giriş/Kayıt Eklendi) ---

VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Menajer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

def anasayfa(request):
    sporcular = Sporcu.objects.all()
    puan_tablosu = PuanDurumu.objects.all().order_by('-puan')
    maclar = Mac.objects.all().order_by('tarih')[:5]
    return render(request, 'index.html', {'sporcular': sporcular, 'puan_tablosu': puan_tablosu, 'maclar': maclar})

def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})

def giris_yap(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
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
        rol = request.POST['rol'] # 'sporcu' veya 'menajer'

        # Kullanıcı Oluştur
        if User.objects.filter(username=kullanici_adi).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
            return render(request, 'kayit.html')
            
        user = User.objects.create_user(username=kullanici_adi, password=sifre)
        
        # Profil Oluştur
        if rol == 'sporcu':
            Sporcu.objects.create(user=user, isim=isim)
        elif rol == 'menajer':
            Menajer.objects.create(user=user, isim=isim)
        
        login(request, user)
        messages.success(request, "Kayıt başarılı! Hoşgeldiniz.")
        return redirect('anasayfa')

    return render(request, 'kayit.html')
"""

# --- 3. URL AYARLARI ---

URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import anasayfa, sporcu_detay, giris_yap, kayit_ol, cikis_yap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    path('giris/', giris_yap, name='giris'),
    path('kayit/', kayit_ol, name='kayit'),
    path('cikis/', cikis_yap, name='cikis'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# --- 4. HTML TASARIMLARI (Navbar Güncellendi) ---

# Navbar Kısmını Dinamik Yapıyoruz (Kullanıcı giriş yaptıysa Çıkış butonu görünsün)
NAVBAR_HTML = """
    <nav class="bg-white shadow p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <div class="flex items-center space-x-4">
                {% if user.is_authenticated %}
                    <span class="text-gray-600 text-sm hidden md:inline">Hoşgeldin, <b>{{ user.username }}</b></span>
                    <a href="{% url 'cikis' %}" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-sm">Çıkış Yap</a>
                {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900 font-medium hover:underline">Giriş Yap</a>
                    <a href="{% url 'kayit' %}" class="bg-indigo-900 text-white px-4 py-2 rounded hover:bg-indigo-800 text-sm">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </nav>
"""

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
        {{% if messages %}}
        <div class="mb-4">
            {{% for message in messages %}}
            <div class="p-4 rounded-lg bg-green-100 text-green-700 border border-green-200">{{{{ message }}}}</div>
            {{% endfor %}}
        </div>
        {{% endif %}}

        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-3">
                <h1 class="text-2xl font-bold text-gray-800 mb-6 border-l-4 border-orange-500 pl-4">Öne Çıkan Sporcular</h1>
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
                    </a>
                    {{% empty %}}
                        <p class="text-gray-500">Henüz sporcu eklenmedi.</p>
                    {{% endfor %}}
                </div>
            </div>

            <div class="md:col-span-1 space-y-8">
                <div class="bg-white rounded-xl shadow overflow-hidden">
                    <div class="bg-indigo-900 text-white p-3 font-bold text-center">Puan Durumu</div>
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
            </div>
        </div>
    </div>
</body>
</html>
"""

GIRIS_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Giriş Yap - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-2xl font-bold text-center text-indigo-900 mb-6">Giriş Yap</h2>
        {% if messages %}
            {% for message in messages %}
                <div class="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <form method="POST">
            {% csrf_token %}
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">Kullanıcı Adı</label>
                <input type="text" name="username" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" required>
            </div>
            <div class="mb-6">
                <label class="block text-gray-700 text-sm font-bold mb-2">Şifre</label>
                <input type="password" name="password" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" required>
            </div>
            <button type="submit" class="w-full bg-indigo-900 text-white font-bold py-2 px-4 rounded hover:bg-indigo-800 transition">Giriş Yap</button>
        </form>
        <p class="text-center mt-4 text-sm text-gray-600">Hesabın yok mu? <a href="/kayit" class="text-orange-500 font-bold">Kayıt Ol</a></p>
        <p class="text-center mt-4 text-sm text-gray-400"><a href="/">← Ana Sayfaya Dön</a></p>
    </div>
</body>
</html>
"""

KAYIT_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kayıt Ol - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-2xl font-bold text-center text-indigo-900 mb-6">VolleyMarkt Üyeliği</h2>
        {% if messages %}
            {% for message in messages %}
                <div class="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <form method="POST">
            {% csrf_token %}
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">Hesap Türü</label>
                <select name="rol" class="w-full border rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500">
                    <option value="sporcu">🏐 Ben Sporcuyum</option>
                    <option value="menajer">💼 Ben Menajerim</option>
                </select>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">Ad Soyad (Profilde Görünecek)</label>
                <input type="text" name="isim" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" required>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">Kullanıcı Adı</label>
                <input type="text" name="username" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" required>
            </div>
            <div class="mb-6">
                <label class="block text-gray-700 text-sm font-bold mb-2">Şifre</label>
                <input type="password" name="password" class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" required>
            </div>
            <button type="submit" class="w-full bg-orange-500 text-white font-bold py-2 px-4 rounded hover:bg-orange-600 transition">Ücretsiz Kayıt Ol</button>
        </form>
        <p class="text-center mt-4 text-sm text-gray-600">Zaten hesabın var mı? <a href="/giris" class="text-indigo-900 font-bold">Giriş Yap</a></p>
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
    print("🚀 Üyelik Sistemi Yükleniyor...\n")
    
    write_file('core/models.py', MODELS_CODE)
    write_file('core/views.py', VIEWS_CODE)
    write_file('volleymarkt/urls.py', URLS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/giris.html', GIRIS_HTML)
    write_file('core/templates/kayit.html', KAYIT_HTML)
    
    print("\n🎉 GÜNCELLEME TAMAMLANDI!")
    print("⚠️ LÜTFEN ŞU KOMUTLARI ÇALIŞTIR (Veritabanı değişikliği için):")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")

if __name__ == '__main__':
    main()