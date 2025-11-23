import os

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

def oy_ver(request, anket_id):
    if request.method == 'POST':
        secenek_id = request.POST.get('secenek')
        if secenek_id:
            s = get_object_or_404(Secenek, id=secenek_id); s.oy_sayisi += 1; s.save()
            messages.success(request, "Oyunuz kaydedildi!")
    return redirect('anasayfa')

def sporcu_detay(request, pk):
    sporcu = get_object_or_404(Sporcu, pk=pk)
    if request.method == 'POST':
        if 'yorum_yaz' in request.POST:
            if request.user.is_authenticated:
                Yorum.objects.create(yazan=request.user, sporcu=sporcu, metin=request.POST.get('metin'))
                messages.success(request, "Yorum eklendi.")
            else: messages.error(request, "Giriş yapmalısınız.")
        elif 'begen' in request.POST:
            if request.user.is_authenticated:
                if request.user in sporcu.begeniler.all(): sporcu.begeniler.remove(request.user)
                else: sporcu.begeniler.add(request.user)
            return redirect('sporcu_detay', pk=pk)
        return redirect('sporcu_detay', pk=pk)
    return render(request, 'detay.html', {'sporcu': sporcu})

def haber_detay(request, pk):
    haber = get_object_or_404(Haber, pk=pk)
    benzer = Haber.objects.filter(kategori=haber.kategori).exclude(id=haber.id)[:3]
    return render(request, 'haber_detay.html', {'haber': haber, 'benzer_haberler': benzer})

def tum_haberler(request):
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

    # GÜVENLİ KIYASLAMA FONKSİYONU
    def kiyasla(val1, val2):
        v1 = val1 if val1 is not None else 0
        v2 = val2 if val2 is not None else 0
        
        if v1 == 0 and v2 == 0: return 0
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

# --- YARDIMCI FONKSİYONLAR ---
def giris_yap(request):
    if request.method=="POST":
        f=AuthenticationForm(request, data=request.POST)
        if f.is_valid():
            u=f.get_user(); login(request, u)
            if hasattr(u,'menajer'): return redirect('menajer_panel')
            elif hasattr(u,'sporcu'): return redirect('profil_duzenle')
            else: return redirect('anasayfa')
    return render(request, 'giris.html')
def cikis_yap(request): logout(request); return redirect('anasayfa')
def kayit_ol(request):
    if request.method=="POST":
        u=request.POST['username']; p=request.POST['password']; i=request.POST['isim']; r=request.POST['rol']
        user=User.objects.create_user(username=u, password=p)
        if r=='sporcu': Sporcu.objects.create(user=user, isim=i)
        else: Menajer.objects.create(user=user, isim=i)
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
# --- YENİ: MAÇ DETAYI ---
def mac_detay(request, pk):
    mac = get_object_or_404(Mac, pk=pk)
    return render(request, 'mac_detay.html', {'mac': mac})
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ View Düzeltildi: {path}")

if __name__ == '__main__':
    write_file('core/views.py', VIEWS_CODE)
    print("🎉 Hata çözüldü! Sayfayı yenile.")
    