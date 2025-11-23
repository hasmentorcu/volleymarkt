import os

# --- 1. MODELLER (Transfer ve Piyasa Değeri Eklendi) ---
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
    
    # YENİ ALAN: Piyasa Değeri
    piyasa_degeri = models.PositiveIntegerField(null=True, blank=True, verbose_name="Piyasa Değeri (€)", help_text="Sadece sayı girin (Örn: 50000)")
    
    smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True)
    blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True)
    profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True)
    video_linki = models.URLField(blank=True)

    def __str__(self):
        return f"{self.isim}"

# YENİ MODEL: Transfer Geçmişi
class Transfer(models.Model):
    sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='transferler')
    sezon = models.CharField(max_length=20, verbose_name="Sezon", help_text="Örn: 2023-2024")
    tarih = models.DateField(null=True, blank=True)
    eski_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='giden_transferler', verbose_name="Eski Kulüp")
    yeni_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='gelen_transferler', verbose_name="Yeni Kulüp")
    tip = models.CharField(max_length=50, choices=[('Kiralık', 'Kiralık'), ('Bonservis', 'Bonservis'), ('Bedelsiz', 'Bedelsiz')], default='Bedelsiz')
    
    class Meta:
        ordering = ['-tarih'] # En yeni transfer en üstte

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

# --- 2. ADMIN (Transferleri Sporcu Sayfasında Göster) ---
ADMIN_CODE = """from django.contrib import admin
from .models import Kulup, Menajer, Sporcu, PuanDurumu, Mac, Transfer

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('isim', 'sehir')

# Transferleri Sporcu sayfasının içine gömüyoruz (Inline)
class TransferInline(admin.TabularInline):
    model = Transfer
    extra = 1
    fk_name = "sporcu"

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'kulup', 'piyasa_degeri')
    list_filter = ('mevki', 'kulup')
    inlines = [TransferInline] # <-- Transferler burada görünecek

@admin.register(PuanDurumu)
class PuanDurumuAdmin(admin.ModelAdmin):
    list_display = ('kulup', 'puan')
    ordering = ('-puan',)

@admin.register(Mac)
class MacAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'ev_sahibi', 'skor', 'deplasman')

admin.site.register(Menajer)
# admin.site.register(Transfer) # İstersek ayrı da görebiliriz ama Inline daha iyi
"""

# --- 3. HTML (Detay Sayfasında Transfer Tablosu) ---
DETAY_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ sporcu.isim }} - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        // Sayıları formatlamak için basit bir script (100000 -> 100.000 €)
        function formatMoney(amount) {
            return amount.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".");
        }
    </script>
</head>
<body class="bg-gray-100 font-sans pb-12">
    <nav class="bg-white shadow p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a>
            <div class="flex items-center space-x-4">
                 {% if user.is_authenticated %}
                     {% if user.menajer %}
                         <a href="{% url 'menajer_panel' %}" class="text-indigo-900 font-bold">💼 Panelim</a>
                     {% elif user.sporcu %}
                         <a href="{% url 'profil_duzenle' %}" class="text-orange-500 font-bold">✏️ Profilim</a>
                     {% endif %}
                 {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900 font-medium">Giriş</a>
                 {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-4">
        
        <div class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col md:flex-row mb-8">
            <div class="md:w-1/3 bg-gray-200 h-96 md:h-auto relative">
                {% if sporcu.profil_fotografi %}
                    <img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover">
                {% else %}
                    <div class="w-full h-full flex items-center justify-center text-gray-500">Fotoğraf Yok</div>
                {% endif %}
                
                {% if sporcu.piyasa_degeri %}
                <div class="absolute top-4 left-4 bg-green-600 text-white px-3 py-1 rounded shadow-lg">
                    <div class="text-xs opacity-90">Piyasa Değeri</div>
                    <div class="text-lg font-bold">€ {{ sporcu.piyasa_degeri }}</div>
                </div>
                {% endif %}
            </div>

            <div class="p-8 md:w-2/3 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start">
                        <div>
                            <h1 class="text-4xl font-bold text-gray-900">{{ sporcu.isim }}</h1>
                            <div class="flex items-center gap-2 mt-2">
                                <span class="bg-indigo-100 text-indigo-900 px-3 py-1 rounded font-bold text-sm">{{ sporcu.kulup.isim }}</span>
                                <span class="text-gray-500">•</span>
                                <span class="text-gray-600 font-medium">{{ sporcu.get_mevki_display }}</span>
                            </div>
                        </div>
                        <div class="text-right hidden md:block">
                            <div class="text-5xl font-bold text-gray-100">#{{ sporcu.id }}</div>
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-6 mt-8 text-center bg-gray-50 p-6 rounded-lg border border-gray-100">
                        <div>
                            <div class="text-3xl font-bold text-indigo-900">{{ sporcu.boy }}</div>
                            <div class="text-xs text-gray-500 uppercase font-bold tracking-wide">Boy (cm)</div>
                        </div>
                        <div class="border-l border-gray-200">
                            <div class="text-3xl font-bold text-indigo-900">{{ sporcu.smac_yuksekligi|default:"-" }}</div>
                            <div class="text-xs text-gray-500 uppercase font-bold tracking-wide">Smaç</div>
                        </div>
                        <div class="border-l border-gray-200">
                            <div class="text-3xl font-bold text-indigo-900">{{ sporcu.blok_yuksekligi|default:"-" }}</div>
                            <div class="text-xs text-gray-500 uppercase font-bold tracking-wide">Blok</div>
                        </div>
                    </div>

                    <div class="mt-6 grid grid-cols-2 gap-4 text-sm">
                        <div><span class="text-gray-500">Doğum Tarihi:</span> <span class="font-medium text-gray-900">{{ sporcu.dogum_tarihi|default:"-" }}</span></div>
                        <div><span class="text-gray-500">Menajer:</span> <span class="font-medium text-indigo-600">{{ sporcu.menajer.isim|default:"Menajeri Yok" }}</span></div>
                    </div>
                </div>

                {% if sporcu.video_linki %}
                <div class="mt-6 pt-6 border-t border-gray-100">
                    <a href="{{ sporcu.video_linki }}" target="_blank" class="flex items-center justify-center gap-2 w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 transition font-bold">
                        <span>▶</span> Videoyu İzle
                    </a>
                </div>
                {% endif %}
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
                <div class="bg-white rounded-xl shadow-lg p-6">
                    <h3 class="text-xl font-bold text-gray-900 mb-4 border-b pb-2 flex items-center gap-2">
                        🔄 Transfer Geçmişi
                    </h3>
                    
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm text-gray-600">
                            <thead class="bg-gray-50 text-gray-700 uppercase text-xs">
                                <tr>
                                    <th class="p-3">Sezon</th>
                                    <th class="p-3">Tarih</th>
                                    <th class="p-3">Eski Kulüp</th>
                                    <th class="p-3">Yeni Kulüp</th>
                                    <th class="p-3">Tip</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-100">
                                {% for transfer in sporcu.transferler.all %}
                                <tr class="hover:bg-gray-50">
                                    <td class="p-3 font-bold text-indigo-900">{{ transfer.sezon }}</td>
                                    <td class="p-3">{{ transfer.tarih|date:"d M Y" }}</td>
                                    <td class="p-3">
                                        <div class="flex items-center gap-2">
                                            <span class="text-red-500 text-xs">▼</span> 
                                            {{ transfer.eski_kulup.isim|default:"-" }}
                                        </div>
                                    </td>
                                    <td class="p-3">
                                        <div class="flex items-center gap-2">
                                            <span class="text-green-500 text-xs">▲</span> 
                                            <span class="font-medium text-gray-900">{{ transfer.yeni_kulup.isim|default:"-" }}</span>
                                        </div>
                                    </td>
                                    <td class="p-3 text-xs">
                                        <span class="px-2 py-1 rounded bg-gray-100 border border-gray-200">{{ transfer.tip }}</span>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="5" class="p-6 text-center text-gray-400">
                                        Transfer geçmişi bulunmuyor.
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-1">
                <div class="bg-indigo-900 text-white rounded-xl shadow-lg p-6 text-center">
                    <h3 class="font-bold text-lg mb-2">Sponsor Alanı</h3>
                    <p class="text-indigo-200 text-sm mb-4">Bu alana lig sponsorları veya menajerlik şirketi reklamları gelebilir.</p>
                    <div class="h-32 bg-indigo-800 rounded flex items-center justify-center border border-indigo-700 border-dashed">
                        Reklam Banner
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
    print("🚀 Transfer Modülü Yükleniyor...\n")
    write_file('core/models.py', MODELS_CODE)
    write_file('core/admin.py', ADMIN_CODE)
    write_file('core/templates/detay.html', DETAY_HTML)
    print("\n🎉 İŞLEM TAMAM! Şimdi veritabanını güncelle:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")

if __name__ == '__main__':
    main()