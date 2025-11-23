import os

# ==========================================
# 1. ORTAK HTML PARÇALARI (En Başta Tanımlı)
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
# 2. MODELLER
# ==========================================
MODELS_CODE = """from django.db import models
from django.contrib.auth.models import User

MEVKILER = (('PASOR', 'Pasör'), ('PASOR_CAPRAZI', 'Pasör Çaprazı'), ('SMACOR', 'Smaçör'), ('ORTA_OYUNCU', 'Orta Oyuncu'), ('LIBERO', 'Libero'))

class Kulup(models.Model):
    isim = models.CharField(max_length=100); sehir = models.CharField(max_length=50); kurulus_yili = models.PositiveIntegerField(null=True, blank=True); logo = models.ImageField(upload_to='kulupler/', null=True, blank=True)
    def __str__(self): return self.isim

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

# --- MAÇ MODELİ (GÜNCELLENMİŞ) ---
class Mac(models.Model):
    ev_sahibi = models.ForeignKey(Kulup, related_name='ev_maclari', on_delete=models.CASCADE, verbose_name="Ev Sahibi")
    deplasman = models.ForeignKey(Kulup, related_name='dep_maclari', on_delete=models.CASCADE, verbose_name="Deplasman")
    tarih = models.DateTimeField(verbose_name="Tarih ve Saat")
    skor = models.CharField(max_length=10, blank=True, default="-", verbose_name="Maç Skoru", help_text="Örn: 3-1")
    salon = models.CharField(max_length=100, blank=True, verbose_name="Salon Adı", help_text="Örn: Burhan Felek")
    hakemler = models.CharField(max_length=200, blank=True, verbose_name="Hakemler", help_text="Örn: Nurper Özbar, Erol Akbulut")
    set1 = models.CharField(max_length=10, blank=True, verbose_name="1. Set", help_text="25-18")
    set2 = models.CharField(max_length=10, blank=True, verbose_name="2. Set", help_text="22-25")
    set3 = models.CharField(max_length=10, blank=True, verbose_name="3. Set", help_text="25-15")
    set4 = models.CharField(max_length=10, blank=True, verbose_name="4. Set")
    set5 = models.CharField(max_length=10, blank=True, verbose_name="5. Set") # Tie-break
    tamamlandi = models.BooleanField(default=False, verbose_name="Maç Bitti")
    class Meta: ordering = ['tarih']; verbose_name_plural = "Fikstür / Maçlar"
    def __str__(self): return f"{self.ev_sahibi} vs {self.deplasman}"

# --- TAHMİN MODELİ ---
class Tahmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tahminler')
    mac = models.ForeignKey(Mac, on_delete=models.CASCADE, related_name='tahminler')
    SKOR_SECENEKLERI = [('3-0', '3-0'), ('3-1', '3-1'), ('3-2', '3-2'), ('0-3', '0-3'), ('1-3', '1-3'), ('2-3', '2-3')]
    skor = models.CharField(max_length=5, choices=SKOR_SECENEKLERI)
    puan_kazandi = models.IntegerField(default=0, help_text="Maç bitince hesaplanır")
    hesaplandi = models.BooleanField(default=False)
    tarih = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('user', 'mac')
"""

# ==========================================
# 3. VIEWS
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
    mansetler = list(Haber.objects.filter(manset_mi=True)[:10])
    reklam_1 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/FF5733/FFFFFF?text=REKLAM+ALANI+1', 'link': '#'}
    manset_listesi = []
    sayac = 0
    for h in mansetler:
        manset_listesi.append(h); sayac += 1
        if sayac == 2: manset_listesi.append(reklam_1)

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
        'secili_mevki': mevki, 'secili_min_boy': min_boy, 'secili_max_boy': max_boy, 'mansetler': manset_listesi,
        'son_haberler': son_haberler, 'aktif_anket': aktif_anket, 'mevki_labels': mevki_labels, 'mevki_counts': mevki_counts,
        'uzun_labels': uzun_labels, 'uzun_values': uzun_values, 'deger_labels': deger_labels, 'deger_values': deger_values,
    }
    return render(request, 'index.html', context)

@login_required
def tahmin_yap(request, mac_id):
    mac = get_object_or_404(Mac, pk=mac_id)
    if request.method == 'POST':
        skor = request.POST.get('skor')
        Tahmin.objects.update_or_create(user=request.user, mac=mac, defaults={'skor': skor})
        messages.success(request, f"Tahmininiz ({skor}) kaydedildi!")
    return redirect('mac_detay', pk=mac_id)

def liderlik_tablosu(request):
    liderler = User.objects.annotate(toplam_puan=Sum('tahminler__puan_kazandi')).order_by('-toplam_puan')[:20]
    return render(request, 'liderlik.html', {'liderler': liderler})

def mac_detay(request, pk):
    mac = get_object_or_404(Mac, pk=pk)
    kullanici_tahmini = None
    if request.user.is_authenticated:
        kullanici_tahmini = Tahmin.objects.filter(user=request.user, mac=mac).first()
    return render(request, 'mac_detay.html', {'mac': mac, 'kullanici_tahmini': kullanici_tahmini})

def oy_ver(request, anket_id):
    if request.method == 'POST':
        s=get_object_or_404(Secenek, id=request.POST.get('secenek')); s.oy_sayisi+=1; s.save(); messages.success(request, "Oyunuz kaydedildi!")
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
def haber_detay(request, pk): h=get_object_or_404(Haber, pk=pk); b=Haber.objects.filter(kategori=h.kategori).exclude(id=h.id)[:3]; return render(request, 'haber_detay.html', {'haber': h, 'benzer_haberler': b})
def tum_haberler(request): return render(request, 'haberler.html', {'haberler': Haber.objects.all().order_by('-tarih')})
def karsilastir(request):
    id1 = request.GET.get('p1'); id2 = request.GET.get('p2')
    if not id1 or not id2: return redirect('anasayfa')
    p1 = get_object_or_404(Sporcu, id=id1); p2 = get_object_or_404(Sporcu, id=id2)
    def k(v1, v2):
        v1 = v1 if v1 else 0; v2 = v2 if v2 else 0
        if v1 > v2: return 1
        elif v2 > v1: return 2
        return 0
    analiz = {'boy': k(p1.boy, p2.boy), 'smac': k(p1.smac_yuksekligi, p2.smac_yuksekligi), 'blok': k(p1.blok_yuksekligi, p2.blok_yuksekligi), 'deger': k(p1.piyasa_degeri, p2.piyasa_degeri)}
    return render(request, 'karsilastir.html', {'p1': p1, 'p2': p2, 'analiz': analiz})
def giris_yap(request):
    if request.method=="POST":
        f=AuthenticationForm(request, data=request.POST)
        if f.is_valid(): u=f.get_user(); login(request, u); return redirect('anasayfa')
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
# 4. HTML DOSYALARI (Navbar/Footer Gömülü)
# ==========================================

MAC_DETAY_HTML_BODY = """
<body class="bg-gray-100 flex flex-col min-h-screen">
    __NAVBAR__

    <main class="flex-grow container mx-auto px-4 py-12">
        {% if messages %}<div class="mb-6">{% for m in messages %}<div class="p-4 rounded-lg bg-green-100 text-green-800 shadow-sm">✅ {{ m }}</div>{% endfor %}</div>{% endif %}

        <div class="bg-gradient-to-r from-indigo-900 to-blue-900 rounded-[2rem] shadow-2xl p-8 md:p-12 text-white relative overflow-hidden mb-8">
            <div class="absolute top-0 left-0 w-64 h-64 bg-orange-500 opacity-10 rounded-full -ml-24 -mt-24 blur-3xl"></div>
            <div class="relative z-10 flex flex-col md:flex-row justify-between items-center text-center md:text-left gap-8">
                <div class="flex-1 flex flex-col items-center">
                    <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center p-2 shadow-lg">{% if mac.ev_sahibi.logo %}<img src="{{ mac.ev_sahibi.logo.url }}" class="w-full h-full object-contain">{% else %}<span class="text-gray-400 font-bold text-2xl">E</span>{% endif %}</div>
                    <h2 class="text-2xl font-bold mt-4">{{ mac.ev_sahibi.isim }}</h2>
                </div>
                <div class="flex-1 flex flex-col items-center">
                    <div class="bg-white/20 backdrop-blur px-4 py-1 rounded-full text-sm font-bold mb-4 border border-white/30">{{ mac.tarih|date:"d F Y • H:i" }}</div>
                    <div class="text-6xl md:text-8xl font-black tracking-tighter leading-none flex items-center gap-4"><span>{{ mac.skor|default:"v" }}</span></div>
                    {% if mac.tamamlandi %}<span class="text-green-400 font-bold mt-2 tracking-widest uppercase text-sm">MAÇ SONUCU</span>{% else %}<span class="text-orange-400 font-bold mt-2 tracking-widest uppercase text-sm animate-pulse">CANLI / OYNANMADI</span>{% endif %}
                </div>
                <div class="flex-1 flex flex-col items-center">
                    <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center p-2 shadow-lg">{% if mac.deplasman.logo %}<img src="{{ mac.deplasman.logo.url }}" class="w-full h-full object-contain">{% else %}<span class="text-gray-400 font-bold text-2xl">D</span>{% endif %}</div>
                    <h2 class="text-2xl font-bold mt-4">{{ mac.deplasman.isim }}</h2>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="md:col-span-1 bg-white rounded-[2rem] shadow-lg p-8 border border-orange-100 relative overflow-hidden">
                <div class="absolute top-0 right-0 w-32 h-32 bg-orange-500 opacity-5 rounded-full -mr-16 -mt-16"></div>
                <h3 class="text-xl font-bold text-indigo-900 mb-6 flex items-center gap-2"><span class="bg-orange-100 text-orange-600 p-2 rounded-lg text-sm">🔮</span> Skor Tahmini</h3>
                
                {% if user.is_authenticated %}
                    {% if mac.tamamlandi %}
                        <div class="bg-gray-100 p-4 rounded-xl text-center text-gray-500">Maç tamamlandı, tahmin kapalı.</div>
                        {% if kullanici_tahmini %}
                            <div class="mt-4 text-center">
                                <p class="text-sm text-gray-500">Senin Tahminin:</p>
                                <p class="text-2xl font-bold text-indigo-900">{{ kullanici_tahmini.skor }}</p>
                                <p class="text-xs font-bold {% if kullanici_tahmini.puan_kazandi > 0 %}text-green-600{% else %}text-red-500{% endif %}">+{{ kullanici_tahmini.puan_kazandi }} Puan</p>
                            </div>
                        {% endif %}
                    {% else %}
                        {% if kullanici_tahmini %}
                            <div class="bg-green-50 border border-green-200 p-4 rounded-xl text-center">
                                <p class="text-green-800 font-medium">Tahminin Kaydedildi:</p>
                                <p class="text-3xl font-black text-green-900 mt-2">{{ kullanici_tahmini.skor }}</p>
                                <button onclick="document.getElementById('tahminForm').classList.remove('hidden'); this.classList.add('hidden');" class="text-xs text-green-600 underline mt-2 cursor-pointer">Değiştir</button>
                            </div>
                        {% endif %}
                        
                        <form action="{% url 'tahmin_yap' mac.id %}" method="POST" id="tahminForm" class="space-y-4 {% if kullanici_tahmini %}hidden{% endif %}">
                            {% csrf_token %}
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-2">Skor Seçin:</label>
                                <div class="grid grid-cols-3 gap-2">
                                    <button type="submit" name="skor" value="3-0" class="border-2 border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 py-2 rounded-lg font-bold text-indigo-900 transition">3-0</button>
                                    <button type="submit" name="skor" value="3-1" class="border-2 border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 py-2 rounded-lg font-bold text-indigo-900 transition">3-1</button>
                                    <button type="submit" name="skor" value="3-2" class="border-2 border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 py-2 rounded-lg font-bold text-indigo-900 transition">3-2</button>
                                    <button type="submit" name="skor" value="0-3" class="border-2 border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 py-2 rounded-lg font-bold text-indigo-900 transition">0-3</button>
                                    <button type="submit" name="skor" value="1-3" class="border-2 border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 py-2 rounded-lg font-bold text-indigo-900 transition">1-3</button>
                                    <button type="submit" name="skor" value="2-3" class="border-2 border-gray-200 hover:border-indigo-500 hover:bg-indigo-50 py-2 rounded-lg font-bold text-indigo-900 transition">2-3</button>
                                </div>
                            </div>
                        </form>
                    {% endif %}
                {% else %}
                    <div class="bg-orange-50 p-6 rounded-xl text-center border border-orange-100">
                        <p class="text-orange-800 mb-3 font-medium">Tahmin yapmak için giriş yapmalısın.</p>
                        <a href="/giris/" class="bg-orange-500 text-white px-6 py-2 rounded-lg font-bold text-sm hover:bg-orange-600 transition shadow block">Giriş Yap</a>
                    </div>
                {% endif %}
                
                <div class="mt-6 pt-6 border-t border-gray-100 text-center">
                    <a href="{% url 'liderlik' %}" class="text-indigo-600 font-bold text-sm hover:underline">🏆 Liderlik Tablosunu Gör</a>
                </div>
            </div>

            <div class="md:col-span-2 bg-white rounded-[2rem] shadow-lg p-8 border border-gray-100">
                <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2"><span class="bg-indigo-100 text-indigo-600 p-2 rounded-lg text-sm">📊</span> Set Sonuçları & Detaylar</h3>
                {% if mac.set1 %}
                <div class="grid grid-cols-5 gap-2 text-center mb-8">
                    <div class="bg-gray-50 p-3 rounded-xl"><div class="text-xs text-gray-400 font-bold uppercase">1. Set</div><div class="text-lg font-black text-indigo-900">{{ mac.set1 }}</div></div>
                    {% if mac.set2 %}<div class="bg-gray-50 p-3 rounded-xl"><div class="text-xs text-gray-400 font-bold uppercase">2. Set</div><div class="text-lg font-black text-indigo-900">{{ mac.set2 }}</div></div>{% endif %}
                    {% if mac.set3 %}<div class="bg-gray-50 p-3 rounded-xl"><div class="text-xs text-gray-400 font-bold uppercase">3. Set</div><div class="text-lg font-black text-indigo-900">{{ mac.set3 }}</div></div>{% endif %}
                    {% if mac.set4 %}<div class="bg-gray-50 p-3 rounded-xl"><div class="text-xs text-gray-400 font-bold uppercase">4. Set</div><div class="text-lg font-black text-indigo-900">{{ mac.set4 }}</div></div>{% endif %}
                    {% if mac.set5 %}<div class="bg-orange-50 p-3 rounded-xl border border-orange-100"><div class="text-xs text-orange-400 font-bold uppercase">TB</div><div class="text-lg font-black text-orange-600">{{ mac.set5 }}</div></div>{% endif %}
                </div>
                {% else %}<p class="text-gray-400 italic text-center py-4 mb-8">Set detayları henüz girilmemiş.</p>{% endif %}
                
                <ul class="space-y-4">
                    <li class="flex items-start gap-3"><span class="text-xl">📍</span><div><div class="text-xs text-gray-400 font-bold uppercase">Salon</div><div class="font-medium text-gray-800">{{ mac.salon|default:"Belirtilmemiş" }}</div></div></li>
                    <li class="flex items-start gap-3"><span class="text-xl">🚩</span><div><div class="text-xs text-gray-400 font-bold uppercase">Hakemler</div><div class="font-medium text-gray-800">{{ mac.hakemler|default:"Belirtilmemiş" }}</div></div></li>
                </ul>
            </div>
        </div>
    </main>
    __FOOTER__
</body>
</html>
"""

LIDERLIK_HTML_BODY = """
<body class="bg-gray-100 flex flex-col min-h-screen">
    __NAVBAR__

    <main class="flex-grow container mx-auto px-4 py-12 max-w-3xl">
        <div class="text-center mb-12">
            <h1 class="text-4xl font-extrabold text-indigo-900 mb-4">🏆 Tahmin Ligi Liderleri</h1>
            <p class="text-gray-600">Doğru skor tahminleriyle zirveye oynayan en iyi voleybol gurmeleri.</p>
        </div>

        <div class="bg-white rounded-[2rem] shadow-xl overflow-hidden border border-indigo-100">
            <table class="w-full text-left">
                <thead class="bg-indigo-900 text-white uppercase text-sm tracking-wider">
                    <tr><th class="p-5 text-center w-16">#</th><th class="p-5">Kullanıcı</th><th class="p-5 text-center">Puan</th></tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    {% for user in liderler %}
                    <tr class="hover:bg-indigo-50 transition group">
                        <td class="p-5 text-center font-bold text-gray-400 group-hover:text-indigo-600">{% if forloop.counter == 1 %}🥇{% elif forloop.counter == 2 %}🥈{% elif forloop.counter == 3 %}🥉{% else %}{{ forloop.counter }}{% endif %}</td>
                        <td class="p-5 font-bold text-gray-800 text-lg flex items-center gap-3"><div class="w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-red-500 text-white flex items-center justify-center text-sm shadow">{{ user.username.0|upper }}</div>{{ user.username }}</td>
                        <td class="p-5 text-center font-black text-2xl text-indigo-900 group-hover:text-orange-500 transition">{{ user.toplam_puan|default:"0" }}</td>
                    </tr>
                    {% empty %}<tr><td colspan="3" class="p-8 text-center text-gray-400">Henüz puan durumu oluşmadı.</td></tr>{% endfor %}
                </tbody>
            </table>
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
    print("🚀 TAHMİN MODÜLÜ HATASIZ YÜKLENİYOR...\n")
    
    # 1. Models & Views
    write_file('core/models.py', MODELS_CODE)
    write_file('core/views.py', VIEWS_CODE)
    
    # 2. HTML'leri Birleştir
    mac_detay_full = MAC_DETAY_HTML_BODY.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML)
    liderlik_full = LIDERLIK_HTML_BODY.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML)
    
    write_file('core/templates/mac_detay.html', mac_detay_full)
    write_file('core/templates/liderlik.html', liderlik_full)
    
    print("\n🎉 İŞLEM TAMAM! Şimdi şu komutları çalıştır:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")

if __name__ == '__main__':
    main()