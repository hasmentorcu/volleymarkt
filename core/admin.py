from django.contrib import admin
from .models import *

class SecenekInline(admin.TabularInline): model = Secenek; extra = 3
class TransferInline(admin.TabularInline): model = Transfer; extra = 1; fk_name = "sporcu"

@admin.register(Mac)
class MacAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'ev_sahibi', 'skor', 'deplasman', 'salon', 'tamamlandi')
    list_filter = ('tamamlandi', 'tarih')
    fieldsets = (
        ('Temel Bilgiler', {'fields': ('ev_sahibi', 'deplasman', 'tarih', 'salon', 'hakemler')}),
        ('Sonuç', {'fields': ('tamamlandi', 'skor')}),
        ('Set Detayları', {'fields': ('set1', 'set2', 'set3', 'set4', 'set5')}),
    )

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'kulup', 'piyasa_degeri')
    list_filter = ('mevki', 'kulup')
    inlines = [TransferInline]

# Diğerleri standart
admin.site.register(Kulup)
admin.site.register(Menajer)
admin.site.register(PuanDurumu)
admin.site.register(Haber)
admin.site.register(Anket, list_display=('soru', 'aktif_mi'), inlines=[SecenekInline])
admin.site.register(Yorum)
