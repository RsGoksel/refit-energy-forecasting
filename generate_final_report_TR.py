"""
Generate the comprehensive Final Project Report (DOCX) and convert to PDF.

Clean style:
 - Calibri throughout
 - 1.3 line spacing
 - No em-dash, no superscript R-squared, no et al., no subscript digits
 - "and others" instead of "et al."

Rich content:
 - Cover page
 - Abstract
 - Section structure: Intro -> Data -> Methodology -> Results -> Discussion -> Conclusion
 - All 6 EDA/result figures + 4 custom diagrams
 - Results tables
 - References
"""
import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "results")
OUTPUT_DOCX = os.path.join(BASE, "EBT629E_Final_Project_Report_TR.docx")
OUTPUT_PDF = os.path.join(BASE, "EBT629E_Final_Project_Report_TR.pdf")

doc = Document()

# Page setup
for section in doc.sections:
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.4)
    section.right_margin = Cm(2.4)

# Default style
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.3
style.paragraph_format.space_after = Pt(5)

NAVY = RGBColor(0, 51, 102)
GREY = RGBColor(80, 80, 80)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def add_heading(text, level=1, color=NAVY):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = color
        run.font.name = 'Calibri'
    return h


def add_para(text, lead_bold=None, justify=True):
    p = doc.add_paragraph()
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if lead_bold:
        r = p.add_run(lead_bold)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(11)
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(11)
    return p


def add_figure(filename, caption, width=Inches(6.0)):
    path = os.path.join(RESULTS, filename)
    if not os.path.exists(path):
        doc.add_paragraph(f"[Figure missing: {filename}]")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run()
    run.add_picture(path, width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run(caption)
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = 'Calibri'


def add_bullet(text):
    p = doc.add_paragraph(text, style='List Bullet')
    for r in p.runs:
        r.font.name = 'Calibri'
        r.font.size = Pt(11)


def add_table_caption(text):
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(2)
    r = cap.add_run(text)
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = 'Calibri'


# ============================================================
# COVER PAGE
# ============================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Istanbul Teknik Universitesi")
r.font.size = Pt(14)
r.font.name = 'Calibri'
r.font.color.rgb = GREY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("EBT 629E, Yapay Zeka")
r.font.size = Pt(14)
r.font.name = 'Calibri'
r.font.color.rgb = GREY

doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Donem Sonu Proje Raporu")
r.font.size = Pt(22)
r.bold = True
r.font.name = 'Calibri'
r.font.color.rgb = NAVY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Zaman Serisi Modelleri ile\nHane Halki Enerji Tuketimi Tahmini")
r.font.size = Pt(16)
r.bold = True
r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("REFIT Veri Seti Uzerinde ARIMA, LSTM ve FB-Prophet Modellerinin Karsilastirmali Analizi")
r.font.size = Pt(12)
r.italic = True
r.font.name = 'Calibri'
r.font.color.rgb = GREY

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Grup Uyeleri")
r.font.size = Pt(12)
r.bold = True
r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(
    "Nurullah Yıldırım (301252004)\n"
    "Kadir Göksel Gündüz (301241077)\n"
    "Furkan Çınar (301212001)"
)
r.font.size = Pt(12)
r.font.name = 'Calibri'

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Mayis 2026")
r.font.size = Pt(12)
r.font.name = 'Calibri'
r.font.color.rgb = GREY

doc.add_page_break()

# ============================================================
# ABSTRACT
# ============================================================
add_heading("Ozet", level=1)
add_para(
    "Bu rapor, REFIT Akilli Ev veri setinden hane halki enerji tuketimine uygulanan dort zaman "
    "serisi tahmin yaklasiminin karsilastirmali bir incelemesini sunmaktadir. Uc Birlesik Krallik "
    "hanesinden (Ev 1, Ev 2 ve Ev 5) 22 aylik 8 saniye cozunurluklu olcumleri kullaniyoruz; "
    "verileri gunluk ortalama gucu uretecek sekilde yeniden orneklenir, ardindan 7 gunluk hareketli "
    "ortalama ile yumusatilir ve her seri yuzde 80 egitim, yuzde 20 test olacak sekilde zaman "
    "sirasinda bolunur. Uc aday modelin (ARIMA, Long Short-Term Memory (LSTM) ve FB-Prophet) yani "
    "sira saglik kontrolu olarak persistence temel modeli (y_hat[t] = y[t-1]) ekledik. ARIMA modeli "
    "ADF duraganlik testi ve AIC izgara aramasi ile ayarlanir, ardindan tek adim onde yuvarlanan "
    "tahmin protokolu altinda calistirilir; LSTM uc katmanli yiginlanmis RNN mimarisi kullanir; "
    "Prophet haftalik ve yillik mevsimsellik bilesenleriyle tek seferlik cok adim modunda calisir. "
    "Ev 2 de ARIMA(2, 1, 2) R2 = 0.876 ve RMSE = 48.7 W e ulasir, ancak Diebold-Mariano testi "
    "persistence temel modeli (R2 = 0.873) uzerindeki marjinin istatistiksel olarak anlamli "
    "olmadigini gosterir (p = 0.665). LSTM (R2 = 0.748) ve Prophet (R2 = 0.015) persistence e "
    "anlamli olarak kaybeder (her ikisinde de p < 0.001). Ayni oruntu Ev 1 ve Ev 5 te de tekrarlanir: "
    "ARIMA dar bir farkla kazanir, ancak persistence uzerine cok az sey ekler; LSTM ve Prophet ise "
    "tutarli olarak temel modelin altinda kalir. Baslica ders, yumusatilmis gunluk konut tuketiminin "
    "gecikme-1 otokorelasyonu tarafindan domine edildigi; bu nedenle tek satirlik bir kuralin "
    "neredeyse tum tahmin edilebilir yapiyi yakaladigidir. Daha agir makineler ancak daha guclu "
    "disasal girdiler veya daha ince granulariteli hedefler bu otokorelasyonu kirdiginda dogrulanir. "
    "Sabit rastgele tohum kullanilan tum kod tabani bu rapora eslik etmektedir."
)

doc.add_page_break()

# ============================================================
# 1. INTRODUCTION
# ============================================================
add_heading("1. Giris", level=1)

add_heading("1.1 Genel Bilgi ve Motivasyon", level=2)
add_para(
    "Hane halki elektrik tuketimi, modern enerji sistemlerinin merkezindeki birkac sorunu ayni anda etkilemektedir. Sebeke isletmecisi acisindan kisa ufuklu dogrulukla yapilan tahminler, yenilenebilir uretiminin dengelenmesi, yedek kapasite planlamasi ve kisitlama miktarinin azaltilmasi icin gereklidir. Tuketici acisindan ise bu tahminler talep yaniti programlarina katilimi, cihazlarin akilli sekilde programlanmasini, cati ustu PV ve batarya sistemleriyle entegrasyonun iyilestirilmesini kolaylastirir. Avrupa genelinde akilli sayaclarin hizla yayilmasi ve makine ogrenmesi yontemlerinin olgunlasmasi, sorunun artik trafo merkezi yerine tekil hane duzeyinde calisilmasini mumkun kilmaktadir."
)
add_para(
    "Konut tuketiminin tahmini, toplulastirilmis talebi tahmin etmekten yapisal olarak daha zordur. Tek bir hane ani anahtarlama olaylari (su isiticisi, firin, camasir makinesi), kullaniciya ozgu programlar ve hava ile tatil etkilesimi gosteren mevsimsellik icerir. Cok sayida haneyi ortalayarak bu gurultunun buyuk bolumu sonuc sinyalinden silinir; bu nedenle sebeke duzeyinde dusuk MAPE raporlanirken hane duzeyinde tahmin tamamen basarisiz olabilir."
)

add_heading("1.2 Proje Hedefleri", level=2)
add_para(
    "Bu projenin sordugu soru hem odakli hem de uygulamaya yoneliktir: yaygin uc zaman serisi modeli olan ARIMA, LSTM ve FB-Prophet arasinda, tek bir hanenin gunluk enerji tuketimini tahmin etmek icin hangisi daha uygundur ve bunun ardindaki gerekceler nelerdir? Somut olarak proje dort hedef pesinden gider."
)
add_bullet("Ham 8 saniye REFIT okumalarindan model ciktilarina kadar uzanan tekrar uretilebilir bir boru hatti kurmak.")
add_bullet("ARIMA, LSTM ve FB-Prophet modellerini ayni veri bolme protokolu altinda tek bir test ortaminda karsilastirmak.")
add_bullet("Model performansini MSE, RMSE, MAE ve R2 metrikleriyle nicel olarak olcmek.")
add_bullet("Her modelin nerede kazanip nerede kaybettigini incelemek ve nihai tasarima goturen iterasyonlari belgelemek.")

add_heading("1.3 Rapor Yapisi", level=2)
add_para(
    "Bolum 2, REFIT veri setini ve secilen haneyi tanitir. Bolum 3, on isleme boru hatti ve uc modelleme yaklasimini detaylandirir; literaturdeki cok cesitli karsilastirmalardan ayrismamizi saglayan yuvarlanan tahmin protokolu de burada anlatilir. Bolum 4 kesifsel veri analizini sunar. Bolum 5 sayisal sonuclari ve gorsel karsilastirmalari sunar. Bolum 6 bulgulari, calismanin sinirlamalarini ve gecerlilik tehditlerini tartisir. Bolum 7 sonuc ve ileride yapilabilecek calismalarla kapanir."
)

# ============================================================
# 2. DATASET
# ============================================================
add_heading("2. Veri Seti: REFIT Akilli Ev Elektrik Yuku Olcumleri", level=1)

add_heading("2.1 Genel Bakis", level=2)
add_para(
    "REFIT (Personalised Retrofit Decision Support Tools for UK Homes), Ekim 2013 ile Haziran 2015 arasinda Birlesik Krallik Loughborough bolgesinde toplanan boylamsal bir veri setidir. Veriler Strathclyde, Loughborough ve East Anglia Universiteleri ortakliginda EPSRC finansmaniyla uretilmis ve Creative Commons Attribution 4.0 International lisansi altinda yayinlanmistir. Yirmi hane (Ev 1 ile Ev 21 arasinda, Ev 14 atlanarak) tum hane akimi olcen bir akim klempi ve dokuz adet bireysel cihaz olcumleyici ile donatilmistir. Aktif guc, yaklasik alti ile sekiz saniyede bir Watt cinsinden orneklenmis ve tum haneler toplaminda yaklasik 1,19 milyar gozlemden olusan bir koleksiyon olusturmustur (Murray, Stankovic ve Stankovic, 2017)."
)

add_heading("2.2 Secilen Hane: Ev 2", level=2)
add_para(
    "Bu projenin test ortami olarak Ev 2 secilmistir. CSV dosyasi diskte 299 MB yer kaplar ve 22 aylik bir surede toplanan 5.733.526 zaman damgali okuma icerir. Izlenen cihazlar Buzdolabi-Dondurucu, Camasir Makinesi, Bulasik Makinesi, Televizyon, Mikrodalga, Tost Makinesi, Hi-Fi, Su Isiticisi ve Firin Aspiratorudur. Ev 2; belgelenmis cihaz degisikligi olmamasi, cati ustu PV girisimi bulunmamasi ve tipik bir Birlesik Krallik hanesinin cihaz karisimini temsil etmesi nedeniyle secilmistir."
)

# Correlation heatmap
add_figure("correlation_heatmap.png",
           "Sekil 1. Ev 2 hanesinde toplam guc kanali ile dokuz bireysel cihaz olcumleyici "
           "arasindaki Pearson korelasyonu.",
           width=Inches(5.5))

add_heading("2.3 Veri Kalitesi ve Temizleme", level=2)
add_para(
    "REFIT surumu, kisa bosluklarda ileri doldurma uygular ve iki dakikadan uzun bosluklari sifirlar. Cihaz kanallarinda 4000 W uzerindeki okumalar (sensor menzilinin disinda) orijinal bakimcilar tarafindan zaten kaldirilmistir. Bizim ek temizleme adimlarimiz, negatif toplam okumalari (klemp polarite hatalarindan kaynaklanan) kaldirir ve degerlerin ust yuzde 1 lik dilimini aykiri olarak budar. Bu adimlardan sonra toplam seri sureklidir ve yeniden ornekleme icin hazirdir."
)

doc.add_page_break()

# ============================================================
# 3. METHODOLOGY
# ============================================================
add_heading("3. Yontem", level=1)

add_figure("pipeline_diagram.png",
           "Sekil 2. Uctan uca makine ogrenmesi boru hatti. Ham 8 saniye REFIT verisi aykiri "
           "deger temizleme, gunluk yeniden ornekleme ve 7 gunluk yumusatma adimlarindan gecer, "
           "ardindan uc rakip modeli besler. Modellerin tahminleri ayrilmis test seti uzerinde "
           "degerlendirilir.",
           width=Inches(6.3))

add_heading("3.1 Veri On Isleme", level=2)
add_para(
    "Bes on isleme adimi ham sinyali modellemeye hazirlar. Once, zaman damgasi sutunu pandas DatetimeIndex e cevrilir. Ikinci olarak, bellek tasarrufu icin Unix epoch sutunu birakilir. Ucuncu olarak, aykiri deger filtreleme negatif degerleri ve 99 uncu persentilin uzerindeki girdileri kaldirir. Dordunculuk olarak, temizlenmis seri gunluk ortalamaya yeniden orneklenir; bu islem 5,7 milyon satiri yaklasik 630 gunluk gozleme indirir ve cihaz duzeyindeki anahtarlama gurultusunun cogunu temizler. Besinci olarak, ortalanmis 7 gunluk hareketli ortalama, hafta-ici degiskenligi bastirirken haftalik ve mevsimsel donguleri korur."
)
add_para(
    "Hareketli ortalamanin NaN urettigi eksik gunler, veri seti zaman sirasiyla bolunmeden once ileri ve geri doldurma ile tamamlanir. Bolme ilk yuzde 80 i egitim, son yuzde 20 yi test olarak ayirir; bu, mevsimsel kayma iceren zaman serileri icin standart protokoldur."
)

add_heading("3.2 ARIMA Modeli", level=2)
add_para(
    "ARIMA(p, d, q), istatistiksel zaman serisi tahmininin temel modelidir. Box-Jenkins prosedurunu izledik. Augmented Dickey-Fuller testi egitim setinde 0.94 p-degerine sahip olarak duragansizliga isaret etti; bu nedenle birinci dereceden farklilastirma (d = 1) uygulandi. Ardindan p in [0, 2] ve q in [0, 2] uzerinde izgara aramasi yapilarak en dusuk AIC degerine sahip yapilanma secildi: ARIMA(2, 1, 2), AIC = 4547.63."
)
add_para(
    "Nihai ARIMA modeli yuvarlanan tek-adim-onde tahmin protokolunde calistirilir: her test gununde model, o ana kadar gozlenen tum veriler uzerinde yeniden uydurulur ve sadece bir sonraki gun icin tahmin yapar. Bu, bir operatorun modelden uretimde nasil yararlanacagini birebir yansitir; cunku dunun gercek olcumu bugunun tahmininden once her zaman elimizdedir.",
    lead_bold="Yuvarlanan tahmin protokolu. "
)

add_heading("3.3 LSTM Modeli", level=2)
add_para(
    "LSTM modeli, sirasiyla 128, 64 ve 32 hucreli uc katmanli yiginlanmis tekrarlayan agdir; katmanlar arasinda 0.2 oraninda dropout, en uste ise 16 hucreli ReLU yogun katman ve ardindan dogrusal cikis bulunur. Girdiler, 14 gunluk kayar pencerelere uygulanan Min-Max olcekli guc degerleridir. Egitimde Adam iyilestirici, MSE kayip fonksiyonu, 16 yigin buyuklugu ve 100 epoch kullanildi; 5 epoch boyunca dogrulama kaybinda iyilesme olmazsa egitim erken durdurulur. Sabit rastgele tohum (42), calismanin makineler arasi tekrar uretilebilir olmasini saglar."
)

add_figure("lstm_architecture.png",
           "Sekil 3. Bu projede kullanilan LSTM aginin mimarisi, hiperparametreleri ve egitim "
           "yapilandirmasi.",
           width=Inches(5.5))

add_heading("3.4 FB-Prophet Modeli", level=2)
add_para(
    "FB-Prophet, bir seriyi trend, mevsimsellik ve tatil etkilerine ayristirir ve her bileseni ek (veya carpan) sinyal olarak uydurur. Haftalik ve yillik mevsimselligi etkinlestirdik, gunluk mevsimselligi devre disi biraktik (gunluk yeniden ornekleme sonrasinda anlamsizdir) ve carpan modu kullandik; cunku mevsimsel salinim genligi genel duzeyle olceklenir. Degisim noktasi onsel olcegi varsayilan 0.05 te birakildi."
)
add_para(
    "Onemli olan, Prophet in tek seferlik cok-adim modunda calistirilmasidir: yani test ufkunun tamamini (122 gun) bir kerede tahmin eder ve test seti gercek degerlerine erisemez. Bu, Prophet in pratikteki kanonik kullanimidir, ancak ARIMA ve LSTM in yuvarlanan kurulumlarina kiyasla onu yapisal olarak dezavantajli kilar. Tartismada bu noktaya geri donecegiz.",
    lead_bold="Cok-adim protokolu. "
)

add_figure("rolling_forecast.png",
           "Sekil 4. Iki tahmin protokolunun karsilastirmasi. ARIMA ve LSTM her tahmin oncesinde "
           "bir onceki gunun gercek degerini gorur; Prophet ise yalnizca egitim verisine "
           "dayanarak test ufkunun tamamina taahhut eder.",
           width=Inches(6.3))

add_heading("3.5 Persistence Temel Modeli", level=2)
add_para(
    "Karmasik bir modelin gercekten faydali oldugunu iddia etmeden once, en basit alternatifi "
    "yenebildigini gostermemiz gerekir. Bu nedenle, bir sonraki gunun bir onceki gunun gercek "
    "degerine esit oldugu tahminini (y_hat[t] = y[t-1]) uretmesi icin persistence (yapiskanlik) "
    "temel modeli ekledik. Bu, zaman serisi tahmininde kanonik bir saglik kontrolu modelidir. "
    "Persistence'i yenemeyen herhangi bir model, tek satirlik bir kuralin yakaladigindan fazla "
    "bir sey ogrenmemis demektir. Persistence, ARIMA ve LSTM ile ayni yuvarlanan protokol "
    "altinda calisir: bir sonraki gunu tahmin ederken bir onceki gunun gercek degeri her zaman "
    "elimizdedir."
)

add_heading("3.6 Degerlendirme Metrikleri", level=2)
add_para(
    "Tahmin dogrulugu birbirini tamamlayan dort metrikle olculur. Ortalama Karesel Hata (MSE) ve Karekok Ortalama Karesel Hata (RMSE) buyuk hatalari agir bicimde cezalandirir; RMSE ozgun birim olan Watt cinsinden raporlanir. Ortalama Mutlak Hata (MAE) aykiri degerlere daha dayaniklidir ve yine Watt cinsindendir. Belirleme katsayisi (R2), aciklanan varyansin birimsiz olcumudur; 1 mukemmel tahmini, ortalama temel modelinin altinda kalan modeller icin negatif degerleri ifade eder."
)

add_heading("3.7 Diebold-Mariano Testi ile Istatistiksel Anlamlilik", level=2)
add_para(
    "RMSE veya R2 nin noktasal degerleri, bir modelin digerinden gercekten daha iyi olup olmadigini "
    "gizleyebilir. Bu nedenle Harvey-Leybourne-Newbold kucuk orneklem duzeltmesiyle Diebold-Mariano "
    "(DM) esit tahmin dogrulugu testini kullaniyoruz. Bos hipotez, iki rakip modelin beklenen "
    "karesel hata kaybinin esit oldugudur; negatif DM istatistigi birinci modeli, pozitif olan "
    "ikinci modeli destekler. Ilgilenilen tum ikili karsilastirmalar icin iki tarafli p-degerlerini "
    "raporluyoruz."
)

doc.add_page_break()

# ============================================================
# 4. EXPLORATORY DATA ANALYSIS
# ============================================================
add_heading("4. Kesifsel Veri Analizi", level=1)

add_para(
    "Modellemeden once, temizlenmis toplam sinyali zaman yapisini karakterize etmek icin inceledik. Sekil 5 teki dort panel bu analizi ozetler."
)

add_figure("data_analysis.png",
           "Sekil 5. Ev 2 nin kesifsel analizi. Sol ust: 22 ay boyunca gunluk ortalama guc. "
           "Sag ust: ham 8 saniye verisi uzerinden hesaplanan saatlik profil (16:00 ile 20:00 "
           "arasinda yemek pisirme ve aydinlatmaya bagli zirve goze carpiyor). Sol alt: hafta "
           "gunlerine gore ortalama gunluk guc (hafta sonlari daha yuksek). Sag alt: gunluk "
           "gucun dagilimi.",
           width=Inches(6.2))

add_para(
    "Uc bulgu one cikti. Birincisi, gunluk seri belirgin bir mevsimsel dongu sergiliyor: kis tuketimi yaza gore belirgin sekilde yuksek; bu, elektrikli isitma kullanimiyla uyumlu. Ikincisi, gunluk toplulastirmanin orneklemi cokertmemesi icin ham veriden hesaplanan saatlik profil, Birlesik Krallik hanelerine ozgu klasik iki tepeli sekli gosteriyor: kucuk bir sabah tepesi ve 16:00 ile 20:00 arasinda belirgin bir aksam tepesi. Ucuncusu, hafta-icine kiyasla hafta sonu tuketiminin yaklasik yuzde 15 daha yuksek olmasi, gun icindeki dolu sure uzunluguyla orustugu konutu yansitiyor."
)

# ============================================================
# 5. RESULTS
# ============================================================
add_heading("5. Sonuclar", level=1)

add_heading("5.1 Nihai Performans Karsilastirmasi", level=2)
add_para(
    "Tablo 1, Ev 2 uzerinde persistence temel modeli ile uc adayin test seti metriklerini "
    "raporlar. Bashlik sonuc: ARIMA(2, 1, 2) R2 = 0.876 ile kazanan, ancak onemsiz persistence "
    "temel modelini (R2 = 0.873) yenmesi ucuncu ondalik basamakta. LSTM (R2 = 0.748) ve "
    "FB-Prophet (R2 = 0.015) ikisi de persistence in altinda kalir. Sonucu, Bolum 5.5 te "
    "Diebold-Mariano testi ile ayrintili olarak inceleyecegiz, ama sezgisel cikarim su: gunluk "
    "konut enerjisindeki gecikme-1 otokorelasyonu butun isi yapiyor; ARIMA bunu temiz bicimde "
    "yakalarken, LSTM ve Prophet bu yapiyi kuramiyor."
)

add_table_caption("Tablo 1. Ev 2 gunluk tahminleri icin persistence temel modeli (y_hat[t] = "
                  "y[t-1]) dahil dort yaklasimin test seti performansi.")

table = doc.add_table(rows=5, cols=5, style='Light Grid Accent 1')
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Model', 'MSE', 'RMSE (W)', 'MAE (W)', 'R2']
data = [
    ['Persistence',    '2,426.76', '49.26', '33.51', '0.873'],
    ['ARIMA(2,1,2)',   '2,370.01', '48.68', '32.75', '0.876'],
    ['LSTM (3-layer)', '4,821.35', '69.44', '52.25', '0.748'],
    ['FB-Prophet',     '18,851.52', '137.30', '111.70', '0.015'],
]
for i, h in enumerate(headers):
    c = table.rows[0].cells[i]
    c.text = h
    for p in c.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(10)
            r.font.name = 'Calibri'
for r_idx, row in enumerate(data):
    for c_idx, v in enumerate(row):
        c = table.rows[r_idx + 1].cells[c_idx]
        c.text = v
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(10)
                r.font.name = 'Calibri'

doc.add_paragraph()

add_figure("metrics_comparison.png",
           "Sekil 6. Uc model arasinda dort degerlendirme metriginin yan-yana karsilastirmasi. "
           "MSE, RMSE ve MAE icin dusuk olan iyi, R2 icin yuksek olan iyi.",
           width=Inches(6.3))

add_heading("5.2 Tahmin Edilen ile Gercek Seri Karsilastirmasi", level=2)
add_para(
    "Sekil 7, her modelin tahminlerini ayrilan test degerleriyle birlikte cizer. ARIMA panelinde yuvarlanan yeniden uydurma sayesinde model en son gozlenen degere sabitlendiginden gercek seri yakindan takip edilir. LSTM paneli trendi genel anlamda yakalar, ancak tepe ve diplerin keskinligini yumusatir. Prophet paneli aslinda parcali dogrusal bir taban cizgisi artiri mevsimsellik uretir; bu, ortalama olarak mantikli kalsa da gercek verideki keskin hareketleri izlemekte basarisiz olur."
)

add_figure("model_comparison.png",
           "Sekil 7. ARIMA, LSTM ve FB-Prophet icin 122 gunluk test penceresi boyunca gercek "
           "ile tahmin edilen gunluk ortalama guc kiyaslamasi.",
           width=Inches(6.3))

add_heading("5.3 Egitim Tanilari", level=2)
add_para(
    "Sekil 8 deki LSTM egitim kaybi egrisi, ilk hizli yakinsamayi ve yaklasik 12 epoch sonra platonun olustugunu gosterir; bu noktada erken durdurma tetiklenir. Dogrulama kaybi egitim kaybini yakindan izler; bu, ana sorunun asiri uyum olmadigini, modelin yumusatilmis gunluk sinyalden cikarabilecegi sinira ulastigini gosterir."
)

add_figure("lstm_training_history.png",
           "Sekil 8. LSTM egitim ve dogrulama MSE kaybinin epoch lara gore degisimi.",
           width=Inches(5.0))

add_para(
    "Sekil 9 daki Prophet ayristirmasi belirgin bir yillik trendi (en yuksek tuketim kisin, en dusuk tuketim yazin) ve orta seviyede haftalik dongu sergiler. Bu bilesenler mantikli olup kesifsel analizle ortusur, ancak genel uyum kisa ufuklu hareketler yerine uzun ufuklu trendin etkisi altinda kalir."
)

add_figure("prophet_components.png",
           "Sekil 9. Ev 2 nin egitim bolumune uydurulmus FB-Prophet ayristirmasinda altta yatan "
           "trend, haftalik mevsimsellik ve yillik mevsimsellik bilesenleri.",
           width=Inches(5.5))

add_heading("5.4 Gelistirme Iterasyonlari", level=2)
add_para(
    "Tablo 1 deki nihai sonuclar ilk denemede elde edilmedi. En iyi modelin R2 sini negatif bolgeden 0.876 ya tasiyan tasarim kararlarini belgeledik. Sekil 10 uc iterasyonu ozetler."
)

add_figure("iteration_timeline.png",
           "Sekil 10. Tasarimin uc iterasyonu ve bunlarin test R2 sine etkisi. En cok fark "
           "yaratan degisiklik, tek seferlik cok-adimli ARIMA tahmininden yuvarlanan "
           "tek-adim-onde protokole gecis oldu.",
           width=Inches(6.3))

doc.add_page_break()

# ============================================================
# 5.5 STATISTICAL SIGNIFICANCE (TR)
# ============================================================
add_heading("5.5 Istatistiksel Anlamlilik: Diebold-Mariano Testi", level=2)
add_para(
    "Ev 2 uzerinde yapilan ikili Diebold-Mariano testleri Tablo 2 deki sonuclari verir. "
    "Uc bulgu one cikiyor. Birincisi, ARIMA nin Persistence uzerindeki gozle gorulen ustunlugu "
    "geleneksel hicbir seviyede istatistiksel olarak anlamli degil (p = 0.665). Iki model bu test "
    "setinde pratik olarak ayirt edilemeyen tahminler uretiyor. Ikincisi, LSTM ve Prophet "
    "Persistence den anlamli sekilde daha kotu (her ikisinde de p < 0.001): model karmasikligini "
    "artirmak burada dogrulugu aktif olarak zedeliyor. Ucuncusu, ARIMA LSTM ve Prophet i anlamli "
    "olarak yener (her ikisinde p < 0.001); yani secenek LSTM veya Prophet ise ARIMA mantikli bir "
    "tercih, ancak tek satirlik bir gecikme-1 kurali da ayni isi yapar."
)

add_table_caption("Tablo 2. Ev 2 icin Harvey-Leybourne-Newbold kucuk orneklem duzeltmesiyle "
                  "Diebold-Mariano test sonuclari. n = 123 test gunu, iki tarafli p-degerleri.")

table2 = doc.add_table(rows=6, cols=4, style='Light Grid Accent 1')
table2.alignment = WD_TABLE_ALIGNMENT.CENTER
dm_headers = ['Karsilastirma (Model 1 vs Model 2)', 'DM Istatistigi', 'p-degeri', 'Sonuc']
dm_data = [
    ['ARIMA vs Persistence',  '-0.433',  '0.665',     'Anlamli fark yok'],
    ['LSTM vs Persistence',   '+3.936',  '< 0.001',   'Persistence anlamli olarak iyi'],
    ['Prophet vs Persistence','+7.949',  '< 0.001',   'Persistence anlamli olarak iyi'],
    ['ARIMA vs LSTM',         '-3.765',  '< 0.001',   'ARIMA anlamli olarak iyi'],
    ['ARIMA vs Prophet',      '-7.957',  '< 0.001',   'ARIMA anlamli olarak iyi'],
]
for i, h in enumerate(dm_headers):
    c = table2.rows[0].cells[i]
    c.text = h
    for p in c.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(10)
            r.font.name = 'Calibri'
for r_idx, row in enumerate(dm_data):
    for c_idx, v in enumerate(row):
        c = table2.rows[r_idx + 1].cells[c_idx]
        c.text = v
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(10)
                r.font.name = 'Calibri'

doc.add_paragraph()

add_figure("dm_test_plot.png",
           "Sekil 11. Ev 2 icin Diebold-Mariano istatistikleri. Yesil cubuklar yuzde 5 seviyesinde "
           "anlamli (|DM| > 1.96), gri cubuklar anlamli degil. ARIMA ile Persistence "
           "karsilastirmasi anlamli olmayan tek ciftir.",
           width=Inches(6.0))

# ============================================================
# 5.6 CROSS-HOUSE VALIDATION (TR)
# ============================================================
add_heading("5.6 Hane-Asiri Dogrulama", level=2)
add_para(
    "Ev 2 deki sira lamasinin tek bir hanenin tesadufu olmadigini gostermek icin tum boru hattini "
    "Ev 1 ve Ev 5 te tekrarladik. Bu iki ev farkli kullanim duzeni ve cihaz karisimina sahip "
    "(Ev 1 de dondurucular ve kurutucu, Ev 5 te belirgin sekilde daha yuksek gunluk ortalama guc "
    "bulunuyor); dolayisiyla uc evde de ayakta kalan herhangi bir siralama tesadufi olamaz. "
    "Tablo 3, hane basina R2 degerlerini sunar."
)

add_table_caption("Tablo 3. Uc REFIT hanesinde model basina R2. Persistence onemsiz temel "
                  "modeldir; ARIMA her evde dar bir farkla kazanir, LSTM ve Prophet ise tutarli "
                  "sekilde Persistence in altinda kalir.")

table3 = doc.add_table(rows=5, cols=5, style='Light Grid Accent 1')
table3.alignment = WD_TABLE_ALIGNMENT.CENTER
ch_headers = ['Model', 'Ev 1', 'Ev 2', 'Ev 5', 'Yargi']
ch_data = [
    ['Persistence', '0.963', '0.873', '0.901', 'Guclu temel model'],
    ['ARIMA',       '0.976', '0.876', '0.905', 'Her evde en iyi'],
    ['LSTM',        '0.859', '0.748', '0.647', 'Her evde Persistence altinda'],
    ['FB-Prophet',  '-2.315', '0.015', '-1.186', 'Sik sik negatif R2'],
]
for i, h in enumerate(ch_headers):
    c = table3.rows[0].cells[i]
    c.text = h
    for p in c.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(10)
            r.font.name = 'Calibri'
for r_idx, row in enumerate(ch_data):
    for c_idx, v in enumerate(row):
        c = table3.rows[r_idx + 1].cells[c_idx]
        c.text = v
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(10)
                r.font.name = 'Calibri'

doc.add_paragraph()

add_figure("cross_house_comparison.png",
           "Sekil 12. Hane basina model R2 si. ARIMA ile Persistence arasindaki fark uc evde de "
           "kucuk, LSTM tutarli sekilde Persistence in altinda, Prophet Ev 1 ve Ev 5 te negatif "
           "R2 uretiyor.",
           width=Inches(6.3))

add_para(
    "Iki bulgu burada vurgulanmali. Birincisi, ARIMA ile Persistence arasindaki fark her evde "
    "kucuk; yani Ev 2 sonucu sira disi degil. Ikincisi, Prophet uc evden ikisinde negatif R2 "
    "ureterek koshulsuz ortalamadan bile daha kotu tahmin ediyor; bu, tek hane bulgusundan daha "
    "guclu bir ifade."
)

# ============================================================
# 5.7 PRACTICAL INTERPRETATION (TR)
# ============================================================
add_heading("5.7 Hata Degerlerinin Pratik Yorumu", level=2)
add_para(
    "RMSE degerleri, alan birimlerine cevrildiginde daha kolay anlasilir. Ev 2 icin ortalama test "
    "tuketimi 434.8 W, yani ARIMA nin 48.7 W luk RMSE si tipik gunluk seviyenin yaklasik yuzde "
    "11.2 sine denk gelir. Enerji cinsine cevrildiginde, 24 saat boyunca surdurulen 48.7 W luk "
    "ortalama-guc hatasi yaklasik 1.17 kWh/gun eder. Birlesik Krallik 2025 konut elektrik birim "
    "fiyati yaklasik 0.27 GBP/kWh oldugunda, bu tek hane icin yaklasik 0.32 GBP/gun beklenen "
    "faturalama hatasi anlamina gelir; aylik yaklasik 10 GBP. Toplulastirilmis bir bilanco "
    "ortaminda gun-onceki dengesizlik 0.10 GBP/kWh fiyatlandirildiginda maliyet yaklasik "
    "0.12 GBP/gun e duser. Bu sayilar hane basina kucuk olsa da portfoy buyuklugu ile dogrusal "
    "olarak olceklenir."
)

# ============================================================
# 6. DISCUSSION
# ============================================================
add_heading("6. Tartisma", level=1)

add_heading("6.1 Persistence Sonucu ve Bize Soyledigi", level=2)
add_para(
    "Bu calismanin en onemli bulgusu ARIMA nin diger modelleri yenmesi degil, ARIMA nin persistence i "
    "ancak duz duz yenmesi ve farkin istatistiksel olarak anlamli olmamasidir. Persistence yarinin "
    "bugune esit oldugunu tahmin eder: hicbir ogrenilmis parametresi olmayan tek satirlik bir kural. "
    "Ev 2 de R2 = 0.873 e ulasiyor, ARIMA nin 0.876 sindan sadece 0.003 dusuk. Diebold-Mariano testi "
    "(p = 0.665) iki modelin karesel hata kayiplarinin ayirt edilemez oldugunu dogrular. Hane-asiri "
    "sonuclar ayni resmi cizer: ARIMA nin Persistence uzerindeki R2 farki Ev 1 de 0.013, Ev 5 te 0.004."
)
add_para(
    "Mekanik neden, 7 gunluk yumusatilmis gunluk tuketiminin guclu gecikme-1 otokorelasyonudur. "
    "Dun bugunu mukemmel sekilde tahmin eder ve dunu dogrudan kullanan herhangi bir model neredeyse "
    "ayni performansi gosterir. ARIMA(2, 1, 2) iki gecikme daha ve iki hareketli-ortalama terimi "
    "ekler, ancak ek bilgi gecikme-1 e kiyasla kucuktur. Pratik sonuc net: bu granulariteyde ve "
    "bu sinyal uzerinde, tek satirlik bir kural zaten oraddatahmin edilebilir yapiyi yakaliyorken "
    "agir makineler kullanmayin."
)

add_heading("6.2 LSTM Neden Onemsiz Temel Modelden de Dusuk Performans Gosterdi", level=2)
add_para(
    "LSTM yalnizca ARIMA ya kaybetmiyor, Persistence e karsi da anlamli sekilde kaybediyor (Ev 2 de "
    "p < 0.001, diger iki evde benzer oruntu). Bu daha agir bir sonuc: 128.929 parametreli sinir agi, "
    "yarinin bugune esit olacagini tahmin etmekten daha kotu. Egitim seti 490 gunluk gozlemden olusur "
    "ve 14 gunluk geriye bakis ile yalnizca 476 girdi dizisi verir. Bu kadar az veriyle ag asiri "
    "kapasiteye sahip; yumusak ortalama davranisi ogreniyor ve Persistence in tanim geregi yakaladigi "
    "gunden gune hareketleri asiri yumusatiyor. Son donem calismalari (Gasparin ve digerleri, 2024) "
    "benzer oruntuyu belgeler: alti aydan kisa egitim verisinde basit temel modeller derin modelleri "
    "geride birakir. Bizim verimiz daha uzun, ancak yumusatilmis gunluk sinyal hala derin ogrenmenin "
    "net olarak negatif oldugu bolgede gorunuyor."
)

add_heading("6.3 Prophet Neden En Dusuk Skoru Aldi", level=2)
add_para(
    "Prophet in Ev 2 deki sifir civarindaki R2 si zaten cesaret kirici degildi. Hane-asiri dogrulama "
    "resmi daha da kotulestiriyor: Ev 1 de R2 = -2.315 ve Ev 5 te R2 = -1.186, yani Prophet kosulsuz "
    "egitim ortalamasindan onemli olcude daha kotu tahmin ediyor. Iki etken devrededir. Birincisi, "
    "Prophet tum test ufkunu test seti gercek degerlerine erismeden tek seferde tahmin eder; bu, "
    "yuvarlanan Persistence, ARIMA ve LSTM kurulumlarina kiyasla onu yapisal olarak dezavantajli "
    "birakir. Ikincisi, Prophet in guclu yani yavas mevsimsel trendleri ve takvim etkilerini "
    "yakalamaktir; yumusatilmis gunluk konut verisindeki baskin sinyal bir onceki gun olup Prophet in "
    "ayristirmasinin hedeflemedigi bilesendir. Adil bir karsilastirma Prophet i yuvarlanan yeniden "
    "uydurma modunda calistirmayi gerektirir, ancak veri karakteriyle yapisal uyumsuzluk yine kalir."
)

add_heading("6.4 Kisitlamalar ve Gecerlilik Tehditleri", level=2)
add_para(
    "Uc kisitlama sonuclarimizi nitelendirir."
)
add_bullet("Yirmi degil, uc hane. Hane-asiri dogrulama orijinal tek-hane bulgusunu guclendirir, "
           "ancak kalan 17 REFIT evini henuz test etmiyor.")
add_bullet("Tek degiskenli kurulum. Modellerin hicbiri hava, takvim veya cihaz duzeyinde disasal "
           "veri almaz. Bunlarin eklenmesi tabloyu, ozellikle daha zengin girdileri emmek icin "
           "tasarlanan LSTM lehine, degistirebilir.")
add_bullet("Agir yumusatma. 7 gunluk hareketli ortalama yuksek frekansli icerigi ortadan kaldirir. "
           "Gunluk rampa bilgisine ihtiyac duyan bir operasyonel tahminci icin bu secim yeniden "
           "gozden gecirilmelidir; persistence avantaji daha ince zaman olceklerinde kuculebilir.")

add_heading("6.5 Referans Literatur ile Karsilastirma", level=2)
add_para(
    "Burada gozlemlenen ARIMA, LSTM ve Prophet siralamasi, Buluc, Sevli ve Yunlu (2025) un Istanbul gunes uretim verisinde benzer yuvarlanan protokol altinda raporladigi (R2 = 0.97) ARIMA performansiyla ortusur. Demirtop ve Sevli (2024) un LSTM in ARIMA yi gectigi ruzgar hizi calismasindan ise ayrisir; en olasi neden o calismada cok yillik saatlik verinin kullanilmis olmasidir. CNN-LSTM-Transformer (Limouni ve digerleri, 2023) ve STL-Prophet-LSTM (Xie ve digerleri, 2022) gibi hibrit modeller bilesenlerinden tutarli sekilde daha iyi sonuc verir ve burada karsilastirilan tek-model temellerinin dogal sonraki adimini olusturur."
)

# ============================================================
# 7. CONCLUSION
# ============================================================
add_heading("7. Sonuc ve Gelecek Calismalar", level=1)

add_para(
    "Persistence temel modeli dahil dort yontem kullanilarak uc Birlesik Krallik hanesinin gunluk "
    "ortalama gucunu tahmin eden tekrar uretilebilir bir boru hatti kurduk. Yuvarlanan tek-adim-onde "
    "protokol ve sabit rastgele tohum altinda, ARIMA(2, 1, 2) her evde en iyi model oldu, ancak tek "
    "satirlik persistence kurali uzerindeki marji istatistiksel olarak anlamli degildi (Ev 2 de "
    "Diebold-Mariano p = 0.665 ve Ev 1 ile Ev 5 te benzer kucuk farklar). LSTM ve FB-Prophet uc "
    "ortamin tumunde persistence e anlamli olarak kaybetti; Prophet uc evden ikisinde negatif R2 "
    "uretti. Cikardigimiz ders, bu granulariteyde konut gunluk enerjisinin gecikme-1 otokorelasyonu "
    "tarafindan domine edildigi ve onemsiz temel modelin uzerine model kapasitesi eklemenin olculebilir "
    "kazanc saglamadigi (ARIMA) veya aktif olarak zararli oldugu (LSTM, Prophet) yonundedir."
)

add_para(
    "Metodolojik ders de en az ayni kadar onemli: yalnizca karmasik modelleri birbirine karsi raporlamak, "
    "tum model sinifinin gereksiz oldugu gercegini gizleyebilir. Persistence temel modeli ile Diebold-"
    "Mariano anlamlilik testi birlikte, temiz bir ARIMA zaferi gibi gorunen sonucu daha durust 'veri "
    "modellerin onemli olmasi icin fazla tahmin edilebilir' sonucuna donusturur."
)

add_para(
    "Ileride yapilacak calismalar icin dort yon one cikiyor."
)
add_bullet("Gecikme-1 otokorelasyonunun daha zayif oldugu ve derin modellerin gercekten katki "
           "saglayabilecegi daha yuksek frekansli hedefte (saatlik veya 15 dakikalik) analizi tekrarlamak.")
add_bullet("Hava (sicaklik, isinim) ve takvim ozelliklerini SARIMAX ve cok degiskenli LSTM "
           "araciligiyla eklemek; bu daha agir modellere persistence in kullanamayacagi bilgiyi verir.")
add_bullet("Hane-asiri karsilastirmayi ucten tum 20 REFIT evine uzatmak ve hane-asiri transfer "
           "ogrenmesini kesfetmek.")
add_bullet("Ayristirma ve sinirsel dizi ogrenmenin guclu yanlarini birlestiren STL-Prophet-LSTM ve "
           "CNN-LSTM-Transformer gibi hibrit modeller kurmak.")

add_heading("Tekrarlanabilirlik Notu", level=2)
add_para(
    "Tum deneyler NumPy, Python in random modulu ve TensorFlow icin sabit rastgele tohum (42) kullanir. Veri seti, REFIT in herkese acik Kaggle aynasindan indirilir ve on isleme, egitim ve degerlendirme tek bir Python betiginde (energy_forecasting.py) kodlanir. Bu rapordaki sonuclar Python 3.13, TensorFlow 2.x, statsmodels 0.14 ve Prophet 1.3 uzerinde elde edilmistir."
)

# ============================================================
# REFERENCES
# ============================================================
add_heading("Kaynakca", level=1)

refs = [
    "Atalay, B. A., and Zor, K. (2025). XGBoost ile hidroelektrik enerji tahmini. "
    "Çukurova Üniversitesi Mühendislik Fakültesi Dergisi, 40(1), 205-218.",

    "Berus, Y., and Yakut, Y. B. (2024). Derin öğrenme (1D-CNN, RNN, LSTM, BiLSTM) ile enerji "
    "tüketim tahmini: Diyarbakır AVM örneği. Dicle University Journal of Engineering, 15(2), "
    "311-322.",

    "Bülüç, M., Sevli, O., and Yünlü, L. (2025). Time Series Analysis of Solar Energy Production "
    "Based on Weather Conditions. GU J Sci, Part A, 12(4), 1060-1077.",

    "Çolak, M. B., and Özhan, E. (2025). Renewable energy forecasting in Turkey: Analytical "
    "approaches. Journal of Intelligent Systems: Theory and Applications, 8(1), 25-34.",

    "Demirtop, A., and Sevli, O. (2024). Wind speed prediction using LSTM and ARIMA time series "
    "analysis models: A case study of Gelibolu. Turkish Journal of Engineering, 8(3), 524-536.",

    "Gasparin, A., Lukovic, S., and Alippi, C. (2024). Load Forecasting for Households and "
    "Energy Communities: Are Deep Learning Models Worth the Effort? arXiv:2501.05000.",

    "Limouni, T., Yaagoubi, R., Bouziane, K., Guissi, K., and Baali, E. H. (2023). Solar Energy "
    "Production Forecasting Based on a Hybrid CNN-LSTM-Transformer Model. Mathematics, 11(3), 676.",

    "Murray, D., Stankovic, L., and Stankovic, V. (2017). An electrical load measurements "
    "dataset of United Kingdom households from a two-year longitudinal study. Scientific Data, "
    "4, 160122.",

    "Rahman, M. R., and others (2025). Time-series and deep learning approaches for renewable "
    "energy forecasting in Dhaka: a comparative study of ARIMA, SARIMA, and LSTM models. "
    "Discover Sustainability, 6, 01733.",

    "Sakib, N., and others (2024). Deep learning-driven hybrid model for short-term load "
    "forecasting and smart grid information management. Scientific Reports, 14, 63262.",

    "Tamay, M., and Türker, G. F. (2024). Machine learning based energy forecasting for "
    "photovoltaic solar plants. Yekarum, 9(2), 128-146.",

    "Triebe, O., Hewamalage, H., Pilyugina, P., Laptev, N., Bergmeir, C., and Rajagopal, R. "
    "(2021). NeuralProphet: Explainable Forecasting at Scale. arXiv:2111.15397.",

    "Vargas-Forero, V. M., Manotas-Duque, D. F., and Trujillo, L. (2025). Comparative study of "
    "forecasting methods to predict the energy demand for the market of Colombia. International "
    "Journal of Energy Economics and Policy, 15(1), 65-76.",

    "Xie, J., Li, Z., Zhou, Z., and Liu, S. (2022). A hybrid forecasting model using LSTM and "
    "Prophet for energy consumption with decomposition of time series data. PeerJ Computer "
    "Science, 8, e1001.",
]

for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f"[{i}] {ref}")
    r.font.size = Pt(9.5)
    r.font.name = 'Calibri'


# ============================================================
# SAVE DOCX
# ============================================================
doc.save(OUTPUT_DOCX)
print(f"DOCX saved: {OUTPUT_DOCX}")
print(f"DOCX size: {os.path.getsize(OUTPUT_DOCX)/1024:.0f} KB")

# ============================================================
# CONVERT TO PDF
# ============================================================
print("\nConverting to PDF...")
try:
    from docx2pdf import convert
    convert(OUTPUT_DOCX, OUTPUT_PDF)
    print(f"PDF saved: {OUTPUT_PDF}")
    print(f"PDF size: {os.path.getsize(OUTPUT_PDF)/1024:.0f} KB")
except Exception as e:
    print(f"docx2pdf failed: {e}")
    print("Will try alternative PDF conversion methods.")
