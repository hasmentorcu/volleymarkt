from django.core.management.base import BaseCommand
from core.models import Tahmin, Mac

class Command(BaseCommand):
    help = 'Biten maçların tahmin puanlarını hesaplar'

    def handle(self, *args, **kwargs):
        # Henüz hesaplanmamış ama bitmiş maçların tahminlerini al
        tahminler = Tahmin.objects.filter(hesaplandi=False, mac__tamamlandi=True)
        
        if not tahminler:
            self.stdout.write("✅ Hesaplanacak yeni maç sonucu yok.")
            return

        count = 0
        for t in tahminler:
            gercek_skor = t.mac.skor.strip() # "3-1"
            tahmin_skor = t.skor.strip()     # "3-1"
            
            try:
                g_ev, g_dep = map(int, gercek_skor.split('-'))
                t_ev, t_dep = map(int, tahmin_skor.split('-'))
                
                puan = 0
                
                # 1. Tam İsabet (3 Puan)
                if gercek_skor == tahmin_skor:
                    puan = 3
                else:
                    # 2. Kazananı Bilme (1 Puan)
                    # Ev sahibi kazandıysa
                    if g_ev > g_dep and t_ev > t_dep:
                        puan = 1
                    # Deplasman kazandıysa
                    elif g_dep > g_ev and t_dep > t_ev:
                        puan = 1
                
                t.puan_kazandi = puan
                t.hesaplandi = True
                t.save()
                count += 1
                
            except:
                continue # Skor formatı bozuksa geç ("-" vs.)

        self.stdout.write(self.style.SUCCESS(f"🎉 {count} tahminin puanı hesaplandı!"))