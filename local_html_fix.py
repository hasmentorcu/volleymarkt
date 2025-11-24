import os
import sys

# --- BU KODDAKİ NAVBAR/FOOTER İÇERİKLERİ KESİNLİKLE EKSİKSİZ VE DOĞRU ÇALIŞAN VERSİYONDUR ---
NAVBAR_HTML = """<nav class="bg-gradient-to-r from-indigo-900 via-purple-900 to-indigo-900 shadow-lg sticky top-0 z-50 font-sans border-b-4 border-orange-500"><div class="container mx-auto px-4"><div class="flex justify-between items-center h-18 py-3"><a href="/" class="flex items-center gap-3 group"><div class="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-indigo-900 font-black text-2xl shadow-lg group-hover:rotate-12 transition transform">V</div><div class="flex flex-col"><span class="text-2xl font-extrabold text-white tracking-tight leading-none">Volley<span class="text-orange-400">Markt</span></span><span class="text-[10px] text-indigo-300 tracking-widest">TÜRKİYE</span></div></a><div class="hidden md:flex items-center space-x-2 bg-white/10 p-1.5 rounded-full backdrop-blur-sm border border-white/10"><a href="/" class="px-4 py-2 rounded-full text-white font-bold hover:bg-white hover:text-indigo-900 transition">🏠 Anasayfa</a><a href="/haberler/" class="px-4 py-2 rounded-full text-white font-bold hover:bg-white hover:text-indigo-900 transition">📰 Haberler</a><a href="/magaza/" class="px-4 py-2 rounded-full text-white font-bold hover:bg-white hover:text-indigo-900 transition">🪙 Mağaza</a><a href="/oyunlar/" class="px-4 py-2 rounded-full text-white font-bold hover:bg-white hover:text-indigo-900 transition">🎮 Oyunlar</a><a href="/karsilastir/" class="px-4 py-2 rounded-full text-white font-bold hover:bg-white hover:text-indigo-900 transition">⚔️ VS</a></div><div class="flex items-center gap-4">{% if user.is_authenticated %}<div class="hidden lg:flex flex-col items-end text-white text-xs font-bold"><span class="text-yellow-300">{{ profil.puan }} P</span><span class="opacity-70">Seviye {{ profil.seviye }}</span></div><a href="/bildirimler/" class="relative p-2 rounded-full bg-white/10 hover:bg-orange-500 text-white transition">🔔{% if bildirim_sayisi > 0 %}<span class="absolute top-0 right-0 bg-red-600 text-white text-[10px] w-4 h-4 flex items-center justify-center rounded-full border border-white">{{ bildirim_sayisi }}</span>{% endif %}</a><a href="/hesabim/" class="bg-white text-indigo-900 px-4 py-1.5 rounded-lg text-sm font-bold shadow-md hover:scale-105 transition flex items-center gap-2">👤 Hesabım</a><a href="/cikis/" class="text-red-300 hover:text-white font-bold text-sm">Çıkış</a>{% else %}<a href="/giris/" class="text-white font-bold hover:text-orange-300">Giriş</a><a href="/kayit/" class="bg-orange-500 text-white px-5 py-2 rounded-xl font-bold text-sm shadow-lg hover:bg-orange-600 transition transform hover:-translate-y-0.5">Kayıt Ol</a>{% endif %}</div></div></div></nav>"""
FOOTER_HTML = """<footer class="bg-gray-900 text-gray-300 mt-24 border-t-4 border-orange-500 pb-8"><div class="container mx-auto px-4 py-16 text-center"><h2 class="text-3xl font-extrabold text-white mb-4">Volley<span class="text-orange-500">Markt</span></h2><p class="text-sm opacity-80">&copy; 2025 Tüm Hakları Saklıdır.</p></div></footer><button onclick="window.scrollTo({top: 0, behavior: 'smooth'});" class="fixed bottom-8 right-8 bg-orange-500 text-white p-4 rounded-full shadow-xl hover:bg-orange-600 transition transform hover:scale-110 z-50 border-4 border-white/20">⬆</button>"""

# MAĞAZA HTML
MAGAZA_HTML = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><title>Mağaza</title><script src="https://cdn.tailwindcss.com"></script><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet"><style>body { font-family: 'Outfit', sans-serif; }</style></head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    __NAVBAR__
    <main class="flex-grow container mx-auto px-4 py-12">
        <div class="bg-indigo-900 text-white p-8 rounded-[2rem] shadow-xl mb-12 flex justify-between items-center"><div><h1 class="text-4xl font-black mb-2">Mağaza & Görevler</h1><p class="opacity-80">Puanlarını harca, ödüller kazan.</p></div><div class="text-right"><div class="text-sm opacity-70">BAKİYENİZ</div><div class="text-5xl font-black text-yellow-400">{{ profil.puan }} P</div></div></div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div><h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">📝 Aktif Görevler</h2><div class="space-y-4">{% for gorev in gorevler %}<div class="bg-white p-6 rounded-2xl shadow-md flex justify-between items-center border-l-4 border-green-500"><div><h3 class="font-bold text-lg">{{ gorev.baslik }}</h3><p class="text-gray-500 text-sm">{{ gorev.aciklama }}</p></div><div class="text-center"><span class="block font-black text-green-600 text-xl">+{{ gorev.odul }}</span><a href="/gorev-yap/{{ gorev.id }}/" class="bg-green-100 text-green-700 px-4 py-1 rounded-lg text-sm font-bold hover:bg-green-200 transition mt-2 inline-block">Tamamla</a></div></div>{% empty %}<p class="text-gray-400 text-center py-8 bg-white rounded-xl">Tüm görevleri tamamladın!</p>{% endfor %}</div></div>
            <div><h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">🛍️ Ürünler</h2><div class="grid grid-cols-2 gap-4">{% for urun in urunler %}<div class="bg-white p-4 rounded-2xl shadow-md hover:shadow-xl transition text-center border border-gray-100"><div class="h-32 bg-gray-100 rounded-xl mb-4 flex items-center justify-center text-4xl">🎁</div><h3 class="font-bold text-gray-900">{{ urun.isim }}</h3><div class="text-yellow-500 font-black text-xl my-2">{{ urun.fiyat }} P</div><a href="/magaza/satin-al/{{ urun.id }}/" class="block w-full bg-indigo-900 text-white py-2 rounded-lg font-bold hover:bg-indigo-700 transition text-sm">Satın Al</a></div>{% empty %}<p class="text-gray-400 col-span-2 text-center">Mağazada ürün yok.</p>{% endfor %}</div></div>
        </div>
    </main>
    __FOOTER__
</body></html>"""

# OYUNLAR HTML
OYUNLAR_HTML = """<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><title>Oyunlar</title><script src="https://cdn.tailwindcss.com"></script><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet"><style>body { font-family: 'Outfit', sans-serif; }</style></head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    __NAVBAR__
    <main class="flex-grow container mx-auto px-4 py-12 text-center">
        <h1 class="text-4xl font-black text-indigo-900 mb-8">🎮 Voleybol Oyunları</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="bg-white p-8 rounded-[2rem] shadow-xl hover:scale-105 transition border-b-8 border-orange-500"><div class="text-6xl mb-4">🏐</div><h2 class="text-2xl font-bold mb-2">Smaç Yarışması</h2><p class="text-gray-500 mb-6">Zamanlamanı ayarla, en sert smacı vur!</p><button class="bg-orange-500 text-white px-6 py-3 rounded-xl font-bold w-full">OYNA</button></div>
            <div class="bg-white p-8 rounded-[2rem] shadow-xl hover:scale-105 transition border-b-8 border-blue-500"><div class="text-6xl mb-4">🧠</div><h2 class="text-2xl font-bold mb-2">Voleybol Quiz</h2><p class="text-gray-500 mb-6">Oyuncuları ne kadar tanıyorsun?</p><button class="bg-blue-500 text-white px-6 py-3 rounded-xl font-bold w-full">OYNA</button></div>
             <div class="bg-white p-8 rounded-[2rem] shadow-xl hover:scale-105 transition border-b-8 border-green-500"><div class="text-6xl mb-4">🔮</div><h2 class="text-2xl font-bold mb-2">Skor Tahmin</h2><p class="text-gray-500 mb-6">Maç sonuçlarını bil, puan kazan.</p><a href="/" class="block bg-green-500 text-white px-6 py-3 rounded-xl font-bold w-full">TAHMİN YAP</a></div>
        </div>
    </main>
    __FOOTER__
</body></html>"""

def write_file(path, content):
    # Dizin yoksa oluştur
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("🚀 GEREKLİ HTML DOSYALARI OLUŞTURULUYOR...\n")
    
    # 1. Klasörleri garanti et
    os.makedirs('core/templates', exist_ok=True)
    
    # 2. Dosyaları yaz
    write_file('core/templates/magaza.html', MAGAZA_HTML.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML))
    write_file('core/templates/oyunlar.html', OYUNLAR_HTML.replace('__NAVBAR__', NAVBAR_HTML).replace('__FOOTER__', FOOTER_HTML))
    
    print("✅ Mağaza ve Oyunlar HTML'leri oluşturuldu.")

if __name__ == '__main__':
    main()