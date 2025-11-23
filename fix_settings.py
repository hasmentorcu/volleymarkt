import os

def fix_settings():
    settings_path = 'volleymarkt/settings.py'
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 'import os' var mı kontrol et, yoksa en başa ekle
    if "import os" not in content:
        content = "import os\n" + content
        print("✅ 'import os' eklendi.")

    # 2. STATIC_ROOT ayarını ekle (Eğer yoksa)
    if "STATIC_ROOT =" not in content:
        # Dosyanın en altına ekleyelim
        eklenecek_kod = """

# --- DEPLOYMENT AYARLARI (OTOMATİK EKLENDİ) ---
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
"""
        content += eklenecek_kod
        print("✅ STATIC_ROOT ve WhiteNoise ayarları eklendi.")
    
    # 3. Middleware Kontrolü (WhiteNoise var mı?)
    if "whitenoise.middleware.WhiteNoiseMiddleware" not in content:
        if "'django.middleware.security.SecurityMiddleware'," in content:
            content = content.replace(
                "'django.middleware.security.SecurityMiddleware',",
                "'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
            )
            print("✅ WhiteNoise Middleware araya sıkıştırıldı.")
        else:
            print("⚠️ Middleware bulunamadı, manuel eklenmeli.")

    # Dosyayı Kaydet
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print("🎉 settings.py başarıyla güncellendi!")

if __name__ == '__main__':
    fix_settings()