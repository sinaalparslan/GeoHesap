    #GEOHESAP
Giriş

Bu çalışma ile Geomatik alanında önemli yer tutan ve yersel ölçme tekniklerinin hesaplarını gerçekleştiren bir yazılım paketinin geliştirilmesi hedeflenmiştir. Yazılım paketindeki her bir uygulama güncel BÖHHBÜY ile
belirlenen mevzuata uygun olarak Python programlama dili ile yazılmıştır.

------ 1. Modüller ------

Yazılım paketimizi oluşturan modüller ve kabiliyetleri
şunlardır:
Bağlı Poligon Hesabı: Hesap, poligon hattını çizdirme, noktaları haritada gösterme ve Excel dokümanı oluşturma. 
Kapalı Poligon Hesabı: Hesap, poligon hattını çizdirme,noktaları haritada gösterme ve Excel dokümanı oluşturma.
Açık Nivelman Hesabı: Hesap, Excel dokümanı oluşturma.
Dayalı (Bağlı) Nivelman Hesabı: Hesap, Excel dokümanı oluşturma.
WGS84-ED50 Datum Dönüşümü: Noktaları haritada gösterme ve Excel dokümanı oluşturma
ED50-WGS84 Datum Dönüşümü: Noktaları haritada gösterme ve Excel dokümanı oluşturma
Nokta Gösterme (Enlem, Boylam): Noktaları haritada gösterme ve Excel dokümanı oluşturma
Nokta Gösterme (Y, X; WGS84): Noktaları haritada gösterme ve Excel dokümanı oluşturma

------ 2. Yararlanılan Kütüphaneler ------

tkinter: temel ara yüz ve işlemleri için kullanıldı.
math: matematiksel işlemler için kullanıldı.
xlsxwriter: Excel dosyasının okunması/yazılması için kullanıldı.
os: işletim sisteminde işlem yapabilmek için kullanıldı.
matplotlib: 2 boyutlu hat çizimi için kullanıldı.
folium: noktaları haritada gösterebilmek için kullanıldı.
pyproj: koordinat projeksiyonları arasında dönüşüm yapmak için kullanıldı.
re: girdi değerlerinin kontrolü için kullanıldı.

------ 3. Sonuçlar ------

Geomatik Mühendisleri ve aday öğrencilerin kullanabilmesi amacıyla poligon hesabı, yükseklik ölçmeleri, datum ve koordinat dönüşümü gibi temel işlemler için gerekli hesapları yapabilen, tablo, grafik ve WEB harita çıktısı
verebilen Python tabanlı bir yazılım geliştirilmiştir.
Geliştirilen modüller daha önce Beytepe Yerleşkesi sınırları içinde gerçekleştirilen arazi çalışmalarının verileri ile test edilerek elde edilen sonuçların uyumlu olduğu görülmüştür.