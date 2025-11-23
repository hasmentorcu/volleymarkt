import os

# --- 1. MODELLER (Değişiklik yok, aynen koruyoruz) ---
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=100)
    sirket_adi = models.CharField(max_length=100, blank=True)
    telefon = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.isim

class Sporcu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=100)
    dogum_tarihi = models.DateField(null=True, blank=True)
    boy = models.PositiveIntegerField(help_text="cm", null=True, blank=True)
    kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular")
    menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True)
    mevki = models.CharField(max_length=20, choices=MEVKILER, null=True, blank=True)
    smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True)
    blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True)
    profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True)
    video_linki = models.URLField(blank=True)

    def __str__(self):
        return f"{self.isim}"

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
"""

# --- 2. FORMLAR (Veri Giriş Kutucukları) ---
FORMS_CODE = """from django import forms
from .models import Sporcu

class SporcuForm(forms.ModelForm):
    class Meta:
        model = Sporcu
        fields = ['isim', 'kulup', 'mevki', 'boy', 'smac_yuksekligi', 'blok_yuksekligi', 'profil_fotografi', 'video_linki']
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'kulup': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'mevki': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'boy': forms.NumberInput(attrs={'class': 'w-full border p-2 rounded'}),
            'smac_yuksekligi': forms.NumberInput(attrs={'class': 'w-full border p-2 rounded'}),
            'blok_yuksekligi': forms.NumberInput(attrs={'class': 'w-full border p-2 rounded'}),
            'video_linki': forms.URLInput(attrs={'class': 'w-full border p-2 rounded', 'placeholder': 'https://youtube.com/...'}),
        }
"""

# --- 3. VIEWS (Profil Düzenleme Mantığı Eklendi) ---
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import Sporcu, PuanDurumu, Mac, Menajer
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        rol = request.POST['rol']
        
        if User.objects.filter(username=kullanici_adi).exists():
            messages.error(request, "Bu kullanıcı adı dolu.")
            return render(request, 'kayit.html')
            
        user = User.objects.create_user(username=kullanici_adi, password=sifre)
        if rol == 'sporcu': Sporcu.objects.create(user=user, isim=isim)
        elif rol == 'menajer': Menajer.objects.create(user=user, isim=isim)
        
        login(request, user)
        return redirect('profil_duzenle') # Kayıt sonrası direkt profile at
    return render(request, 'kayit.html')

@login_required
def profil_duzenle(request):
    try:
        # Giriş yapan kullanıcının sporcu profilini bul
        sporcu = request.user.sporcu
    except Sporcu.DoesNotExist:
        # Eğer menajerse veya profili yoksa ana sayfaya at (Basitlik için)
        messages.warning(request, "Bu özellik sadece sporcular içindir.")
        return redirect('anasayfa')

    if request.method == 'POST':
        # Dosya yükleme olduğu için request.FILES önemli
        form = SporcuForm(request.POST, request.FILES, instance=sporcu)
        if form.is_valid():
            form.save()
            messages.success(request, "Profiliniz başarıyla güncellendi!")
            return redirect('sporcu_detay', pk=sporcu.id)
    else:
        form = SporcuForm(instance=sporcu)

    return render(request, 'profil_duzenle.html', {'form': form})
"""

# --- 4. URLS ---
URLS_CODE = """from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import anasayfa, sporcu_detay, giris_yap, kayit_ol, cikis_yap, profil_duzenle

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    path('giris/', giris_yap, name='giris'),
    path('kayit/', kayit_ol, name='kayit'),
    path('cikis/', cikis_yap, name='cikis'),
    path('profil-duzenle/', profil_duzenle, name='profil_duzenle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

# --- 5. HTML TASARIMLARI ---

NAVBAR_HTML = """
    <nav class="bg-white shadow p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <div class="flex items-center space-x-4">
                {% if user.is_authenticated %}
                    <a href="{% url 'profil_duzenle' %}" class="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600 text-sm font-bold flex items-center gap-2">
                        ✏️ Profilimi Düzenle
                    </a>
                    <a href="{% url 'cikis' %}" class="text-gray-500 hover:text-red-500 text-sm">Çıkış</a>
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

PROFIL_DUZENLE_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Profilimi Düzenle - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans pb-12">
    <nav class="bg-white shadow p-4 mb-8">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <a href="/" class="text-gray-500 text-sm">İptal ve Geri Dön</a>
        </div>
    </nav>

    <div class="container mx-auto px-4 max-w-2xl">
        <div class="bg-white rounded-xl shadow-lg p-8">
            <h1 class="text-2xl font-bold text-gray-900 mb-6 border-b pb-4">Profil Bilgilerimi Güncelle</h1>
            
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
                        <label class="block text-sm font-bold text-gray-700 mb-2">Mevcut Kulüp</label>
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
                        <label class="block text-sm font-bold text-gray-700 mb-2">Smaç Yüksekliği (cm)</label>
                        {{ form.smac_yuksekligi }}
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Blok Yüksekliği (cm)</label>
                        {{ form.blok_yuksekligi }}
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Tanıtım Videosu (YouTube Linki)</label>
                    {{ form.video_linki }}
                    <p class="text-xs text-gray-500 mt-1">Örn: https://www.youtube.com/watch?v=...</p>
                </div>

                <button type="submit" class="w-full bg-orange-500 text-white font-bold py-3 rounded-lg hover:bg-orange-600 transition shadow-md">
                    Değişiklikleri Kaydet
                </button>
            </form>
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
    print("🚀 Profil Modülü Yükleniyor...\n")
    write_file('core/models.py', MODELS_CODE) # Emin olmak için
    write_file('core/forms.py', FORMS_CODE)
    write_file('core/views.py', VIEWS_CODE)
    write_file('volleymarkt/urls.py', URLS_CODE)
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/profil_duzenle.html', PROFIL_DUZENLE_HTML)
    print("\n🎉 İŞLEM TAMAM! 'python manage.py runserver' diyerek devam et.")

if __name__ == '__main__':
    main()