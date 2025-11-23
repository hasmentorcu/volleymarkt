import os

# ==========================================
# 1. MODELLER (Lig Alanı Eklendi)
# ==========================================
MODELS_CODE = """from django.db import models
from django.contrib.auth.models import User

MEVKILER = (('PASOR', 'Pasör'), ('PASOR_CAPRAZI', 'Pasör Çaprazı'), ('SMACOR', 'Smaçör'), ('ORTA_OYUNCU', 'Orta Oyuncu'), ('LIBERO', 'Libero'))

# YENİ: LİG SEÇENEKLERİ
LIGLER = (
    ('SULTANLAR', 'Vodafone Sultanlar Ligi'),
    ('EFELER', 'AXA Sigorta Efeler Ligi'),
    ('KADIN_1', 'Kadınlar 1. Ligi'),
    ('ERKEK_1', 'Erkekler 1. Ligi'),
)

class Kulup(models.Model):
    isim = models.CharField(max_length=100)
    sehir = models.CharField(max_length=50)
    # YENİ ALAN: LİG
    lig = models.CharField(max_length=20, choices=LIGLER, default='SULTANLAR', verbose_name="Bulunduğu Lig")
    kurulus_yili = models.PositiveIntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='kulupler/', null=True, blank=True)
    
    def __str__(self): return f"{self.isim} ({self.get_lig_display()})"
    class Meta: verbose_name_plural = "Kulüpler"

# (Diğer modeller aynı kalıyor, kısalttım)
class Menajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True); isim = models.CharField(max_length=100); sirket_adi = models.CharField(max_length=100, blank=True); telefon = models.CharField(max_length=20, blank=True)
    def __str__(self): return self.isim

class Sporcu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True); isim = models.CharField(max_length=100); dogum_tarihi = models.DateField(null=True, blank=True); boy = models.PositiveIntegerField(null=True, blank=True); kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name="oyuncular"); menajer = models.ForeignKey(Menajer, on_delete=models.SET_NULL, null=True, blank=True); mevki = models.CharField(max_length=20, choices=MEVKILER, null=True, blank=True); piyasa_degeri = models.PositiveIntegerField(null=True, blank=True); smac_yuksekligi = models.PositiveIntegerField(null=True, blank=True); blok_yuksekligi = models.PositiveIntegerField(null=True, blank=True); profil_fotografi = models.ImageField(upload_to='sporcular/', null=True, blank=True); video_linki = models.URLField(blank=True)
    begeniler = models.ManyToManyField(User, related_name='begendigi_sporcular', blank=True)
    def __str__(self): return self.isim
    def begeni_sayisi(self): return self.begeniler.count()

class Transfer(models.Model):
    sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='transferler'); sezon = models.CharField(max_length=20); tarih = models.DateField(null=True, blank=True); eski_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='giden'); yeni_kulup = models.ForeignKey(Kulup, on_delete=models.SET_NULL, null=True, related_name='gelen'); tip = models.CharField(max_length=50, default='Bedelsiz')
    class Meta: ordering = ['-sezon', '-id']

class PuanDurumu(models.Model):
    kulup = models.OneToOneField(Kulup, on_delete=models.CASCADE); oynanan = models.PositiveIntegerField(default=0); galibiyet = models.PositiveIntegerField(default=0); maglubiyet = models.PositiveIntegerField(default=0); puan = models.FloatField(default=0)
    class Meta: ordering = ['-puan', '-galibiyet']

class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE); deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE); tarih = models.DateTimeField(); skor = models.CharField(max_length=10, blank=True, default="-"); salon = models.CharField(max_length=100, blank=True); hakemler = models.CharField(max_length=200, blank=True); set1 = models.CharField(max_length=10, blank=True); set2 = models.CharField(max_length=10, blank=True); set3 = models.CharField(max_length=10, blank=True); set4 = models.CharField(max_length=10, blank=True); set5 = models.CharField(max_length=10, blank=True); tamamlandi = models.BooleanField(default=False)
    class Meta: ordering = ['tarih']

class Haber(models.Model):
    baslik = models.CharField(max_length=200); ozet = models.TextField(max_length=500); icerik = models.TextField(); resim = models.ImageField(upload_to='haberler/'); tarih = models.DateTimeField(auto_now_add=True); kategori = models.CharField(max_length=20, choices=[('Transfer', 'Transfer'), ('Mac', 'Maç Sonucu'), ('Ozel', 'Özel Haber')], default='Ozel'); manset_mi = models.BooleanField(default=False)
    class Meta: ordering = ['-tarih']

class Yorum(models.Model):
    yazan = models.ForeignKey(User, on_delete=models.CASCADE); haber = models.ForeignKey(Haber, on_delete=models.CASCADE, related_name='yorumlar', null=True, blank=True); sporcu = models.ForeignKey(Sporcu, on_delete=models.CASCADE, related_name='yorumlar', null=True, blank=True); metin = models.TextField(); tarih = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-tarih']

class Anket(models.Model):
    soru = models.CharField(max_length=200); aktif_mi = models.BooleanField(default=True); olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.soru

class Secenek(models.Model):
    anket = models.ForeignKey(Anket, on_delete=models.CASCADE, related_name='secenekler'); metin = models.CharField(max_length=200); oy_sayisi = models.PositiveIntegerField(default=0)
    def __str__(self): return self.metin

class Tahmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tahminler'); mac = models.ForeignKey(Mac, on_delete=models.CASCADE, related_name='tahminler'); skor = models.CharField(max_length=5); puan_kazandi = models.IntegerField(default=0); hesaplandi = models.BooleanField(default=False); tarih = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('user', 'mac')

class Bildirim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bildirimler'); mesaj = models.CharField(max_length=255); okundu = models.BooleanField(default=False); tarih = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-tarih']
"""

# ==========================================
# 2. ADMIN (Lig Filtresi Eklendi)
# ==========================================
ADMIN_CODE = """from django.contrib import admin
from .models import *

class SecenekInline(admin.TabularInline): model = Secenek; extra = 3
class TransferInline(admin.TabularInline): model = Transfer; extra = 1; fk_name = "sporcu"

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('isim', 'lig', 'sehir') # Lig eklendi
    list_filter = ('lig', 'sehir')          # Lig filtresi eklendi

@admin.register(PuanDurumu)
class PuanDurumuAdmin(admin.ModelAdmin):
    list_display = ('kulup', 'kulup_lig', 'puan')
    list_filter = ('kulup__lig',) # Lige göre puan durumu süzme
    def kulup_lig(self, obj): return obj.kulup.get_lig_display()

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'kulup', 'piyasa_degeri')
    list_filter = ('mevki', 'kulup__lig') # Lige göre sporcu süzme
    inlines = [TransferInline]

# Diğerleri
admin.site.register(Menajer)
admin.site.register(Mac)
admin.site.register(Haber)
admin.site.register(Yorum)
admin.site.register(Bildirim)
admin.site.register(Anket, list_display=('soru', 'aktif_mi'), inlines=[SecenekInline])
"""

# ==========================================
# 3. VIEWS (Çoklu Lig Desteği)
# ==========================================
VIEWS_CODE = """from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

def get_context(request):
    ctx = {}
    if request.user.is_authenticated:
        ctx['bildirim_sayisi'] = Bildirim.objects.filter(user=request.user, okundu=False).count()
    return ctx

def anasayfa(request):
    # 1. FİLTRELEME
    sporcular = Sporcu.objects.all()
    # Yeni: Lig filtresi eklendi
    secili_lig = request.GET.get('lig')
    if secili_lig: sporcular = sporcular.filter(kulup__lig=secili_lig)
    
    isim = request.GET.get('isim'); kulup_id = request.GET.get('kulup'); mevki = request.GET.get('mevki'); min_boy = request.GET.get('min_boy'); max_boy = request.GET.get('max_boy')
    if isim: sporcular = sporcular.filter(isim__icontains=isim)
    if kulup_id: sporcular = sporcular.filter(kulup_id=kulup_id)
    if mevki: sporcular = sporcular.filter(mevki=mevki)
    if min_boy: sporcular = sporcular.filter(boy__gte=min_boy)
    if max_boy: sporcular = sporcular.filter(boy__lte=max_boy)

    # 2. PUAN DURUMLARI (AYRI AYRI)
    puan_sultanlar = PuanDurumu.objects.filter(kulup__lig='SULTANLAR').order_by('-puan')
    puan_efeler = PuanDurumu.objects.filter(kulup__lig='EFELER').order_by('-puan')

    # 3. HABER VE REKLAM
    mansetler = Haber.objects.filter(manset_mi=True)[:10]
    # Haber ve Reklam Objelerini View'da değil Template'de dizeceğiz bu sefer
    
    # 4. GRAFİKLER (Sadece Sultanlar için örnek, genellenebilir)
    mevki_data = sporcular.values('mevki').annotate(total=Count('id'))
    mevki_labels = [m['mevki'] for m in mevki_data]; mevki_counts = [m['total'] for m in mevki_data]
    
    context = {
        'sporcular': sporcular, 
        'puan_sultanlar': puan_sultanlar, 'puan_efeler': puan_efeler, # Ayrı gönderdik
        'maclar': Mac.objects.all().order_by('tarih')[:5],
        'kulupler': Kulup.objects.all(), 'mevkiler': MEVKILER, 
        'mansetler': mansetler, 'son_haberler': Haber.objects.all().order_by('-tarih')[:6],
        'aktif_anket': Anket.objects.filter(aktif_mi=True).last(),
        'mevki_labels': mevki_labels, 'mevki_counts': mevki_counts,
        'tum_sporcular': Sporcu.objects.all().order_by('isim'),
        
        # Filtre değerlerini geri gönder
        'secili_lig': secili_lig, 'secili_isim': isim, 'secili_kulup': int(kulup_id) if kulup_id else None,
        'secili_mevki': mevki, 'secili_min_boy': min_boy, 'secili_max_boy': max_boy,
    }
    context.update(get_context(request))
    return render(request, 'index.html', context)

# --- Diğer Viewlar (Kısaltıldı, aynı) ---
def mac_detay(request, pk):
    mac = get_object_or_404(Mac, pk=pk); t=None
    if request.user.is_authenticated: t=Tahmin.objects.filter(user=request.user, mac=mac).first()
    c={'mac':mac, 'kullanici_tahmini':t}; c.update(get_context(request)); return render(request, 'mac_detay.html', c)
def haber_detay(request, pk): h=get_object_or_404(Haber, pk=pk); b=Haber.objects.filter(kategori=h.kategori).exclude(id=h.id)[:3]; c={'haber':h, 'benzer_haberler':b}; c.update(get_context(request)); return render(request, 'haber_detay.html', c)
def tum_haberler(request): c={'haberler':Haber.objects.all().order_by('-tarih')}; c.update(get_context(request)); return render(request, 'haberler.html', c)
def sporcu_detay(request, pk): s=get_object_or_404(Sporcu, pk=pk); c={'sporcu':s}; c.update(get_context(request)); return render(request, 'detay.html', c)
def karsilastir(request):
    id1=request.GET.get('p1'); id2=request.GET.get('p2'); 
    if not id1 or not id2: return redirect('anasayfa')
    p1=get_object_or_404(Sporcu, id=id1); p2=get_object_or_404(Sporcu, id=id2)
    def k(v1,v2): v1=v1 or 0; v2=v2 or 0; return 1 if v1>v2 else (2 if v2>v1 else 0)
    analiz={'boy':k(p1.boy,p2.boy), 'smac':k(p1.smac_yuksekligi,p2.smac_yuksekligi), 'deger':k(p1.piyasa_degeri,p2.piyasa_degeri)}
    c={'p1':p1, 'p2':p2, 'analiz':analiz}; c.update(get_context(request)); return render(request, 'karsilastir.html', c)
def liderlik_tablosu(request): l=User.objects.annotate(toplam_puan=Sum('tahminler__puan_kazandi')).order_by('-toplam_puan')[:20]; c={'liderler':l}; c.update(get_context(request)); return render(request, 'liderlik.html', c)
@login_required
def tahmin_yap(request, mac_id):
    if request.method=='POST': Tahmin.objects.update_or_create(user=request.user, mac_id=mac_id, defaults={'skor':request.POST.get('skor')}); messages.success(request, "Tahmin Kaydedildi")
    return redirect('mac_detay', pk=mac_id)
def oy_ver(request, anket_id): 
    if request.method=='POST': s=get_object_or_404(Secenek, id=request.POST.get('secenek')); s.oy_sayisi+=1; s.save()
    return redirect('anasayfa')
def giris_yap(request): 
    if request.method=="POST": 
        f=AuthenticationForm(request, data=request.POST)
        if f.is_valid(): login(request, f.get_user()); return redirect('anasayfa')
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
def bildirimler_sayfasi(request): c={'bildirimler': Bildirim.objects.filter(user=request.user).order_by('-tarih')}; c.update(get_context(request)); return render(request, 'bildirimler.html', c)
@login_required
def bildirim_temizle(request): Bildirim.objects.filter(user=request.user, okundu=False).update(okundu=True); return redirect('bildirimler_sayfasi')
@login_required
def profil_duzenle(request): 
    try: s=request.user.sporcu; f=SporcuForm(instance=s)
    except: return redirect('anasayfa')
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES, instance=s); f.save() if f.is_valid() else None; return redirect('sporcu_detay', pk=s.id)
    c={'form':f}; c.update(get_context(request)); return render(request, 'profil_duzenle.html', c)
@login_required
def menajer_panel(request): c={'menajer':request.user.menajer, 'oyuncular':Sporcu.objects.filter(menajer=request.user.menajer)}; c.update(get_context(request)); return render(request, 'menajer_panel.html', c)
@login_required
def menajer_oyuncu_ekle(request): 
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES); y=f.save(commit=False); y.menajer=request.user.menajer; y.save(); return redirect('menajer_panel')
    return render(request, 'menajer_form.html', {'form':SporcuForm(), 'baslik':'Yeni'})
@login_required
def menajer_oyuncu_duzenle(request, pk):
    s=get_object_or_404(Sporcu, pk=pk, menajer=request.user.menajer)
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES, instance=s); f.save(); return redirect('menajer_panel')
    return render(request, 'menajer_form.html', {'form':SporcuForm(instance=s), 'baslik':'Düzenle'})
"""

# ==========================================
# 4. HTML (Reklam ve Lig Tabları Eklendi)
# ==========================================

NAVBAR_HTML = """
<nav class="bg-white/95 backdrop-blur-md shadow-md sticky top-0 z-50 font-sans border-t-4 border-orange-500">
    <div class="bg-gray-100 py-2 hidden md:block border-b">
        <div class="container mx-auto text-center">
            <img src="https://via.placeholder.com/728x90/333/FFF?text=HEADER+REKLAM+ALANI+(728x90)" class="mx-auto rounded shadow-sm">
        </div>
    </div>

    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="flex items-center gap-2 group">
                <div class="w-11 h-11 bg-gradient-to-br from-orange-500 via-red-500 to-purple-600 rounded-2xl rotate-3 flex items-center justify-center text-white font-extrabold text-2xl shadow-lg group-hover:rotate-12 transition">V</div>
                <div class="flex flex-col">
                    <span class="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-orange-600 leading-none">Volley<span class="text-orange-500">Markt</span></span>
                    <span class="text-[10px] text-gray-400 tracking-[0.2em] uppercase font-bold">Türkiye</span>
                </div>
            </a>

            <div class="hidden md:flex items-center space-x-6">
                <a href="/" class="text-gray-700 hover:text-orange-600 font-bold transition">Anasayfa</a>
                
                <div class="relative group">
                    <button class="flex items-center gap-1 text-gray-700 hover:text-orange-600 font-bold transition">
                        Ligler ▾
                    </button>
                    <div class="absolute left-0 top-full mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition transform group-hover:translate-y-0 translate-y-2 z-50">
                        <a href="/?lig=SULTANLAR" class="block px-4 py-3 hover:bg-orange-50 hover:text-orange-600 rounded-t-xl border-b border-gray-50 font-medium">🏆 Sultanlar Ligi</a>
                        <a href="/?lig=EFELER" class="block px-4 py-3 hover:bg-blue-50 hover:text-blue-600 font-medium">🏐 Efeler Ligi</a>
                        <a href="/?lig=KADIN_1" class="block px-4 py-3 hover:bg-gray-50 text-gray-600 text-sm">Kadınlar 1. Lig</a>
                        <a href="/?lig=ERKEK_1" class="block px-4 py-3 hover:bg-gray-50 text-gray-600 text-sm rounded-b-xl">Erkekler 1. Lig</a>
                    </div>
                </div>

                <a href="/haberler/" class="text-gray-700 hover:text-orange-600 font-bold transition">Haberler</a>
                <a href="/#oyuncular" class="text-gray-700 hover:text-orange-600 font-bold transition">Oyuncular</a>
            </div>

            <div class="flex items-center gap-3">
                {% if user.is_authenticated %}
                    <a href="/bildirimler/" class="relative p-2 rounded-full bg-gray-100 hover:text-orange-600 transition">🔔{% if bildirim_sayisi > 0 %}<span class="absolute top-0 right-0 bg-red-600 text-white text-[10px] w-4 h-4 flex items-center justify-center rounded-full">{{ bildirim_sayisi }}</span>{% endif %}</a>
                    {% if user.menajer %}<a href="/menajer-panel/" class="bg-indigo-900 text-white px-3 py-1.5 rounded-lg text-sm font-bold shadow-md">💼</a>{% elif user.sporcu %}<a href="/profil-duzenle/" class="bg-orange-500 text-white px-3 py-1.5 rounded-lg text-sm font-bold shadow-md">✏️</a>{% endif %}
                    <a href="/cikis/" class="text-red-500 font-bold text-sm">Çıkış</a>
                {% else %}
                    <a href="/giris/" class="text-indigo-900 font-bold">Giriş</a>
                    <a href="/kayit/" class="bg-indigo-900 text-white px-4 py-1.5 rounded-lg font-bold text-sm shadow">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
"""

INDEX_HTML_BODY = """
<body class="bg-gray-50 flex flex-col min-h-screen">
    __NAVBAR__

    <main class="flex-grow container mx-auto px-4 py-8">
        {% if messages %}<div class="mb-6">{% for m in messages %}<div class="p-4 rounded-lg bg-green-100 text-green-800 shadow-sm">✅ {{ m }}</div>{% endfor %}</div>{% endif %}

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
            <div class="lg:col-span-3 h-[450px] relative rounded-[2rem] shadow-2xl overflow-hidden bg-black">
                {% if mansetler %}
                <div class="swiper mySwiper h-full"><div class="swiper-wrapper">
                    {% for item in mansetler %}
                    <div class="swiper-slide relative">
                        {% if item.resim %}<img src="{{ item.resim.url }}">{% endif %}
                        <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black p-8 text-left">
                            <span class="bg-orange-600 text-white text-xs font-bold px-3 py-1 rounded-full">{{ item.get_kategori_display }}</span>
                            <h2 class="text-3xl font-extrabold text-white">{{ item.baslik }}</h2>
                            <a href="/haber/{{ item.id }}/" class="text-white border-b-2 border-orange-500 font-bold">Oku →</a>
                        </div>
                    </div>
                    {% endfor %}
                    
                    <div class="swiper-slide relative bg-gray-900">
                        <img src="https://via.placeholder.com/800x450/111/FFF?text=SLIDER+İÇİ+REKLAM+ALANI" class="opacity-70">
                        <div class="absolute top-4 right-4 bg-white/20 text-white px-2 py-1 rounded text-xs">REKLAM</div>
                    </div>

                </div><div class="swiper-button-next text-white"></div><div class="swiper-button-prev text-white"></div><div class="swiper-pagination"></div></div>
                {% else %}<div class="flex items-center justify-center h-full text-white font-bold text-xl">Haber Bekleniyor...</div>{% endif %}
            </div>
            <div class="hidden lg:block lg:col-span-1 h-[450px] bg-gray-200 rounded-[2rem] flex items-center justify-center shadow-xl overflow-hidden relative group">
                <img src="https://via.placeholder.com/400x600/222/FFF?text=YAN+REKLAM+(300x600)" class="w-full h-full object-cover">
                <div class="absolute top-2 right-2 bg-white text-black text-[10px] px-2 rounded">REKLAM</div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div class="lg:col-span-3" id="oyuncular">
                <div class="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 mb-8">
                    <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        {% if secili_lig %}<input type="hidden" name="lig" value="{{ secili_lig }}">{% endif %}
                        
                        <input type="text" name="isim" value="{{ secili_isim|default:'' }}" placeholder="İsim..." class="border p-3 rounded-xl w-full md:col-span-4 bg-gray-50">
                        <select name="kulup" class="border p-3 rounded-xl w-full bg-gray-50"><option value="">Kulüp</option>{% for k in kulupler %}<option value="{{ k.id }}">{{ k.isim }}</option>{% endfor %}</select>
                        <select name="mevki" class="border p-3 rounded-xl w-full bg-gray-50"><option value="">Mevki</option>{% for k,v in mevkiler %}<option value="{{ k }}">{{ v }}</option>{% endfor %}</select>
                        <div class="flex gap-2"><input type="number" name="min_boy" placeholder="Min" class="border p-3 rounded-xl w-1/2 bg-gray-50"><input type="number" name="max_boy" placeholder="Max" class="border p-3 rounded-xl w-1/2 bg-gray-50"></div>
                        <button class="bg-indigo-900 text-white font-bold rounded-xl p-3 hover:bg-indigo-800">Filtrele</button>
                    </form>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
                    {% for sporcu in sporcular %}
                        
                        {% if forloop.counter == 5 %}
                        <div class="col-span-2 md:col-span-3 bg-gray-100 rounded-xl flex items-center justify-center h-32 border-2 border-dashed border-gray-300 text-gray-400 font-bold">
                            LİSTE ARASI REKLAM ALANI (Responsive)
                        </div>
                        {% endif %}

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
                <div class="bg-white rounded-[2rem] shadow-lg overflow-hidden border border-indigo-50">
                    <div class="flex text-center font-bold cursor-pointer">
                        <div class="w-1/2 p-4 bg-indigo-900 text-white" onclick="openTab('sultanlar')">🏆 Sultanlar</div>
                        <div class="w-1/2 p-4 bg-gray-100 text-gray-600 hover:bg-gray-200" onclick="openTab('efeler')">🏐 Efeler</div>
                    </div>
                    
                    <div id="tab-sultanlar">
                        <table class="w-full text-sm">
                            {% for s in puan_sultanlar %}
                            <tr class="border-b hover:bg-indigo-50 transition"><td class="p-4 font-medium">{{ forloop.counter }}. {{ s.kulup.isim }}</td><td class="p-4 font-bold text-right text-indigo-900">{{ s.puan|floatformat:0 }}</td></tr>
                            {% empty %}<tr><td colspan="2" class="p-4 text-center text-gray-400">Veri Yok</td></tr>{% endfor %}
                        </table>
                    </div>
                    <div id="tab-efeler" class="hidden">
                        <table class="w-full text-sm">
                            {% for s in puan_efeler %}
                            <tr class="border-b hover:bg-blue-50 transition"><td class="p-4 font-medium">{{ forloop.counter }}. {{ s.kulup.isim }}</td><td class="p-4 font-bold text-right text-blue-900">{{ s.puan|floatformat:0 }}</td></tr>
                            {% empty %}<tr><td colspan="2" class="p-4 text-center text-gray-400">Veri Yok</td></tr>{% endfor %}
                        </table>
                    </div>
                </div>

                <div class="bg-gray-100 h-64 rounded-xl flex items-center justify-center border border-gray-300 text-gray-400 font-bold">
                    KARE REKLAM (300x250)
                </div>
                
                <div class="bg-white rounded-[2rem] shadow-lg p-6 border border-gray-100">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2 flex items-center gap-2">📅 Fikstür</h3>
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
    </main>
    __FOOTER__
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        new Swiper(".mySwiper", { autoplay: { delay: 4000 }, pagination: { clickable: true } });
        function openTab(tabName) {
            document.getElementById('tab-sultanlar').classList.add('hidden');
            document.getElementById('tab-efeler').classList.add('hidden');
            document.getElementById('tab-' + tabName).classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

# --- EFELER LİGİ VERİSİNİ EKLEYEN BOT ---
EFELER_BOT = """from django.core.management.base import BaseCommand
from core.models import Kulup, PuanDurumu

class Command(BaseCommand):
    help = 'Efeler Ligi takımlarını ekler'

    def handle(self, *args, **kwargs):
        takimlar = [
            "Halkbank", "Fenerbahçe Parolapara", "Ziraat Bankkart", "Galatasaray HDI Sigorta", "Arkas Spor", "Spor Toto"
        ]
        
        for t in takimlar:
            k, _ = Kulup.objects.get_or_create(isim=t, defaults={'lig': 'EFELER', 'sehir': 'Türkiye'})
            PuanDurumu.objects.get_or_create(kulup=k, defaults={'puan': 0})
            self.stdout.write(f"✅ Efeler Ligi Takımı Eklendi: {t}")
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path} Güncellendi.")

def main():
    print("🚀 BÜYÜME PAKETİ (V2) BAŞLATILIYOR...\n")
    write_file('core/models.py', MODELS_CODE)
    write_file('core/admin.py', ADMIN_CODE)
    write_file('core/views.py', VIEWS_CODE)
    write_file('core/templates/index.html', INDEX_HTML_BODY.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML.replace('__NAVBAR__', ''))) # Footer içinde navbar yok
    
    # Efeler Ligi Botu
    write_file('core/management/commands/efeler_yukle.py', EFELER_BOT)

    print("\n🎉 İŞLEM TAMAM! Şimdi sırasıyla:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py efeler_yukle")
    print("4. python manage.py runserver")

if __name__ == '__main__':
    main()