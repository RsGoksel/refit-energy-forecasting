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
    "Bu rapor, hane halki enerji tuketimi tahmininde kullanilan uc zaman serisi modelinin karsilastirmali bir incelemesini sunmaktadir: ARIMA, Long Short-Term Memory (LSTM) ve FB-Prophet. REFIT Akilli Ev veri setindeki 2 numarali hanenin 22 aylik 8 saniye cozunurluklu olcumlerini kullaniyoruz. Veriler gunluk ortalama gucu uretecek sekilde yeniden orneklenir, ardindan 7 gunluk hareketli ortalama ile yumusatilir ve son olarak yuzde 80 egitim, yuzde 20 test olacak sekilde zaman sirasinda bolunur. ARIMA modeli ADF duraganlik testi ve AIC olcutune gore (p, d, q) izgara aramasi ile ayarlanir, ardindan tek adim onde yuvarlanan tahmin protokolu altinda calistirilir. LSTM modeli uc katmanli yiginlanmis RNN mimarisinden olusur ve erken durdurma ile 100 epoch egitilir. Prophet, haftalik ve yillik mevsimsellik bilesenleriyle tek seferlik cok adim tahmin modunda kullanilir. ARIMA en yuksek dogrulugu yakalar (R2 = 0.876, RMSE = 48.7 W), LSTM ikinci sirada (R2 = 0.193) ve Prophet ucuncu sirada (R2 = 0.015) yer alir. ARIMA ile diger iki model arasindaki buyuk fark, kismen tahmin protokolune baglidir: ARIMA ve LSTM ogretmen zorlamasindan yararlanir, Prophet ise 122 gunluk tahmin ufkuna tek seferde baglanmak zorundadir. Sonuclar literaturde sik karsilasilan goruslerle ortusur: klasik istatistiksel modeller kisa ufuklu konut tuketimi tahmininde rekabetci kalmaya devam eder, derin ogrenmenin kazanci ise veri olcegine ve karsilastirma protokolune kosulludur. Sabit rastgele tohum kullanilan tum kod tabani bu rapora eslik etmektedir."
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

add_heading("3.5 Degerlendirme Metrikleri", level=2)
add_para(
    "Tahmin dogrulugu birbirini tamamlayan dort metrikle olculur. Ortalama Karesel Hata (MSE) ve Karekok Ortalama Karesel Hata (RMSE) buyuk hatalari agir bicimde cezalandirir; RMSE ozgun birim olan Watt cinsinden raporlanir. Ortalama Mutlak Hata (MAE) aykiri degerlere daha dayaniklidir ve yine Watt cinsindendir. Belirleme katsayisi (R2), aciklanan varyansin birimsiz olcumudur; 1 mukemmel tahmini, ortalama temel modelinin altinda kalan modeller icin negatif degerleri ifade eder."
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
    "Tablo 1, test seti uzerinde uc model icin elde edilen metrikleri raporlar. ARIMA dort metrigin tumunde acik bir farkla onde yer alir: R2 = 0.876 ile LSTM in yaklasik dort kati, Prophet in ise yaklasik altmis kati kadar. RMSE farki daha da carpicidir: ARIMA 48.7 W iken LSTM 124.2 W ve Prophet 137.3 W."
)

add_table_caption("Tablo 1. Ev 2 gunluk tahminleri icin uc modelin test seti performansi.")

table = doc.add_table(rows=4, cols=5, style='Light Grid Accent 1')
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Model', 'MSE', 'RMSE (W)', 'MAE (W)', 'R2']
data = [
    ['ARIMA(2,1,2)', '2,370.01', '48.68', '32.75', '0.876'],
    ['LSTM (3-layer)', '15,436.04', '124.24', '93.59', '0.193'],
    ['FB-Prophet',    '18,851.52', '137.30', '111.70', '0.015'],
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
# 6. DISCUSSION
# ============================================================
add_heading("6. Tartisma", level=1)

add_heading("6.1 ARIMA Neden En Iyi Sonucu Verdi", level=2)
add_para(
    "ARIMA nin guclu performansi iki etkenle aciklanir. Birincisi veri karakteridir: gunluk duzeyde konut enerjisi gecikme 1 de guclu otokorelasyon gosterir, dolayisiyla bir onceki gun bugunki tahmin icin tek basina en bilgilendirici ozelliktir. ARIMA(2, 1, 2) bu ozellige otoregresif ve hareketli ortalama terimleri uzerinden dogrudan basvurur. Ikincisi tahmin protokoludur: her adim en yeni gercek degere dayanir; bu durum, modelin parametreleri test penceresinde hafifce kayisa bile tahminleri sabit tutar."
)

add_heading("6.2 LSTM Neden Beklenenden Dusuk Performans Gosterdi", level=2)
add_para(
    "LSTM in mutevazi skoru derin ogrenme aleyhine bir hukum degildir; veri olcegi hakkinda bir yorumdur. Egitim seti 490 gunluk gozlemden olusur ve 14 gunluk geriye bakis ile birlikte yalnizca 476 girdi dizisi anlamina gelir. Yaklasik 129 bin parametreye sahip derin ogrenme mimarileri tam potansiyellerine ulasmak icin tipik olarak buyuklukler mertebesinde daha fazla orneklem ister. Sekil 8 deki egitim ve dogrulama egrileri modelin yakinsadigini ancak iyi genellestiremedigini gosterir. Son donem calismalari (Gasparin ve digerleri, 2024) benzer bir oruntuyu belgeler: alti aydan kisa egitim verisinde basit temel modeller derin modelleri geride birakir; ancak dokuz ay veya daha uzun veriyle derin mimariler one gecmeye baslar."
)

add_heading("6.3 Prophet Neden En Dusuk Skoru Aldi", level=2)
add_para(
    "Prophet in sifir civarindaki R2 si dikkatli yorumlanmalidir. Iki etken devrededir. Birincisi, Prophet tum 122 gunluk ufuk icin tek seferlik cok-adim tahmin uretir ve test seti gercek degerlerine erisemez; bu, yuvarlanan ARIMA ve LSTM kurulumlarina kiyasla onu yapisal olarak dezavantajli birakir. Ikincisi, Prophet in guclu yani yavas mevsimsel trendleri ve takvim etkilerini yakalamaktir; her iki ogeyi de Ev 2 verisinde gormek mumkun, ancak ikisi de tuketimin baskin surukleyicisi degildir. Test seti varyansinin buyuk kismini olusturan gunden gune kalan degiskenlik, tam olarak Prophet in modellemeye calismadigi bilesendir."
)
add_para(
    "Cikarim, Prophet in zayif bir model olmasi degil, karsilastirma kurallarinin ogretmen zorlamasi yapabilen modelleri kayirmasidir. Bu veri seti uzerinde adil bir karsilastirma Prophet i de yuvarlanan yeniden uydurma modunda calistirmayi gerektirir; bunu yaklasik iki buyukluk mertebesinde fazla hesaplama gerektirdigi icin ileride yapilacak calismalar arasinda biraktik."
)

add_heading("6.4 Kisitlamalar ve Gecerlilik Tehditleri", level=2)
add_para(
    "Uc kisitlama sonuclarimizi nitelendirir."
)
add_bullet("Tek hane. Ev 2 diger 19 REFIT evini temsil etmeyebilir; farkli bir kullanim duzeni veya cihaz karisiminda sira degisebilir.")
add_bullet("Tek degiskenli kurulum. Modellerin hicbiri hava, takvim veya cihaz duzeyinde disasal veri almaz. Bunlarin eklenmesi farkin, ozellikle LSTM lehine, kapanmasini kolaylastiracaktir.")
add_bullet("Agir yumusatma. 7 gunluk hareketli ortalama yuksek frekansli icerigi ortadan kaldirir. Gunluk rampa bilgisine ihtiyac duyan bir operasyonel tahminci icin bu secim yeniden gozden gecirilmelidir.")

add_heading("6.5 Referans Literatur ile Karsilastirma", level=2)
add_para(
    "Burada gozlemlenen ARIMA, LSTM ve Prophet siralamasi, Buluc, Sevli ve Yunlu (2025) un Istanbul gunes uretim verisinde benzer yuvarlanan protokol altinda raporladigi (R2 = 0.97) ARIMA performansiyla ortusur. Demirtop ve Sevli (2024) un LSTM in ARIMA yi gectigi ruzgar hizi calismasindan ise ayrisir; en olasi neden o calismada cok yillik saatlik verinin kullanilmis olmasidir. CNN-LSTM-Transformer (Limouni ve digerleri, 2023) ve STL-Prophet-LSTM (Xie ve digerleri, 2022) gibi hibrit modeller bilesenlerinden tutarli sekilde daha iyi sonuc verir ve burada karsilastirilan tek-model temellerinin dogal sonraki adimini olusturur."
)

# ============================================================
# 7. CONCLUSION
# ============================================================
add_heading("7. Sonuc ve Gelecek Calismalar", level=1)

add_para(
    "Tek bir Birlesik Krallik hanesinin gunluk ortalama gucunu tahmin eden tekrar uretilebilir bir boru hatti kurduk ve uc zaman serisi yontemini kullandik. Yuvarlanan tek-adim-onde protokol ve sabit rastgele tohum altinda, ARIMA(2, 1, 2) 122 gorulmemis gun uzerinde R2 = 0.876 a ulasti; uc katmanli LSTM (R2 = 0.193) ve FB-Prophet (R2 = 0.015) modellerini geride birakti. Cikardigimiz dersler sunlardir: tahmin protokolu, kisa serilerde model secimini gectigi bir noktaya kadar baskindir; konut gunluk enerjisi, klasik modellerin dogal olarak yararlandigi gucludeli-1 otokorelasyon sergiler; ve derin mimariler burada elde edilenden onemli olcude fazla veri ister."
)

add_para(
    "Ileride yapilacak calismalar icin dort yon one cikiyor."
)
add_bullet("Yuvarlanan protokolu Prophet a da uygulayarak adil bir cok model karsilastirmasi yapmak.")
add_bullet("Hava (sicaklik, isinim) ve takvim ozelliklerini SARIMAX ve cok degiskenli LSTM araciligiyla eklemek.")
add_bullet("Derin ogrenme egitim maliyetini paylasmak icin 20 REFIT hanesi arasinda hane-asiri transfer ogrenmesi yapmak.")
add_bullet("Ayristirma ve sinirsel dizi ogrenmenin guclu yanlarini birlestiren STL-Prophet-LSTM ve CNN-LSTM-Transformer gibi hibrit modeller kurmak.")

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
