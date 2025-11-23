from django.shortcuts import render, get_object_or_404, redirect
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
