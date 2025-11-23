from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Otomatik Admin Kullanıcısı Oluşturur'

    def handle(self, *args, **kwargs):
        # Kullanıcı adı ve şifre belirliyoruz
        USERNAME = 'admin'
        EMAIL = 'admin@example.com'
        PASSWORD = 'admin123' # BURAYI İSTERSEN DEĞİŞTİR

        if not User.objects.filter(username=USERNAME).exists():
            self.stdout.write(f"👤 Admin kullanıcısı oluşturuluyor: {USERNAME}...")
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            self.stdout.write(self.style.SUCCESS(f"✅ SÜPER KULLANICI OLUŞTURULDU! Şifre: {PASSWORD}"))
        else:
            self.stdout.write("ℹ️ Admin kullanıcısı zaten var.")