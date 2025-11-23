#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Kütüphaneleri Yükle
pip install -r requirements.txt

# 2. Statik Dosyaları Topla
python manage.py collectstatic --no-input

# 3. Veritabanını Kur
python manage.py migrate

# 4. Admin Kullanıcısını Oluştur (Bizim yazdığımız komut)
python manage.py auto_admin