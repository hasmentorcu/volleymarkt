from django.contrib import admin
from .models import *

class SecenekInline(admin.TabularInline): model = Secenek; extra = 3
class TransferInline(admin.TabularInline): model = Transfer; extra = 1; fk_name = "sporcu"

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('isim', 'lig', 'sehir')
    list_filter = ('lig', 'sehir')

@admin.register(PuanDurumu)
class PuanDurumuAdmin(admin.ModelAdmin):
    list_display = ('kulup', 'get_lig', 'puan')
    list_filter = ('kulup__lig',)
    def get_lig(self, obj): return obj.kulup.get_lig_display()

@admin.register(Sporcu)
class SporcuAdmin(admin.ModelAdmin):
    list_display = ('isim', 'mevki', 'kulup', 'piyasa_degeri')
    list_filter = ('mevki', 'kulup__lig')
    inlines = [TransferInline]

admin.site.register(Menajer)
admin.site.register(Mac)
admin.site.register(Haber)
admin.site.register(Yorum)
admin.site.register(Bildirim)
admin.site.register(Anket, inlines=[SecenekInline])
admin.site.register(Tahmin)
