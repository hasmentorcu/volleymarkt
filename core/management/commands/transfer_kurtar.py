from django.core.management.base import BaseCommand
from core.models import Sporcu, Kulup, Transfer

class Command(BaseCommand):
    help = 'Transfer verilerini manuel olarak kurtarır ve yükler'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚑 Transfer Verileri Kurtarılıyor...")

        # 1. ZEHRA GÜNEŞ VERİLERİ
        self.yukle("Zehra Güneş", [
            ("2011-2014", "VakıfBank Altyapı", "Bedelsiz"),
            ("2014-2015", "İstanbul BBSK", "Kiralık"),
            ("2015-2016", "VakıfBank", "Kiralık Dönüşü"),
            ("2016-2017", "Beşiktaş", "Kiralık"),
            ("2017-Günümüz", "VakıfBank", "Sözleşme Yenileme"),
        ], 450000) # Piyasa Değeri

        # 2. EDA ERDEM VERİLERİ
        self.yukle("Eda Erdem Dündar", [
            ("2000-2004", "Beşiktaş Altyapı", "Bedelsiz"),
            ("2004-2008", "Beşiktaş", "Profesyonel"),
            ("2008-Günümüz", "Fenerbahçe Opet", "Bonservis"),
        ], 300000)

        # 3. HANDE BALADIN VERİLERİ
        self.yukle("Hande Baladın", [
            ("2010-2014", "Eczacıbaşı Altyapı", "Bedelsiz"),
            ("2014-2015", "Sarıyer Bld.", "Kiralık"),
            ("2015-2018", "Eczacıbaşı Dynavit", "Kiralık Dönüşü"),
            ("2018-2019", "Galatasaray", "Kiralık"),
            ("2019-Günümüz", "Eczacıbaşı Dynavit", "Sözleşme Yenileme"),
        ], 350000)

        # 4. MELİSSA VARGAS VERİLERİ
        self.yukle("Melissa Vargas", [
            ("2014-2015", "Cienfuegos", "Bedelsiz"),
            ("2015-2016", "Agel Prostejov", "Bonservis"),
            ("2016-2018", "Volero Zürich", "Bonservis"),
            ("2018-Günümüz", "Fenerbahçe Opet", "Bonservis"),
            ("2021", "Tianjin Bohai Bank", "Kiralık"),
        ], 850000)

        self.stdout.write(self.style.SUCCESS("🎉 Operasyon Başarılı! Veriler geri yüklendi."))

    def yukle(self, isim, transferler, deger):
        # İsmi biraz esnek arayalım (Zehra Güneş veya Zehra Gunes)
        sporcu = Sporcu.objects.filter(isim__icontains=isim).first()
        
        if not sporcu:
            self.stdout.write(self.style.WARNING(f"⚠️ {isim} veritabanında bulunamadı, atlanıyor."))
            return

        # Eski verileri temizle (Garanti olsun)
        sporcu.transferler.all().delete()
        
        # Piyasa Değerini Güncelle
        sporcu.piyasa_degeri = deger
        sporcu.save()

        # Transferleri Ekle
        for sezon, kulup_adi, tip in transferler:
            kulup, _ = Kulup.objects.get_or_create(isim=kulup_adi, defaults={'sehir': 'Türkiye'})
            
            Transfer.objects.create(
                sporcu=sporcu,
                sezon=sezon,
                yeni_kulup=kulup,
                tip=tip
            )
        
        self.stdout.write(f"✅ {isim} transferleri eklendi.")