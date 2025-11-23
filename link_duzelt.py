import os

# --- DÜZELTİLMİŞ INDEX.HTML ---
# Fikstür kısmındaki <div> etiketini <a> (Link) etiketiyle değiştirdik.

INDEX_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; }
        .swiper { width: 100%; height: 100%; }
        .swiper-slide { display: flex; justify-content: center; align-items: center; background: #000; }
        .swiper-slide img { width: 100%; height: 100%; object-fit: cover; opacity: 0.85; }
    </style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    
    <nav class="bg-white/95 backdrop-blur-md shadow-md sticky top-0 z-50 font-sans border-t-4 border-orange-500">
        <div class="container mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="flex items-center gap-2 group">
                    <div class="w-11 h-11 bg-gradient-to-br from-orange-500 via-red-500 to-purple-600 rounded-2xl rotate-3 flex items-center justify-center text-white font-extrabold text-2xl shadow-lg group-hover:rotate-12 transition">V</div>
                    <div class="flex flex-col">
                        <span class="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-orange-600 leading-none">Volley<span class="text-orange-500">Markt</span></span>
                        <span class="text-[10px] text-gray-400 tracking-[0.2em] uppercase font-bold">Türkiye</span>
                    </div>
                </a>
                <div class="hidden md:flex space-x-1 items-center bg-gray-100/50 p-1 rounded-full">
                    <a href="/" class="px-4 py-2 rounded-full text-gray-700 font-bold hover:bg-white hover:text-orange-600 hover:shadow-sm transition">Anasayfa</a>
                    <a href="/haberler/" class="px-4 py-2 rounded-full text-gray-700 font-bold hover:bg-white hover:text-orange-600 hover:shadow-sm transition">Haberler</a>
                    <a href="/#oyuncular" class="px-4 py-2 rounded-full text-gray-700 font-bold hover:bg-white hover:text-orange-600 hover:shadow-sm transition">Oyuncular</a>
                </div>
                <div class="flex items-center gap-3">
                    {% if user.is_authenticated %}
                        {% if user.menajer %}<a href="/menajer-panel/" class="bg-indigo-900 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">💼 Panel</a>
                        {% elif user.sporcu %}<a href="/profil-duzenle/" class="bg-orange-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">✏️ Profil</a>{% endif %}
                        <a href="/cikis/" class="text-red-500 font-bold text-sm">Çıkış</a>
                    {% else %}
                        <a href="/giris/" class="text-indigo-900 font-bold">Giriş</a>
                        <a href="/kayit/" class="bg-indigo-900 text-white px-5 py-2 rounded-full font-bold text-sm">Kayıt Ol</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>

    <main class="flex-grow container mx-auto px-4 py-8">
        {% if messages %}
        <div class="mb-6">{% for m in messages %}<div class="p-4 rounded-lg bg-green-100 text-green-800 border-l-4 border-green-500 shadow-sm">✅ {{ m }}</div>{% endfor %}</div>
        {% endif %}

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
            <div class="lg:col-span-3 h-[450px] relative rounded-[2rem] shadow-2xl overflow-hidden bg-black">
                {% if mansetler %}
                <div class="swiper mySwiper h-full"><div class="swiper-wrapper">
                    {% for item in mansetler %}
                        {% if item.is_ad %}
                            <div class="swiper-slide relative bg-gray-900"><img src="{{ item.image }}" class="opacity-60"><div class="absolute top-4 right-4 bg-white/20 text-white px-2 py-1 rounded text-xs border">REKLAM</div></div>
                        {% else %}
                            <div class="swiper-slide relative">
                                {% if item.resim %}<img src="{{ item.resim.url }}">{% endif %}
                                <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black p-8 text-left">
                                    <span class="bg-orange-600 text-white text-xs font-bold px-3 py-1 rounded-full mb-3 inline-block">{{ item.get_kategori_display }}</span>
                                    <h2 class="text-3xl font-extrabold text-white mb-3">{{ item.baslik }}</h2>
                                    <a href="/haber/{{ item.id }}/" class="text-white border-b-2 border-orange-500 font-bold">Haberi Oku →</a>
                                </div>
                            </div>
                        {% endif %}
                    {% endfor %}
                </div><div class="swiper-button-next text-white"></div><div class="swiper-button-prev text-white"></div><div class="swiper-pagination"></div></div>
                {% else %}<div class="flex items-center justify-center h-full text-white font-bold text-xl">Haber bekleniyor...</div>{% endif %}
            </div>
            <div class="hidden lg:block lg:col-span-1 h-[450px]">
                <div class="bg-gray-200 h-full rounded-[2rem] flex items-center justify-center relative shadow-xl"><div class="absolute top-4 right-4 bg-black/30 text-white text-[10px] px-2 rounded">REKLAM</div><span class="text-gray-400 font-bold">SPONSOR ALANI</span></div>
            </div>
        </div>

        <div class="bg-gradient-to-r from-indigo-900 to-blue-900 rounded-[2rem] shadow-xl p-8 mb-12 text-white relative overflow-hidden">
            <div class="relative z-10">
                <h2 class="text-2xl font-bold mb-6 flex items-center gap-3"><span class="bg-orange-500 p-2 rounded-lg">⚔️</span> Oyuncu Karşılaştır</h2>
                <form action="/karsilastir/" method="GET" class="flex flex-col md:flex-row gap-4 items-center">
                    <select name="p1" class="w-full p-4 rounded-xl text-gray-900 font-bold"><option value="">1. Oyuncuyu Seç</option>{% for s in tum_sporcular %}<option value="{{ s.id }}">{{ s.isim }}</option>{% endfor %}</select>
                    <div class="text-orange-500 font-black text-2xl bg-white rounded-full w-12 h-12 flex items-center justify-center shadow-lg">VS</div>
                    <select name="p2" class="w-full p-4 rounded-xl text-gray-900 font-bold"><option value="">2. Oyuncuyu Seç</option>{% for s in tum_sporcular %}<option value="{{ s.id }}">{{ s.isim }}</option>{% endfor %}</select>
                    <button class="bg-orange-500 text-white font-bold py-4 px-10 rounded-xl shadow-lg hover:bg-orange-600 transition">KIYASLA</button>
                </form>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div class="lg:col-span-3" id="oyuncular">
                <div class="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 mb-8">
                    <h3 class="font-bold text-gray-800 mb-4">🔍 Filtrele</h3>
                    <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <input type="text" name="isim" value="{{ secili_isim|default:'' }}" placeholder="İsim..." class="border p-3 rounded-xl w-full md:col-span-4 bg-gray-50">
                        <select name="kulup" class="border p-3 rounded-xl w-full bg-gray-50"><option value="">Kulüp</option>{% for k in kulupler %}<option value="{{ k.id }}">{{ k.isim }}</option>{% endfor %}</select>
                        <select name="mevki" class="border p-3 rounded-xl w-full bg-gray-50"><option value="">Mevki</option>{% for k,v in mevkiler %}<option value="{{ k }}">{{ v }}</option>{% endfor %}</select>
                        <div class="flex gap-2"><input type="number" name="min_boy" placeholder="Min" class="border p-3 rounded-xl w-1/2 bg-gray-50"><input type="number" name="max_boy" placeholder="Max" class="border p-3 rounded-xl w-1/2 bg-gray-50"></div>
                        <button class="bg-indigo-900 text-white font-bold rounded-xl p-3 hover:bg-indigo-800">Filtrele</button>
                    </form>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
                    {% for sporcu in sporcular %}
                    <a href="/sporcu/{{ sporcu.id }}/" class="bg-white rounded-3xl shadow hover:shadow-2xl transition group overflow-hidden border-2 border-transparent hover:border-orange-200">
                        <div class="h-60 bg-gray-200 relative">
                            {% if sporcu.profil_fotografi %}<img src="{{ sporcu.profil_fotografi.url }}" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">{% endif %}
                            <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-indigo-900 p-4 pt-10">
                                <h3 class="text-white font-bold text-lg">{{ sporcu.isim }}</h3>
                                <p class="text-orange-300 text-xs font-bold">{{ sporcu.kulup.isim }}</p>
                            </div>
                        </div>
                        <div class="p-4 flex justify-between items-center text-sm">
                            <span class="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">{{ sporcu.get_mevki_display }}</span>
                            <span class="font-bold text-indigo-900">{{ sporcu.boy }} cm</span>
                        </div>
                    </a>
                    {% endfor %}
                </div>
            </div>

            <div class="space-y-8">
                {% if aktif_anket %}
                <div class="bg-white rounded-[2rem] shadow-xl border border-orange-100 p-6 relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-orange-100 rounded-full -mr-16 -mt-16 blur-2xl opacity-50"></div>
                    <h3 class="text-lg font-extrabold text-indigo-900 mb-4 relative z-10 flex items-center gap-2">📊 Haftanın Anketi</h3>
                    <p class="text-gray-700 font-bold mb-4 relative z-10">{{ aktif_anket.soru }}</p>
                    <form action="/oy-ver/{{ aktif_anket.id }}/" method="POST" class="relative z-10 space-y-3">
                        {% csrf_token %}
                        {% for secenek in aktif_anket.secenekler.all %}
                        <label class="flex items-center justify-between bg-gray-50 hover:bg-orange-50 p-3 rounded-xl cursor-pointer transition border border-gray-200 hover:border-orange-300 group">
                            <div class="flex items-center gap-3"><input type="radio" name="secenek" value="{{ secenek.id }}" class="w-4 h-4 text-orange-600"><span class="text-sm font-medium">{{ secenek.metin }}</span></div>
                            <span class="text-xs font-bold text-gray-400">{{ secenek.oy_sayisi }}</span>
                        </label>
                        {% endfor %}
                        <button class="w-full bg-indigo-900 text-white py-3 rounded-xl font-bold text-sm hover:bg-indigo-800 mt-4 shadow-lg">OY VER</button>
                    </form>
                </div>
                {% endif %}

                <div class="bg-white rounded-[2rem] shadow-lg overflow-hidden border border-indigo-50">
                    <div class="bg-indigo-900 text-white p-5 font-bold text-center">🏆 Sultanlar Ligi</div>
                    <table class="w-full text-sm">{% for s in puan_tablosu %}<tr class="border-b hover:bg-indigo-50 transition"><td class="p-4 font-medium">{{ forloop.counter }}. {{ s.kulup.isim }}</td><td class="p-4 font-bold text-right text-indigo-900">{{ s.puan|floatformat:0 }}</td></tr>{% endfor %}</table>
                </div>

                <div class="bg-white rounded-[2rem] shadow-lg p-6 border border-gray-100">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2 flex items-center gap-2">📅 Fikstür</h3>
                    <div class="space-y-3">
                        {% for mac in maclar %}
                        <a href="{% url 'mac_detay' mac.id %}" class="block text-sm border-b border-dashed border-gray-200 pb-3 last:border-0 last:pb-0 hover:bg-orange-50 transition p-2 rounded-lg group">
                            <div class="text-xs text-orange-600 font-bold mb-1 group-hover:text-orange-700">{{ mac.tarih|date:"d M • H:i" }}</div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700 w-1/3 text-right truncate">{{ mac.ev_sahibi.isim }}</span>
                                <span class="font-bold bg-indigo-100 text-indigo-900 px-2 py-0.5 rounded mx-1 text-xs group-hover:bg-indigo-200 transition">{{ mac.skor }}</span>
                                <span class="font-medium text-gray-700 w-1/3 truncate">{{ mac.deplasman.isim }}</span>
                            </div>
                        </a>
                        {% empty %}
                            <p class="text-xs text-gray-400 text-center">Planlanmış maç yok.</p>
                        {% endfor %}
                    </div>
                </div>

            </div>
        </div>

        <div class="mt-24 border-t pt-12">
            <h2 class="text-3xl font-extrabold text-center text-indigo-900 mb-12">İstatistik Merkezi</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white p-6 rounded-3xl shadow-lg"><canvas id="mevkiChart"></canvas></div>
                <div class="bg-white p-6 rounded-3xl shadow-lg"><canvas id="boyChart"></canvas></div>
                <div class="bg-white p-6 rounded-3xl shadow-lg"><canvas id="degerChart"></canvas></div>
            </div>
        </div>
    </main>

    <footer class="bg-gradient-to-b from-gray-900 to-indigo-950 text-gray-300 mt-24 border-t-4 border-orange-500">
        <div class="container mx-auto px-4 py-16 text-center">
            <h2 class="text-3xl font-extrabold text-white mb-4">Volley<span class="text-orange-500">Markt</span></h2>
            <p class="text-sm opacity-80">&copy; 2025 Tüm Hakları Saklıdır.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>new Swiper(".mySwiper", { autoplay: { delay: 4000 }, pagination: { clickable: true } });</script>
    <script>
        const mevkiData = { labels: {{ mevki_labels|safe }}, datasets: [{ data: {{ mevki_counts|safe }}, backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'] }] };
        const boyData = { labels: {{ uzun_labels|safe }}, datasets: [{ label: 'Boy', data: {{ uzun_values|safe }}, backgroundColor: '#36A2EB' }] };
        const degerData = { labels: {{ deger_labels|safe }}, datasets: [{ label: 'Değer', data: {{ deger_values|safe }}, backgroundColor: '#4BC0C0' }] };
        new Chart(document.getElementById('mevkiChart'), { type: 'doughnut', data: mevkiData });
        new Chart(document.getElementById('boyChart'), { type: 'bar', data: boyData, options: { indexAxis: 'y' } });
        new Chart(document.getElementById('degerChart'), { type: 'bar', data: degerData });
    </script>
</body>
</html>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ HTML Güncellendi: {path}")

def main():
    print("🚀 Link Tamir Paketi Çalışıyor...\n")
    write_file('core/templates/index.html', INDEX_HTML)
    print("\n🎉 İŞLEM TAMAM! Siteyi yenile (F5). Artık maçlara tıklayabilirsin.")

if __name__ == '__main__':
    main()