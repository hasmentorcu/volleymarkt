import os
import sys
import subprocess

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def generate_requirements():
    print("📄 requirements.txt oluşturuluyor...")
    with open('requirements.txt', 'w') as f:
        subprocess.check_call([sys.executable, "-m", "pip", "freeze"], stdout=f)

def create_build_sh():
    print("🔨 build.sh oluşturuluyor...")
    content = """#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
"""
    # Dosyayı binary modda yazmıyoruz ama Linux uyumlu satır sonu (\n) kullanıyoruz
    with open('build.sh', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def update_settings():
    print("⚙️ settings.py güncelleniyor (ALLOWED_HOSTS)...")
    settings_path = 'volleymarkt/settings.py'
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ALLOWED_HOSTS ayarını tüm dünyaya açalım (Render için gerekli)
    if "ALLOWED_HOSTS = []" in content:
        content = content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']")
        print("✅ ALLOWED_HOSTS = ['*'] yapıldı.")
    elif "ALLOWED_HOSTS = ['*']" in content:
        print("ℹ️ ALLOWED_HOSTS zaten ayarlı.")
    else:
        print("⚠️ ALLOWED_HOSTS otomatik değiştirilemedi, lütfen manuel kontrol et.")

    # Static dosyalar için gerekli ayar (Whitenoise) - Render için kritik
    if "whitenoise" not in content:
        # Middleware ekle
        if "'django.middleware.security.SecurityMiddleware'," in content:
            content = content.replace(
                "'django.middleware.security.SecurityMiddleware',",
                "'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
            )
            print("✅ WhiteNoise Middleware eklendi.")
        
        # Static ayarları güncelle
        if "STATIC_URL = '/static/'" in content:
            extra_static = "\nSTATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')\nSTATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n"
            content = content.replace("STATIC_URL = 'static/'", "STATIC_URL = '/static/'" + extra_static)
            # Bazen slash olmaz
            content = content.replace("STATIC_URL = '/static/'", "STATIC_URL = '/static/'" + extra_static)
            print("✅ Static Root ayarları eklendi.")

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("🚀 DEPLOYMENT HAZIRLIĞI BAŞLIYOR...\n")
    
    # 1. Gunicorn ve Whitenoise Kur (Sunucu için şart)
    print("📦 Gunicorn ve Whitenoise yükleniyor...")
    install_package("gunicorn")
    install_package("whitenoise")
    
    # 2. Dosyaları Oluştur
    generate_requirements()
    create_build_sh()
    
    # 3. Ayarları Düzenle
    update_settings()
    
    print("\n🎉 HAZIRLIK TAMAMLANDI!")
    print("Şimdi şu komutlarla GitHub'a gönder:")
    print("1. git add .")
    print("2. git commit -m 'Deployment hazırlığı'")
    print("3. git push")

if __name__ == '__main__':
    main()