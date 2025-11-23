from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import SporcuForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

# --- ORTAK BİLDİRİM SAYACI ---
# Bu fonksiyon her view içinde tekrar tekrar yazmamak için
def get_context(request):
    ctx = {}
    if request.user.is_authenticated:
        ctx['bildirim_sayisi'] = Bildirim.objects.filter(user=request.user, okundu=False).count()
    return ctx

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
    reklam_2 = {'is_ad': True, 'image': 'https://via.placeholder.com/800x400/33FF57/FFFFFF?text=REKLAM+ALANI+2', 'link': '#'}
    manset_listesi = []
    sayac = 0
    for h in mansetler:
        manset_listesi.append(h); sayac += 1
        if sayac == 2: manset_listesi.append(reklam_1)
        if sayac == 5: manset_listesi.append(reklam_2)

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
    context.update(get_context(request)) # Bildirim sayısını ekle
    return render(request, 'index.html', context)

@login_required
def bildirimler_sayfasi(request):
    bildirimler = Bildirim.objects.filter(user=request.user).order_by('-tarih')
    # Sayfaya girince hepsini okundu yapma, kullanıcı tıklasın
    context = {'bildirimler': bildirimler}
    context.update(get_context(request))
    return render(request, 'bildirimler.html', context)

@login_required
def bildirim_temizle(request):
    Bildirim.objects.filter(user=request.user, okundu=False).update(okundu=True)
    return redirect('bildirimler_sayfasi')

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
    context = {'liderler': liderler}
    context.update(get_context(request))
    return render(request, 'liderlik.html', context)

def mac_detay(request, pk):
    mac = get_object_or_404(Mac, pk=pk)
    kullanici_tahmini = None
    if request.user.is_authenticated:
        kullanici_tahmini = Tahmin.objects.filter(user=request.user, mac=mac).first()
    context = {'mac': mac, 'kullanici_tahmini': kullanici_tahmini}
    context.update(get_context(request))
    return render(request, 'mac_detay.html', context)

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
    context = {'sporcu': sporcu}; context.update(get_context(request))
    return render(request, 'detay.html', context)
def haber_detay(request, pk): 
    h=get_object_or_404(Haber, pk=pk); b=Haber.objects.filter(kategori=h.kategori).exclude(id=h.id)[:3]
    context = {'haber': h, 'benzer_haberler': b}; context.update(get_context(request))
    return render(request, 'haber_detay.html', context)
def tum_haberler(request): 
    context={'haberler': Haber.objects.all().order_by('-tarih')}; context.update(get_context(request))
    return render(request, 'haberler.html', context)
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
    context = {'p1': p1, 'p2': p2, 'analiz': analiz}; context.update(get_context(request))
    return render(request, 'karsilastir.html', context)
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
    context={'form': SporcuForm(instance=s)}; context.update(get_context(request))
    return render(request, 'profil_duzenle.html', context)
@login_required
def menajer_panel(request): 
    context={'menajer': request.user.menajer, 'oyuncular': Sporcu.objects.filter(menajer=request.user.menajer)}; context.update(get_context(request))
    return render(request, 'menajer_panel.html', context)
@login_required
def menajer_oyuncu_ekle(request):
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES); y=f.save(commit=False); y.menajer=request.user.menajer; y.save(); return redirect('menajer_panel')
    return render(request, 'menajer_form.html', {'form': SporcuForm(), 'baslik': 'Yeni'})
@login_required
def menajer_oyuncu_duzenle(request, pk):
    s=get_object_or_404(Sporcu, pk=pk, menajer=request.user.menajer)
    if request.method=='POST': f=SporcuForm(request.POST, request.FILES, instance=s); f.save(); return redirect('menajer_panel')
    return render(request, 'menajer_form.html', {'form': SporcuForm(instance=s), 'baslik': 'Düzenle'})
# ... (Mevcut importların altına ekle)
from django.core.management import call_command
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required # Sadece adminler çalıştırabilsin
def manuel_guncelleme(request):
    # Bu fonksiyon 'tam_guncelleme' komutunu çalıştırır
    try:
        call_command('tam_guncelleme')
        return HttpResponse("✅ GÜNCELLEME BAŞARIYLA TAMAMLANDI! Siteyi kontrol edebilirsin.")
    except Exception as e:
        return HttpResponse(f"❌ HATA OLUŞTU: {str(e)}")