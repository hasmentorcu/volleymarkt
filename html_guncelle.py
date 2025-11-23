import os

# --- ANKETLİ INDEX ---
# (Önceki renkli tasarıma Anket Widget'ı eklenmiş hali)
INDEX_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>body { font-family: 'Outfit', sans-serif; } .swiper { width: 100%; height: 100%; } .swiper-slide img { width: 100%; height: 100%; object-fit: cover; opacity: 0.85; }</style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    <nav class="bg-white/90 backdrop-blur-md shadow-md sticky top-0 z-50 font-sans border-t-4 border-orange-500">
        <div class="container mx-auto px-4 flex justify-between items-center h-16">
            <a href="/" class="flex items-center gap-2 group"><div class="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">V</div><span class="text-2xl font-extrabold text-indigo-900">Volley<span class="text-orange-500">Markt</span></span></a>
            <div class="flex gap-3">{% if user.is_authenticated %}<a href="/cikis/" class="text-red-500 font-bold">Çıkış</a>{% else %}<a href="/giris/" class="text-indigo-900 font-bold">Giriş</a>{% endif %}</div>
        </div>
    </nav>

    <main class="flex-grow container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
            <div class="lg:col-span-3 h-[450px] rounded-2xl overflow-hidden bg-black shadow-xl">
                {% if mansetler %}
                <div class="swiper mySwiper h-full"><div class="swiper-wrapper">
                    {% for item in mansetler %}
                    <div class="swiper-slide relative">
                        {% if item.resim %}<img src="{{ item.resim.url }}">{% endif %}
                        <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black p-8"><h2 class="text-3xl font-bold text-white">{{ item.baslik }}</h2></div>
                    </div>
                    {% endfor %}
                </div></div>
                {% endif %}
            </div>
            <div class="hidden lg:block lg:col-span-1 h-[450px] bg-gray-200 rounded-2xl flex items-center justify-center">REKLAM</div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div class="lg:col-span-3">
                <h2 class="text-2xl font-bold text-indigo-900 mb-6">Oyuncular</h2>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
                    {% for sporcu in sporcular %}
                    <a href="{% url 'sporcu_detay' sporcu.id %}" class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden">
                        <div class="h-56 bg-gray-200 relative">
                            {% if sporcu.profil_fotografi %}<img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover">{% endif %}
                            <div class="absolute bottom-0 left-0 w-full bg-black/60 p-3 text-white font-bold">{{ sporcu.isim }}</div>
                        </div>
                        <div class="p-3 flex justify-between text-sm"><span class="text-gray-600">{{ sporcu.get_mevki_display }}</span><span class="font-bold">{{ sporcu.boy }} cm</span></div>
                    </a>
                    {% endfor %}
                </div>
            </div>

            <div class="space-y-8">
                {% if aktif_anket %}
                <div class="bg-white rounded-xl shadow-lg border-t-4 border-indigo-900 p-6">
                    <h3 class="text-lg font-bold text-indigo-900 mb-4 flex items-center gap-2">📊 Haftanın Anketi</h3>
                    <p class="text-gray-700 font-medium mb-4">{{ aktif_anket.soru }}</p>
                    <form action="{% url 'oy_ver' aktif_anket.id %}" method="POST" class="space-y-2">
                        {% csrf_token %}
                        {% for secenek in aktif_anket.secenekler.all %}
                        <label class="flex items-center justify-between bg-gray-50 p-3 rounded cursor-pointer hover:bg-indigo-50">
                            <div class="flex items-center gap-2"><input type="radio" name="secenek" value="{{ secenek.id }}"><span>{{ secenek.metin }}</span></div>
                            <span class="text-xs font-bold text-gray-400">{{ secenek.oy_sayisi }} Oy</span>
                        </label>
                        {% endfor %}
                        <button class="w-full bg-orange-500 text-white py-2 rounded font-bold mt-2">Oy Ver</button>
                    </form>
                </div>
                {% endif %}

                <div class="bg-white rounded-xl shadow overflow-hidden">
                    <div class="bg-indigo-900 text-white p-3 font-bold text-center">Sultanlar Ligi</div>
                    <table class="w-full text-sm">{% for s in puan_tablosu %}<tr class="border-b"><td class="p-2">{{ forloop.counter }}. {{ s.kulup.isim }}</td><td class="p-2 font-bold text-right">{{ s.puan|floatformat:0 }}</td></tr>{% endfor %}</table>
                </div>
            </div>
        </div>
    </main>
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>new Swiper(".mySwiper", { autoplay: { delay: 4000 } });</script>
</body>
</html>
"""

# --- YORUMLU DETAY ---
DETAY_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{ sporcu.isim }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>body { font-family: 'Outfit', sans-serif; }</style>
</head>
<body class="bg-gray-100 flex flex-col min-h-screen">
    <nav class="bg-white/90 shadow-md p-4 sticky top-0 z-50"><div class="container mx-auto"><a href="/" class="text-2xl font-extrabold text-indigo-900">Volley<span class="text-orange-500">Markt</span></a></div></nav>

    <main class="flex-grow container mx-auto px-4 py-8">
        <div class="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col md:flex-row mb-8">
            <div class="md:w-1/3 bg-gray-200 relative min-h-[400px]">
                {% if sporcu.profil_fotografi %}<img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover absolute inset-0">{% endif %}
                
                <div class="absolute bottom-4 right-4 z-10">
                    <form method="POST">{% csrf_token %}<button name="begen" class="bg-white/90 text-red-500 px-4 py-2 rounded-full shadow-lg font-bold hover:scale-105 transition flex items-center gap-2">❤️ {{ sporcu.begeni_sayisi }}</button></form>
                </div>
            </div>
            <div class="p-8 md:w-2/3">
                <h1 class="text-4xl font-bold text-gray-900 mb-2">{{ sporcu.isim }}</h1>
                <p class="text-xl text-indigo-600 font-medium mb-6">{{ sporcu.kulup.isim }} | {{ sporcu.get_mevki_display }}</p>
                
                <div class="grid grid-cols-3 gap-4 mb-8 text-center">
                    <div class="bg-gray-50 p-4 rounded border"><div class="text-3xl font-bold text-indigo-900">{{ sporcu.boy }}</div><div class="text-xs font-bold text-gray-500">BOY</div></div>
                    <div class="bg-gray-50 p-4 rounded border"><div class="text-3xl font-bold text-indigo-900">{{ sporcu.smac_yuksekligi|default:"-" }}</div><div class="text-xs font-bold text-gray-500">SMAÇ</div></div>
                    <div class="bg-gray-50 p-4 rounded border"><div class="text-3xl font-bold text-indigo-900">€ {{ sporcu.piyasa_degeri|default:"-" }}</div><div class="text-xs font-bold text-gray-500">DEĞER</div></div>
                </div>
            </div>
        </div>

        <div class="max-w-4xl mx-auto mt-12">
            <h3 class="text-2xl font-bold text-indigo-900 mb-6">💬 Taraftar Yorumları</h3>
            {% if user.is_authenticated %}
            <form method="POST" class="mb-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                {% csrf_token %}
                <input type="hidden" name="yorum_yaz" value="1">
                <textarea name="metin" rows="3" class="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500" placeholder="Yorum yaz..."></textarea>
                <button class="mt-3 bg-orange-500 text-white px-6 py-2 rounded-lg font-bold">Gönder</button>
            </form>
            {% else %}<p class="mb-8 bg-blue-50 p-4 text-blue-800 rounded">Yorum yapmak için <a href="/giris/" class="font-bold underline">giriş yap.</a></p>{% endif %}

            <div class="space-y-4">
                {% for yorum in sporcu.yorumlar.all %}
                <div class="bg-white p-4 rounded-xl shadow-sm flex gap-4 border border-gray-50">
                    <div class="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold">{{ yorum.yazan.username.0|upper }}</div>
                    <div>
                        <div class="flex items-center gap-2 mb-1"><span class="font-bold">{{ yorum.yazan.username }}</span><span class="text-xs text-gray-400">{{ yorum.tarih|timesince }} önce</span></div>
                        <p class="text-gray-700 text-sm">{{ yorum.metin }}</p>
                    </div>
                </div>
                {% empty %}<p class="text-gray-400 text-center">Henüz yorum yok.</p>{% endfor %}
            </div>
        </div>
    </main>
</body>
</html>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ HTML Güncellendi: {path}")

def main():
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/detay.html', DETAY_HTML)
    print("\n🎉 TASARIM TAMAMLANDI! Siteyi yenile.")

if __name__ == '__main__':
    main()
    