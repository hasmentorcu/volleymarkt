import os

# --- ORTAK PARÇALAR (Header ve Footer) ---

NAVBAR_HTML = """
    <nav class="bg-white shadow-md p-4 mb-8 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="flex items-center gap-3 group">
                <div class="w-10 h-10 bg-gradient-to-tr from-orange-500 to-red-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg group-hover:rotate-12 transition">
                    V
                </div>
                <div class="text-2xl font-bold text-indigo-900 tracking-tight">
                    Volley<span class="text-orange-500">Markt</span>
                    <span class="text-xs block font-normal text-gray-400 -mt-1 tracking-widest uppercase">Turkey</span>
                </div>
            </a>

            <div class="flex items-center space-x-4">
                {% if user.is_authenticated %}
                    {% if user.menajer %}
                         <a href="{% url 'menajer_panel' %}" class="bg-indigo-900 text-white px-4 py-2 rounded-lg hover:bg-indigo-800 text-sm font-bold flex items-center gap-2 shadow-md transition">
                            💼 Panel
                        </a>
                    {% elif user.sporcu %}
                         <a href="{% url 'profil_duzenle' %}" class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 text-sm font-bold flex items-center gap-2 shadow-md transition">
                            ✏️ Profilim
                        </a>
                    {% endif %}
                    <a href="{% url 'cikis' %}" class="text-gray-500 hover:text-red-500 text-sm font-medium">Çıkış</a>
                {% else %}
                    <a href="{% url 'giris' %}" class="text-indigo-900 font-bold hover:text-orange-500 transition">Giriş</a>
                    <a href="{% url 'kayit' %}" class="border-2 border-indigo-900 text-indigo-900 px-4 py-1.5 rounded-lg hover:bg-indigo-900 hover:text-white transition font-bold text-sm">Kayıt Ol</a>
                {% endif %}
            </div>
        </div>
    </nav>
"""

FOOTER_HTML = """
    <footer class="bg-indigo-900 text-white mt-20 border-t-4 border-orange-500">
        <div class="container mx-auto px-4 py-12">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div class="col-span-1 md:col-span-2">
                    <h2 class="text-2xl font-bold text-white mb-4">Volley<span class="text-orange-500">Markt</span></h2>
                    <p class="text-indigo-200 text-sm leading-relaxed mb-6">
                        Türkiye'nin en kapsamlı voleybol veri tabanı. Sultanlar Ligi ve Efeler Ligi'nden güncel transferler, 
                        istatistikler ve oyuncu profilleri tek adreste.
                    </p>
                    <div class="flex gap-4">
                        <a href="#" class="w-8 h-8 bg-indigo-800 rounded flex items-center justify-center hover:bg-orange-500 transition">𝕏</a>
                        <a href="#" class="w-8 h-8 bg-indigo-800 rounded flex items-center justify-center hover:bg-orange-500 transition">📷</a>
                        <a href="#" class="w-8 h-8 bg-indigo-800 rounded flex items-center justify-center hover:bg-orange-500 transition">▶</a>
                    </div>
                </div>

                <div>
                    <h3 class="font-bold text-lg mb-4 border-b border-indigo-700 pb-2 inline-block">Kurumsal</h3>
                    <ul class="space-y-2 text-indigo-200 text-sm">
                        <li><a href="#" class="hover:text-orange-400 transition">→ Hakkımızda</a></li>
                        <li><a href="#" class="hover:text-orange-400 transition">→ Reklam & Sponsorluk</a></li>
                        <li><a href="#" class="hover:text-orange-400 transition">→ Kullanım Şartları</a></li>
                        <li><a href="#" class="hover:text-orange-400 transition">→ İletişim</a></li>
                    </ul>
                </div>

                <div>
                    <h3 class="font-bold text-lg mb-4 border-b border-indigo-700 pb-2 inline-block">İletişim</h3>
                    <ul class="space-y-3 text-indigo-200 text-sm">
                        <li class="flex items-start gap-2">
                            <span>📍</span> <span>İstanbul, Türkiye</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <span>📧</span> <span>info@volleymarkt.com</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <span>📞</span> <span>+90 (212) 555 00 00</span>
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="border-t border-indigo-800 mt-12 pt-8 text-center text-xs text-indigo-400">
                &copy; 2025 VolleyMarkt Turkey. Tüm hakları saklıdır. Veriler TVF ve Wikipedia kaynaklıdır.
            </div>
        </div>
    </footer>
"""

# --- YENİ INDEX SAYFASI ---
INDEX_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>VolleyMarkt - Voleybolun Kalbi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-gray-50 flex flex-col min-h-screen">
    {NAVBAR_HTML}

    <main class="flex-grow container mx-auto px-4">
        {{% if messages %}}
        <div class="mb-6">
            {{% for message in messages %}}
            <div class="p-4 rounded-lg bg-green-100 text-green-800 border-l-4 border-green-500 shadow-sm flex items-center gap-2">
                <span>✅</span> {{{{ message }}}}
            </div>
            {{% endfor %}}
        </div>
        {{% endif %}}

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-10">
            <h2 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <span class="bg-orange-100 text-orange-600 p-1.5 rounded">🔍</span> Detaylı Oyuncu Arama
            </h2>
            <form method="GET" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="col-span-1 md:col-span-4">
                    <input type="text" name="isim" value="{{{{ secili_isim|default:'' }}}}" placeholder="Oyuncu adı ara..." class="w-full border border-gray-200 p-2.5 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none transition">
                </div>
                <div>
                    <select name="kulup" class="w-full border border-gray-200 p-2.5 rounded-lg bg-white focus:ring-2 focus:ring-orange-500 outline-none">
                        <option value="">Tüm Kulüpler</option>
                        {{% for kulup in kulupler %}}
                            <option value="{{{{ kulup.id }}}}" {{% if kulup.id == secili_kulup %}}selected{{% endif %}}>{{{{ kulup.isim }}}}</option>
                        {{% endfor %}}
                    </select>
                </div>
                <div>
                    <select name="mevki" class="w-full border border-gray-200 p-2.5 rounded-lg bg-white focus:ring-2 focus:ring-orange-500 outline-none">
                        <option value="">Tüm Mevkiler</option>
                        {{% for kod, ad in mevkiler %}}
                            <option value="{{{{ kod }}}}" {{% if kod == secili_mevki %}}selected{{% endif %}}>{{{{ ad }}}}</option>
                        {{% endfor %}}
                    </select>
                </div>
                <div class="flex gap-2">
                    <input type="number" name="min_boy" value="{{{{ secili_min_boy|default:'' }}}}" placeholder="Min" class="w-1/2 border border-gray-200 p-2.5 rounded-lg">
                    <input type="number" name="max_boy" value="{{{{ secili_max_boy|default:'' }}}}" placeholder="Max" class="w-1/2 border border-gray-200 p-2.5 rounded-lg">
                </div>
                <div class="flex gap-2">
                    <button type="submit" class="bg-indigo-900 text-white px-4 py-2.5 rounded-lg hover:bg-indigo-800 flex-1 font-bold shadow-md transition">Sonuçları Göster</button>
                    <a href="/" class="bg-gray-100 text-gray-500 px-3 py-2.5 rounded-lg hover:bg-gray-200 flex items-center justify-center transition">↺</a>
                </div>
            </form>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="md:col-span-3">
                <div class="flex justify-between items-center mb-6">
                    <h1 class="text-2xl font-bold text-gray-800 border-l-4 border-orange-500 pl-4">Oyuncular</h1>
                    <span class="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">{{{{ sporcular|length }}}} Kayıt</span>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {{% for sporcu in sporcular %}}
                    <a href="{{% url 'sporcu_detay' sporcu.id %}}" class="block bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition duration-300 group overflow-hidden">
                        <div class="h-60 overflow-hidden bg-gray-200 relative">
                            {{% if sporcu.profil_fotografi %}}
                                <img src="{{{{ sporcu.profil_fotografi.url }}}}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-700">
                            {{% else %}}
                                <div class="w-full h-full flex flex-col items-center justify-center text-gray-400 bg-gray-100">
                                    <span class="text-4xl">👤</span>
                                    <span class="text-xs mt-2">Görsel Yok</span>
                                </div>
                            {{% endif %}}
                            
                            <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/90 via-black/60 to-transparent p-4 pt-10">
                                <h2 class="text-white font-bold text-lg leading-tight">{{{{ sporcu.isim }}}}</h2>
                                <p class="text-orange-400 text-xs font-medium uppercase tracking-wider mt-1">{{{{ sporcu.kulup.isim|default:"Kulüpsüz" }}}}</p>
                            </div>
                        </div>
                        <div class="p-4 flex justify-between items-center text-sm border-t border-gray-50 bg-white">
                            <span class="text-gray-600 bg-gray-100 px-2 py-0.5 rounded text-xs font-medium">{{{{ sporcu.get_mevki_display }}}}</span>
                            <span class="font-bold text-indigo-900">{{{{ sporcu.boy }}}} cm</span>
                        </div>
                    </a>
                    {{% empty %}}
                        <div class="col-span-3 text-center py-12">
                            <div class="text-6xl mb-4">🏐</div>
                            <p class="text-gray-500">Aradığınız kriterlere uygun oyuncu bulunamadı.</p>
                        </div>
                    {{% endfor %}}
                </div>
            </div>

            <div class="md:col-span-1 space-y-8">
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-indigo-900 to-indigo-800 text-white p-3 font-bold text-center text-sm uppercase tracking-wide">
                        🏆 Sultanlar Ligi
                    </div>
                    <table class="w-full text-sm text-left text-gray-600">
                        <thead class="text-xs text-gray-500 uppercase bg-gray-50 border-b">
                            <tr>
                                <th class="px-3 py-2">Takım</th>
                                <th class="px-2 py-2 text-center">P</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            {{% for sira in puan_tablosu %}}
                            <tr class="hover:bg-indigo-50 transition">
                                <td class="px-3 py-2.5 font-medium text-gray-800 flex items-center gap-2">
                                    <span class="text-xs text-gray-400 w-4">{{{{ forloop.counter }}}}.</span>
                                    {{{{ sira.kulup.isim }}}}
                                </td>
                                <td class="px-2 py-2.5 text-center font-bold text-indigo-900">{{{{ sira.puan|floatformat:0 }}}}</td>
                            </tr>
                            {{% empty %}}
                                <tr><td colspan="2" class="p-4 text-center text-xs">Veri Yok</td></tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                    <div class="bg-gray-50 p-2 text-center text-xs text-gray-400 border-t">
                        TVF Resmi Verileri
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
                    <h3 class="font-bold text-gray-800 mb-4 border-b pb-2 text-sm uppercase">📅 Fikstür</h3>
                    <div class="space-y-4">
                        {{% for mac in maclar %}}
                        <div class="text-sm border-b border-dashed border-gray-200 pb-3 last:border-0 last:pb-0">
                            <div class="text-xs text-orange-600 font-bold mb-1">{{{{ mac.tarih|date:"d M l - H:i" }}}}</div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700 w-1/3 text-right">{{{{ mac.ev_sahibi.isim }}}}</span>
                                <span class="font-bold bg-indigo-100 text-indigo-900 px-2 py-0.5 rounded mx-1 text-xs">{{{{ mac.skor }}}}</span>
                                <span class="font-medium text-gray-700 w-1/3">{{{{ mac.deplasman.isim }}}}</span>
                            </div>
                        </div>
                        {{% empty %}}
                            <p class="text-xs text-gray-400 text-center">Planlanmış maç yok.</p>
                        {{% endfor %}}
                    </div>
                </div>
            </div>
        </div>
    </main>

    {FOOTER_HTML}
</body>
</html>
"""

# --- YENİ DETAY SAYFASI ---
DETAY_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{{{{ sporcu.isim }}}} - VolleyMarkt</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-gray-100 flex flex-col min-h-screen">
    {NAVBAR_HTML}

    <main class="flex-grow container mx-auto px-4">
        
        <div class="text-sm text-gray-500 mb-4 flex gap-2">
            <a href="/" class="hover:text-orange-500">Anasayfa</a> <span>/</span> 
            <span class="text-gray-800 font-medium">Oyuncu Profili</span>
        </div>

        <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden flex flex-col md:flex-row mb-8">
            <div class="md:w-1/3 bg-gray-200 relative min-h-[400px]">
                {{% if sporcu.profil_fotografi %}}
                    <img src="{{{{ sporcu.profil_fotografi.url }}}}" class="w-full h-full object-cover absolute inset-0">
                {{% else %}}
                    <div class="w-full h-full flex flex-col items-center justify-center text-gray-400">
                        <span class="text-6xl">👤</span>
                    </div>
                {{% endif %}}
                
                {{% if sporcu.piyasa_degeri %}}
                <div class="absolute top-4 left-4 bg-green-600/90 backdrop-blur-sm text-white px-4 py-2 rounded-lg shadow-lg border border-green-500">
                    <div class="text-xs opacity-90 uppercase tracking-wide">Piyasa Değeri</div>
                    <div class="text-xl font-bold">€ {{{{ sporcu.piyasa_degeri }}}}</div>
                </div>
                {{% endif %}}
            </div>

            <div class="p-8 md:w-2/3 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start border-b border-gray-100 pb-6 mb-6">
                        <div>
                            <h1 class="text-4xl font-bold text-gray-900 tracking-tight">{{{{ sporcu.isim }}}}</h1>
                            <div class="flex items-center gap-3 mt-3">
                                <span class="bg-indigo-50 text-indigo-900 px-3 py-1 rounded-full font-bold text-sm border border-indigo-100">
                                    {{{{ sporcu.kulup.isim|default:"Kulüpsüz" }}}}
                                </span>
                                <span class="text-gray-300">|</span>
                                <span class="text-gray-600 font-medium flex items-center gap-1">
                                    🏐 {{{{ sporcu.get_mevki_display }}}}
                                </span>
                            </div>
                        </div>
                        <div class="hidden md:block text-right">
                             <div class="text-6xl opacity-10 font-bold text-indigo-900">#{{{{ sporcu.id }}}}</div>
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-4 mb-8">
                        <div class="bg-gray-50 p-4 rounded-lg text-center border border-gray-100 hover:border-orange-200 transition">
                            <div class="text-3xl font-bold text-indigo-900">{{{{ sporcu.boy }}}}</div>
                            <div class="text-xs text-gray-500 font-bold uppercase mt-1">Boy (cm)</div>
                        </div>
                        <div class="bg-gray-50 p-4 rounded-lg text-center border border-gray-100 hover:border-orange-200 transition">
                            <div class="text-3xl font-bold text-indigo-900">{{{{ sporcu.smac_yuksekligi|default:"-" }}}}</div>
                            <div class="text-xs text-gray-500 font-bold uppercase mt-1">Smaç</div>
                        </div>
                        <div class="bg-gray-50 p-4 rounded-lg text-center border border-gray-100 hover:border-orange-200 transition">
                            <div class="text-3xl font-bold text-indigo-900">{{{{ sporcu.blok_yuksekligi|default:"-" }}}}</div>
                            <div class="text-xs text-gray-500 font-bold uppercase mt-1">Blok</div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4 text-sm mb-6">
                        <div>
                            <span class="block text-gray-400 text-xs uppercase mb-1">Doğum Tarihi</span> 
                            <span class="font-medium text-gray-900">{{{{ sporcu.dogum_tarihi|default:"-" }}}}</span>
                        </div>
                        <div>
                            <span class="block text-gray-400 text-xs uppercase mb-1">Menajer</span> 
                            {{% if sporcu.menajer %}}
                                <span class="font-medium text-indigo-600">{{{{ sporcu.menajer.isim }}}}</span>
                            {{% else %}}
                                <span class="text-gray-400 italic">Temsilci Yok</span>
                            {{% endif %}}
                        </div>
                    </div>
                </div>

                {{% if sporcu.video_linki %}}
                <div class="mt-4">
                    <a href="{{{{ sporcu.video_linki }}}}" target="_blank" class="flex items-center justify-center gap-3 w-full bg-red-600 text-white py-3.5 rounded-lg hover:bg-red-700 transition font-bold shadow-md group">
                        <span class="bg-white text-red-600 rounded-full w-6 h-6 flex items-center justify-center text-xs group-hover:scale-110 transition">▶</span> 
                        Tanıtım Videosunu İzle
                    </a>
                </div>
                {{% endif %}}
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <h3 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                        <span class="bg-indigo-100 p-1 rounded text-indigo-600">🔄</span> Transfer Geçmişi
                    </h3>
                    
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm text-gray-600">
                            <thead class="bg-gray-50 text-gray-500 uppercase text-xs font-bold border-b">
                                <tr>
                                    <th class="p-3">Sezon</th>
                                    <th class="p-3">Eski</th>
                                    <th class="p-3">Yeni</th>
                                    <th class="p-3">Durum</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-100">
                                {{% for transfer in sporcu.transferler.all %}}
                                <tr class="hover:bg-gray-50 transition">
                                    <td class="p-3 font-bold text-indigo-900">{{{{ transfer.sezon }}}}</td>
                                    <td class="p-3">
                                        {{{{ transfer.eski_kulup.isim|default:"-" }}}}
                                    </td>
                                    <td class="p-3 font-medium text-gray-900 flex items-center gap-2">
                                        {{{{ transfer.yeni_kulup.isim|default:"-" }}}}
                                        {{% if transfer.yeni_kulup == sporcu.kulup %}}
                                            <span class="text-xs bg-green-100 text-green-700 px-1.5 rounded">Aktif</span>
                                        {{% endif %}}
                                    </td>
                                    <td class="p-3 text-xs">
                                        <span class="px-2 py-1 rounded bg-gray-100 border border-gray-200">{{{{ transfer.tip }}}}</span>
                                    </td>
                                </tr>
                                {{% empty %}}
                                <tr>
                                    <td colspan="4" class="p-8 text-center text-gray-400">
                                        Kariyer verisi henüz girilmemiş.
                                    </td>
                                </tr>
                                {{% endfor %}}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-1">
                <div class="bg-gradient-to-br from-indigo-900 to-indigo-800 text-white rounded-xl shadow-lg p-8 text-center relative overflow-hidden">
                    <div class="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 bg-white opacity-5 rounded-full"></div>
                    
                    <h3 class="font-bold text-lg mb-2 z-10 relative">Sponsorluk</h3>
                    <p class="text-indigo-200 text-sm mb-6 z-10 relative">Bu oyuncu ile ilgileniyor musunuz? İletişime geçin.</p>
                    <button class="bg-orange-500 text-white w-full py-2 rounded font-bold hover:bg-orange-600 transition shadow-md z-10 relative">
                        Menajerle İletişim
                    </button>
                </div>
            </div>
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
    print("🚀 Tasarım Güncellemesi Yükleniyor...\n")
    write_file('core/templates/index.html', INDEX_HTML)
    write_file('core/templates/detay.html', DETAY_HTML)
    print("\n🎉 İŞLEM TAMAM! Sunucuyu kapatıp açmana gerek yok, sayfayı yenilemen yeterli.")

if __name__ == '__main__':
    main()