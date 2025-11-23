import os

# --- RENKLİ NAVBAR VE FOOTER PARÇALARI ---
NAVBAR_HTML = """
<nav class="bg-white/90 backdrop-blur-md shadow-md sticky top-0 z-50 font-sans border-t-4 border-orange-500">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="flex items-center gap-2 group">
                <div class="w-11 h-11 bg-gradient-to-br from-orange-500 via-red-500 to-purple-600 rounded-2xl rotate-3 flex items-center justify-center text-white font-extrabold text-2xl shadow-lg shadow-orange-200 group-hover:rotate-12 group-hover:scale-110 transition transform duration-300">V</div>
                <div class="flex flex-col">
                    <span class="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-orange-600 leading-none">Volley<span class="text-orange-500">Markt</span></span>
                    <span class="text-[10px] text-gray-400 tracking-[0.2em] uppercase font-bold">Türkiye'nin Voleybol Üssü</span>
                </div>
            </a>

            <div class="hidden md:flex space-x-1 items-center bg-gray-100/50 p-1 rounded-full">
                <a href="/" class="px-4 py-2 rounded-full text-gray-700 font-bold transition hover:bg-white hover:text-orange-600 hover:shadow-sm">Anasayfa</a>
                <a href="{% url 'tum_haberler' %}" class="px-4 py-2 rounded-full text-gray-700 font-bold transition hover:bg-white hover:text-orange-600 hover:shadow-sm">Haberler</a>
                <a href="/?isim=&kulup=&mevki=&min_boy=&max_boy=" class="px-4 py-2 rounded-full text-gray-700 font-bold transition hover:bg-white hover:text-orange-600 hover:shadow-sm">Oyuncular</a>
            </div>

            <div class="flex items-center gap-3">
                {% if user.is_authenticated %}
                    {% if user.menajer %}
                        <a href="{% url 'menajer_panel' %}" class="bg-gradient-to-r from-indigo-900 to-purple-800 text-white px-5 py-2 rounded-full hover:shadow-lg hover:shadow-indigo-200 text-sm font-bold flex items-center gap-2 transition transform hover:-translate-y-0.5">💼 Panel</a>
                    {% elif user.sporcu %}
                        <a href="{% url 'profil_duzenle' %}" class="bg-gradient-to-r from-orange-500 to-red-500 text-white px-5 py-2 rounded-full hover:shadow-lg hover:shadow-orange-200 text-sm font-bold flex items-center gap-2 transition transform hover:-translate-y-0.5">✏️ Profil</a>
                    {% endif %}
                    <a href="{% url 'cikis' %}" class="w-10 h-10 flex items-center justify-center rounded-full bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition">✕</a>
                {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900 font-bold hover:text-orange-500 transition">Giriş</a>
                    <a href="{% url 'kayit' %}" class="bg-gradient-to-r from-indigo-600 to-blue-500 text-white px-6 py-2 rounded-full hover:shadow-lg hover:shadow-blue-200 font-bold text-sm transition transform hover:-translate-y-0.5">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
"""

FOOTER_HTML = """
<footer class="bg-gradient-to-b from-gray-900 to-indigo-950 text-gray-300 mt-24 relative overflow-hidden">
    <div class="absolute top-0 left-0 w-full overflow-hidden leading-0 transform rotate-180">
        <svg class="relative block w-[calc(130%+1.3px)] h-[60px]" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" class="fill-gray-50"></path>
        </svg>
    </div>

    <div class="container mx-auto px-4 py-16 pt-24">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div class="col-span-1 md:col-span-2">
                <h2 class="text-3xl font-extrabold text-white mb-6 flex items-center gap-2">
                    <span class="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center text-white text-lg">V</span>
                    Volley<span class="text-orange-500">Markt</span>
                </h2>
                <p class="text-sm leading-relaxed mb-8 max-w-md opacity-80">
                    Türkiye'nin en kapsamlı voleybol veri tabanı. Sultanlar Ligi ve Efeler Ligi'nden güncel transferler, 
                    istatistikler, maç sonuçları ve oyuncu profilleri tek adreste.
                </p>
                <div class="flex gap-4">
                    <a href="#" class="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center hover:bg-gradient-to-br hover:from-blue-400 hover:to-blue-600 hover:text-white transition text-xl backdrop-blur-sm border border-white/10 hover:border-transparent hover:shadow-lg hover:shadow-blue-500/30 group"><span class="group-hover:scale-110 transition">𝕏</span></a>
                    <a href="#" class="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center hover:bg-gradient-to-br hover:from-pink-500 hover:to-purple-600 hover:text-white transition text-xl backdrop-blur-sm border border-white/10 hover:border-transparent hover:shadow-lg hover:shadow-pink-500/30 group"><span class="group-hover:scale-110 transition">📷</span></a>
                    <a href="#" class="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center hover:bg-gradient-to-br hover:from-red-500 hover:to-orange-600 hover:text-white transition text-xl backdrop-blur-sm border border-white/10 hover:border-transparent hover:shadow-lg hover:shadow-red-500/30 group"><span class="group-hover:scale-110 transition">▶</span></a>
                </div>
            </div>
            <div>
                <h3 class="text-white font-bold text-lg mb-6 border-b-2 border-orange-500 pb-2 inline-block">Hızlı Erişim</h3>
                <ul class="space-y-3 text-sm font-medium">
                    <li><a href="/" class="hover:text-orange-400 transition flex items-center gap-2"><span class="text-orange-500">→</span> Anasayfa</a></li>
                    <li><a href="{% url 'tum_haberler' %}" class="hover:text-orange-400 transition flex items-center gap-2"><span class="text-orange-500">→</span> Haber Merkezi</a></li>
                    <li><a href="#" class="hover:text-orange-400 transition flex items-center gap-2"><span class="text-orange-500">→</span> Puan Durumu</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-white font-bold text-lg mb-6 border-b-2 border-orange-500 pb-2 inline-block">İletişim</h3>
                <ul class="space-y-4 text-sm">
                    <li class="flex items-center gap-4 bg-white/5 p-3 rounded-xl border border-white/10"><span class="text-2xl">📍</span> <span class="font-medium">İstanbul, Türkiye</span></li>
                    <li class="flex items-center gap-4 bg-white/5 p-3 rounded-xl border border-white/10"><span class="text-2xl">📧</span> <span class="font-medium">info@volleymarkt.com</span></li>
                </ul>
            </div>
        </div>
        <div class="border-t border-white/10 mt-16 pt-8 text-center text-sm text-gray-500 font-medium flex flex-col md:flex-row justify-between items-center gap-4">
            <p>&copy; 2025 VolleyMarkt Turkey. Tüm hakları saklıdır.</p>
            <p class="flex gap-4"><a href="#" class="hover:text-orange-400">Kullanım Şartları</a> | <a href="#" class="hover:text-orange-400">Gizlilik</a></p>
        </div>
    </div>
</footer>
"""

# --- RENKLİ INDEX SAYFASI ---
INDEX_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt - Voleybolun Yeni Yüzü</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Outfit', sans-serif; }}
        .swiper {{ width: 100%; height: 100%; }}
        .swiper-slide {{ display: flex; justify-content: center; align-items: center; background: #000; }}
        .swiper-slide img {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.85; }}
        .text-gradient {{ background-clip: text; -webkit-background-clip: text; color: transparent; background-image: linear-gradient(to right, #4338ca, #ea580c); }}
    </style>
</head>
<body class="bg-gradient-to-br from-gray-50 via-white to-orange-50 flex flex-col min-h-screen">
    {NAVBAR_HTML}

    <main class="flex-grow container mx-auto px-4 py-10">
        
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-16">
            <div class="lg:col-span-3 h-[450px] md:h-[520px] relative rounded-[2rem] shadow-2xl shadow-indigo-200/50 overflow-hidden bg-black border-4 border-white">
                {{% if mansetler %}}
                <div class="swiper mySwiper h-full">
                    <div class="swiper-wrapper">
                        {{% for item in mansetler %}}
                            {{% if item.is_ad %}}
                                <div class="swiper-slide relative bg-gradient-to-br from-gray-900 to-indigo-900">
                                    <img src="{{{{ item.image }}}}" alt="Reklam" class="opacity-60 mix-blend-overlay">
                                    <div class="absolute top-4 right-4 bg-white/10 backdrop-blur text-white px-3 py-1 rounded-full text-xs font-bold border border-white/20 tracking-widest">SPONSOR</div>
                                    <div class="absolute inset-0 flex items-center justify-center">
                                        <span class="text-white font-black text-4xl uppercase tracking-tighter border-4 border-white p-4 transform -rotate-6 mix-blend-overlay">Reklam Alanı</span>
                                    </div>
                                </div>
                            {{% else %}}
                                <div class="swiper-slide relative">
                                    {{% if item.resim %}}<img src="{{{{ item.resim.url }}}}" alt="{{{{ item.baslik }}}}">{{% endif %}}
                                    <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-indigo-950 via-indigo-950/80 to-transparent p-8 md:p-16 text-left">
                                        <span class="bg-gradient-to-r from-orange-500 to-red-500 text-white text-xs font-bold px-4 py-1.5 rounded-full mb-4 inline-block uppercase tracking-wider shadow-lg shadow-orange-500/30">{{{{ item.get_kategori_display }}}}</span>
                                        <h2 class="text-3xl md:text-5xl font-extrabold text-white mb-6 leading-tight drop-shadow-xl">{{{{ item.baslik }}}}</h2>
                                        <a href="{{% url 'haber_detay' item.id %}}" class="group inline-flex items-center gap-3 bg-white/10 hover:bg-white text-white hover:text-indigo-900 backdrop-blur-md border border-white/30 px-6 py-3 rounded-full font-bold text-sm transition-all duration-300">Haberi Oku <span class="group-hover:translate-x-1 transition">→</span></a>
                                    </div>
                                </div>
                            {{% endif %}}
                        {{% endfor %}}
                    </div>
                    <div class="swiper-button-next !text-white/50 hover:!text-white !w-12 !h-12 bg-black/20 hover:bg-black/50 rounded-full backdrop-blur transition after:!text-2xl"></div>
                    <div class="swiper-button-prev !text-white/50 hover:!text-white !w-12 !h-12 bg-black/20 hover:bg-black/50 rounded-full backdrop-blur transition after:!text-2xl"></div>
                    <div class="swiper-pagination !bottom-8"></div>
                </div>
                {{% else %}}
                    <div class="flex items-center justify-center h-full text-white font-bold text-xl bg-indigo-950">Haber bekleniyor...</div>
                {{% endif %}}
            </div>
            <div class="hidden lg:block lg:col-span-1 h-[520px]">
                <div class="bg-gradient-to-b from-gray-200 to-gray-300 h-full rounded-[2rem] flex items-center justify-center relative group overflow-hidden shadow-xl border-4 border-white">
                    <img src="https://via.placeholder.com/400x600/2a2a72/FFF?text=SPONSOR+ALANI" class="w-full h-full object-cover mix-blend-multiply opacity-80 group-hover:scale-105 transition duration-700">
                    <div class="absolute top-4 right-4 bg-black/30 text-white text-[10px] px-3 py-1 rounded-full backdrop-blur">REKLAM</div>
                </div>
            </div>
        </div>

        <div class="relative mb-16">
             <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-orange-500 rounded-[2.5rem] rotate-1 opacity-20 blur-2xl transform scale-105"></div>
             <div class="bg-gradient-to-r from-indigo-900 via-indigo-800 to-blue-900 rounded-[2rem] shadow-2xl shadow-indigo-500/30 p-8 md:p-12 text-white relative overflow-hidden border-b-4 border-orange-500">
                <div class="absolute top-0 right-0 w-96 h-96 bg-orange-500 opacity-10 rounded-full -mr-24 -mt-24 blur-3xl mix-blend-overlay"></div>
                <div class="relative z-10">
                    <h2 class="text-3xl font-extrabold mb-8 flex items-center gap-4">
                        <span class="bg-gradient-to-br from-orange-400 to-red-600 text-white p-3 rounded-2xl shadow-lg animate-pulse">⚔️</span> 
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-white to-orange-200">Oyuncu Karşılaştır</span>
                    </h2>
                    <form action="{{% url 'karsilastir' %}}" method="GET" class="flex flex-col md:flex-row gap-6 items-center">
                        <div class="w-full md:flex-1">
                             <select name="p1" class="w-full p-5 rounded-2xl text-gray-900 font-bold text-lg focus:outline-none shadow-inner bg-white/90 backdrop-blur-sm border-4 border-transparent focus:border-orange-400 appearance-none">
                                <option value="">1. Oyuncuyu Seç 🏐</option>
                                {{% for s in tum_sporcular %}}<option value="{{{{ s.id }}}}">{{{{ s.isim }}}} ({{{{ s.kulup.isim }}}})</option>{{% endfor %}}
                            </select>
                        </div>
                        <div class="bg-gradient-to-br from-orange-500 to-red-600 text-white font-black text-3xl rounded-2xl w-20 h-20 flex items-center justify-center shadow-xl shadow-orange-500/50 shrink-0 transform rotate-3 border-4 border-white/20">VS</div>
                        <div class="w-full md:flex-1">
                            <select name="p2" class="w-full p-5 rounded-2xl text-gray-900 font-bold text-lg focus:outline-none shadow-inner bg-white/90 backdrop-blur-sm border-4 border-transparent focus:border-blue-400 appearance-none">
                                <option value="">2. Oyuncuyu Seç 🏐</option>
                                {{% for s in tum_sporcular %}}<option value="{{{{ s.id }}}}">{{{{ s.isim }}}} ({{{{ s.kulup.isim }}}})</option>{{% endfor %}}
                            </select>
                        </div>
                        <button type="submit" class="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white font-extrabold text-xl py-5 px-12 rounded-2xl shadow-xl shadow-orange-500/30 transition w-full md:w-auto hover:scale-105 active:scale-95">KIYASLA!</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-12">
            <div class="lg:col-span-3">
                <h2 class="text-3xl font-extrabold text-indigo-900 mb-8 flex items-center gap-3"><span class="text-orange-500">🔍</span> Oyuncu Havuzu</h2>
                
                <div class="bg-white p-8 rounded-[2rem] shadow-xl shadow-indigo-100/50 border border-indigo-50 mb-10 relative overflow-hidden">
                     <div class="absolute top-0 right-0 w-64 h-64 bg-orange-100 rounded-full -mr-32 -mt-32 blur-3xl opacity-50"></div>
                    <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-5 relative z-10">
                        <input type="text" name="isim" value="{{{{ secili_isim|default:'' }}}}" placeholder="İsim Ara..." class="border-2 border-gray-100 p-4 rounded-xl w-full md:col-span-4 focus:border-indigo-500 outline-none font-medium text-gray-700 bg-gray-50/50 focus:bg-white transition">
                        <select name="kulup" class="border-2 border-gray-100 p-4 rounded-xl w-full bg-gray-50/50 focus:bg-white focus:border-indigo-500 outline-none font-medium text-gray-700 appearance-none"><option value="">Tüm Kulüpler</option>{{% for k in kulupler %}}<option value="{{{{ k.id }}}}" {{% if k.id == secili_kulup %}}selected{{% endif %}}>{{{{ k.isim }}}}</option>{{% endfor %}}</select>
                        <select name="mevki" class="border-2 border-gray-100 p-4 rounded-xl w-full bg-gray-50/50 focus:bg-white focus:border-indigo-500 outline-none font-medium text-gray-700 appearance-none"><option value="">Tüm Mevkiler</option>{{% for k,v in mevkiler %}}<option value="{{{{ k }}}}" {{% if k == secili_mevki %}}selected{{% endif %}}>{{{{ v }}}}</option>{{% endfor %}}</select>
                        <div class="flex gap-3"><input type="number" name="min_boy" value="{{{{ secili_min_boy|default:'' }}}}" placeholder="Min cm" class="w-1/2 border-2 border-gray-100 p-4 rounded-xl bg-gray-50/50 focus:bg-white focus:border-indigo-500 outline-none font-medium text-gray-700"><input type="number" name="max_boy" value="{{{{ secili_max_boy|default:'' }}}}" placeholder="Max cm" class="w-1/2 border-2 border-gray-100 p-4 rounded-xl bg-gray-50/50 focus:bg-white focus:border-indigo-500 outline-none font-medium text-gray-700"></div>
                        <button type="submit" class="bg-indigo-900 hover:bg-indigo-800 text-white font-bold rounded-xl p-4 shadow-lg transition hover:-translate-y-1">Filtrele</button>
                    </form>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 gap-8">
                    {{% for sporcu in sporcular %}}
                    <a href="{{% url 'sporcu_detay' sporcu.id %}}" class="bg-white rounded-3xl shadow-md hover:shadow-2xl hover:shadow-orange-200/50 transition duration-300 group overflow-hidden border-2 border-transparent hover:border-orange-300 flex flex-col h-full transform hover:-translate-y-2">
                        <div class="h-64 bg-gray-100 relative overflow-hidden rounded-t-[1.4rem]">
                            {{% if sporcu.profil_fotografi %}}<img src="{{{{ sporcu.profil_fotografi.url }}}}" class="w-full h-full object-cover object-top group-hover:scale-110 transition duration-700">{{% endif %}}
                            <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-indigo-900 via-indigo-900/70 to-transparent p-5 pt-12">
                                <h3 class="text-white font-extrabold text-xl leading-none">{{{{ sporcu.isim }}}}</h3>
                                <p class="text-orange-300 text-sm font-bold mt-1 flex items-center gap-1"><span class="inline-block w-2 h-2 bg-orange-400 rounded-full"></span> {{{{ sporcu.kulup.isim|default:"-" }}}}</p>
                            </div>
                        </div>
                        <div class="p-5 flex justify-between items-center text-sm bg-white rounded-b-3xl flex-grow">
                            <span class="bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-full text-xs font-bold border border-indigo-100 group-hover:bg-orange-50 group-hover:text-orange-600 group-hover:border-orange-100 transition">{{{{ sporcu.get_mevki_display }}}}</span>
                            <span class="font-extrabold text-indigo-900 text-lg">{{{{ sporcu.boy }}}} <span class="text-xs text-gray-500 font-medium">cm</span></span>
                        </div>
                    </a>
                    {{% empty %}}<p class="col-span-3 text-center text-gray-400 py-16 text-lg font-medium bg-white rounded-3xl border-2 border-dashed border-gray-200">Aradığınız kriterde oyuncu bulunamadı.</p>{{% endfor %}}
                </div>
            </div>

            <div class="space-y-10">
                <div id="puan-durumu" class="bg-white rounded-[2rem] shadow-xl shadow-indigo-100/50 overflow-hidden border border-indigo-50 relative">
                    <div class="bg-gradient-to-r from-indigo-900 to-blue-800 text-white p-5 font-extrabold text-center uppercase tracking-widest text-sm shadow-md relative z-10 flex items-center justify-center gap-2">
                        <span>🏆</span> Sultanlar Ligi
                    </div>
                    <table class="w-full text-sm relative z-10">
                        {{% for sira in puan_tablosu %}}
                        <tr class="border-b border-gray-100 hover:bg-indigo-50/50 transition group">
                            <td class="p-4 font-bold flex gap-3 items-center">
                                <span class="{{% if forloop.counter <= 3 %}}bg-orange-100 text-orange-600{{% else %}}bg-gray-100 text-gray-400{{% endif %}} w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold group-hover:bg-indigo-100 group-hover:text-indigo-600 transition">{{{{ forloop.counter }}}}.</span> 
                                <span class="text-gray-800 group-hover:text-indigo-900 transition">{{{{ sira.kulup.isim }}}}</span>
                            </td>
                            <td class="p-4 font-extrabold text-right text-indigo-900 text-lg group-hover:text-orange-500 transition">{{{{ sira.puan|floatformat:0 }}}}P</td>
                        </tr>
                        {{% endfor %}}
                    </table>
                     <div class="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-indigo-50 to-transparent opacity-50 pointer-events-none"></div>
                </div>

                <div class="bg-white rounded-[2rem] shadow-xl shadow-orange-100/50 border border-orange-50 p-6 relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-48 h-48 bg-orange-100 rounded-full -mr-24 -mt-24 blur-3xl opacity-40"></div>
                    <h3 class="font-extrabold text-gray-900 mb-6 flex items-center gap-2 relative z-10"><span class="text-orange-500">📰</span> Son Gelişmeler</h3>
                    <div class="space-y-5 relative z-10">
                        {{% for haber in son_haberler %}}
                        <a href="{{% url 'haber_detay' haber.id %}}" class="flex gap-4 group bg-gray-50 hover:bg-white p-3 rounded-2xl transition border border-transparent hover:border-orange-200 hover:shadow-md">
                            <div class="w-20 h-20 bg-gray-200 rounded-xl overflow-hidden shrink-0 shadow-sm">
                                {{% if haber.resim %}}<img src="{{{{ haber.resim.url }}}}" class="w-full h-full object-cover group-hover:scale-110 transition duration-500">{{% endif %}}
                            </div>
                            <div>
                                <h4 class="text-sm font-bold text-gray-900 group-hover:text-orange-600 leading-snug mb-2 line-clamp-2 transition">{{{{ haber.baslik }}}}</h4>
                                <span class="text-[10px] text-gray-500 font-medium flex items-center gap-1"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full group-hover:bg-orange-400 transition"></span> {{{{ haber.tarih|date:"d F Y" }}}}</span>
                            </div>
                        </a>
                        {{% endfor %}}
                        <a href="{{% url 'tum_haberler' %}}" class="block text-center text-sm font-extrabold text-white bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 py-3 rounded-xl shadow-md hover:shadow-lg transition mt-6 transform hover:-translate-y-1">Tüm Haber Merkezi →</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="mt-24 pt-16 border-t border-gray-200 relative">
            <div class="absolute top-0 left-1/2 -translate-x-1/2 -mt-6 bg-white px-6 py-2 rounded-full text-gray-400 font-bold text-sm border border-gray-100 shadow-sm">İSTATİSTİK MERKEZİ</div>
            <h2 class="text-4xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-orange-600 mb-12">📊 Ligin Rakamları</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
                <div class="bg-white p-8 rounded-[2rem] shadow-xl shadow-indigo-100/50 border border-indigo-50 hover:shadow-2xl transition"><h3 class="text-center font-extrabold text-gray-700 mb-6 text-lg flex items-center justify-center gap-2"><span class="text-purple-500">●</span> Mevki Dağılımı</h3><div class="p-4"><canvas id="mevkiChart"></canvas></div></div>
                <div class="bg-white p-8 rounded-[2rem] shadow-xl shadow-blue-100/50 border border-blue-50 hover:shadow-2xl transition"><h3 class="text-center font-extrabold text-gray-700 mb-6 text-lg flex items-center justify-center gap-2"><span class="text-blue-500">●</span> En Uzunlar</h3><canvas id="boyChart"></canvas></div>
                <div class="bg-white p-8 rounded-[2rem] shadow-xl shadow-green-100/50 border border-green-50 hover:shadow-2xl transition"><h3 class="text-center font-extrabold text-gray-700 mb-6 text-lg flex items-center justify-center gap-2"><span class="text-green-500">●</span> En Değerliler</h3><canvas id="degerChart"></canvas></div>
            </div>
        </div>
    </main>

    {FOOTER_HTML}

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        new Swiper(".mySwiper", {{ spaceBetween: 0, effect: "fade", autoplay: {{ delay: 4000 }}, pagination: {{ el: ".swiper-pagination", clickable: true, dynamicBullets: true }}, navigation: {{ nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" }} }});
        // Grafikler için font ayarı
        Chart.defaults.font.family = "'Outfit', sans-serif";
        Chart.defaults.font.weight = 'bold';
        new Chart(document.getElementById('mevkiChart'), {{ type: 'doughnut', data: {{ labels: {{ mevki_labels|safe }}, datasets: [{{ data: {{ mevki_counts|safe }}, backgroundColor: ['#ec4899', '#3b82f6', '#eab308', '#22c55e', '#a855f7'], borderWidth: 0, hoverOffset: 20 }}] }}, options: {{ cutout: '70%', plugins: {{ legend: {{ position: 'bottom', labels: {{ padding: 20, usePointStyle: true }} }} }} }} }});
        new Chart(document.getElementById('boyChart'), {{ type: 'bar', data: {{ labels: {{ uzun_labels|safe }}, datasets: [{{ label: 'Boy', data: {{ uzun_values|safe }}, backgroundColor: '#3b82f6', borderRadius: 8, barThickness: 20 }}] }}, options: {{ indexAxis: 'y', scales: {{ x: {{ grid: {{ display: false }} }}, y: {{ grid: {{ display: false }} }} }}, plugins: {{ legend: {{ display: false }} }} }} }});
        new Chart(document.getElementById('degerChart'), {{ type: 'bar', data: {{ labels: {{ deger_labels|safe }}, datasets: [{{ label: 'Değer (€)', data: {{ deger_values|safe }}, backgroundColor: '#22c55e', borderRadius: 8, barThickness: 20 }}] }}, options: {{ scales: {{ x: {{ grid: {{ display: false }} }}, y: {{ grid: {{ display: false }} }} }}, plugins: {{ legend: {{ display: false }} }} }} }});
    </script>
</body>
</html>
"""

# --- RENKLİ HABERLER SAYFASI ---
HABERLER_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Haber Merkezi - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Outfit', sans-serif; }}</style>
</head>
<body class="bg-gradient-to-br from-gray-50 via-white to-indigo-50 flex flex-col min-h-screen">
    {NAVBAR_HTML}

    <main class="flex-grow container mx-auto px-4 py-12">
        <div class="text-center mb-16">
            <h1 class="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-orange-600 mb-4">Haber Merkezi</h1>
            <p class="text-gray-500 text-lg font-medium max-w-2xl mx-auto">Voleybol dünyasından en son gelişmeler, transfer haberleri ve maç analizleri.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {{% for haber in haberler %}}
            <a href="{{% url 'haber_detay' haber.id %}}" class="bg-white rounded-[2rem] shadow-lg hover:shadow-2xl hover:shadow-orange-200/50 transition duration-300 group overflow-hidden flex flex-col h-full border-2 border-transparent hover:border-orange-300 transform hover:-translate-y-2">
                <div class="h-64 overflow-hidden relative rounded-t-[2rem]">
                    {{% if haber.resim %}}
                        <img src="{{{{ haber.resim.url }}}}" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
                    {{% else %}}
                        <div class="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center text-gray-500 font-bold">Görsel Yok</div>
                    {{% endif %}}
                    <div class="absolute top-4 right-4 bg-white/90 backdrop-blur-md text-indigo-900 text-xs font-extrabold px-3 py-1.5 rounded-full shadow-sm border border-white/50">{{{{ haber.get_kategori_display }}}}</div>
                    <div class="absolute bottom-0 left-0 w-full h-24 bg-gradient-to-t from-white to-transparent"></div>
                </div>
                <div class="p-8 flex flex-col flex-grow relative">
                    <div class="text-xs text-orange-500 font-bold mb-3 flex items-center gap-2">
                        <span class="bg-orange-100 p-1 rounded-full">📅</span> {{{{ haber.tarih|date:"d F Y" }}}}
                        <span class="text-gray-300">•</span>
                        <span>{{{{ haber.tarih|date:"H:i" }}}}</span>
                    </div>
                    <h2 class="text-2xl font-extrabold text-gray-900 mb-4 leading-tight group-hover:text-orange-600 transition">{{{{ haber.baslik }}}}</h2>
                    <p class="text-gray-600 text-base line-clamp-3 mb-6 flex-grow leading-relaxed">{{{{ haber.ozet }}}}</p>
                    <span class="text-white bg-gradient-to-r from-indigo-600 to-blue-500 px-6 py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 w-full group-hover:from-orange-500 group-hover:to-red-500 transition shadow-md">Haberi Oku <span class="group-hover:translate-x-1 transition">→</span></span>
                </div>
            </a>
            {{% endfor %}}
        </div>
    </main>

    {FOOTER_HTML}
</body>
</html>
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Güncellendi: {path}")

def main():
    print("🚀 RENK VE ENERJİ PAKETİ YÜKLENİYOR...\n")
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/haberler.html', HABERLER_HTML)
    print("\n🎉 İŞLEM TAMAM! Siteyi yenile (F5). Karşında yepyeni VolleyMarkt!")

if __name__ == '__main__':
    main()