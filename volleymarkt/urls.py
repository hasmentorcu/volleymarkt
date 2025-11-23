from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', anasayfa, name='anasayfa'),
    path('haberler/', tum_haberler, name='tum_haberler'),
    path('haber/<int:pk>/', haber_detay, name='haber_detay'),
    path('sporcu/<int:pk>/', sporcu_detay, name='sporcu_detay'),
    path('mac/<int:pk>/', mac_detay, name='mac_detay'),
    
    path('bildirimler/', bildirimler_sayfasi, name='bildirimler_sayfasi'),
    path('bildirim-temizle/', bildirim_temizle, name='bildirim_temizle'),
    path('tahmin-yap/<int:mac_id>/', tahmin_yap, name='tahmin_yap'),
    path('liderlik/', liderlik_tablosu, name='liderlik'),
    path('karsilastir/', karsilastir, name='karsilastir'),
    path('oy-ver/<int:anket_id>/', oy_ver, name='oy_ver'),

    path('giris/', giris_yap, name='giris'),
    path('kayit/', kayit_ol, name='kayit'),
    path('cikis/', cikis_yap, name='cikis'),
    
    path('profil-duzenle/', profil_duzenle, name='profil_duzenle'),
    path('menajer-panel/', menajer_panel, name='menajer_panel'),
    path('menajer/ekle/', menajer_oyuncu_ekle, name='menajer_oyuncu_ekle'),
    path('menajer/duzenle/<int:pk>/', menajer_oyuncu_duzenle, name='menajer_oyuncu_duzenle'),
]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
