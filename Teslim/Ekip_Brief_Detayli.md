# Ekip Brief, Detayli Surum

Selam,

Onceki brief'i okuduktan sonra model kismi tam oturmamis. Cok normal, ben de ilk basta dolastim. Bu sefer **sifirdan**, gunluk dilden basliyorum. Sonunda projeyi senden iyi anlayan ben olmuyorum, sen oluyorsun. Sloganli laflar yok, gercek aciklamalar var.

---

## BOLUM 1: Genel Resim

### Q: Bizim projemizin amaci tam olarak neydi?

**Cok kisa cevap:** Bir evin yarinki elektrik tuketimini bugun tahmin etmek.

**Biraz daha uzun cevap:** Diyelim ki evine akilli sayac taktirdin. Sayac saniyede bir kac kere "su an evde X watt cekiyorsun" diye veri kaydediyor. Soru su:

> Yarin sabah uyandiginda evinin gun boyunca ortalama kac watt cekecegini *bugunden* bilebilir miyiz?

Eger bunu bilebilirsen su islere yariyor:
- **Sebeke isletmecisi:** Yarinki toplam talebi tahmin edip santralleri ayarlar
- **Sen:** Catindaki gunes panelinden batarya doldurma saatlerini optimize edersin
- **Tedarikci:** "Yarin saat 18'de tuketim patliyor, fiyat yukseltelim" der

Yani **enerji ekonomisinin temelinde tahmin var**. Biz bunun en kucuk birimini, tek hane senaryosunu calistik.

### Q: Niye bu proje? Hoca mi soyledi?

Hoca "ML + Enerji Sistemleri" alaninda 3 proje onerisi istedi (6 Nisan). Biz uc oneri sunduk, bunlardan birini (REFIT veri seti ile zaman serisi tahmini) sectik ve gelistirdik. Sectiqimiz konu makaledeki calismanin (Buluc et al. 2025) hane bazina indirgenmis haliydi.

### Q: Makalede ne yapilmis ki bizim referansimiz oldu?

Buluc ve arkadaslari Istanbul Ikitelli'deki bir gunes santralinin uretimini ARIMA / LSTM / Prophet ile tahmin etmis. ARIMA en iyiyi yapmis (R²=0.97). Bizim sorumuz: **ayni uc model hane bazli verisi icin ne yapar?** Gunes santrali tahmini ile ev tahmini cok farkli, cunku ev cok daha gurultulu.

---

## BOLUM 2: Veri

### Q: REFIT veri seti tam olarak ne?

Birlesik Krallik'ta uc universite (Strathclyde, Loughborough, East Anglia) Ekim 2013 - Haziran 2015 arasinda 20 evi izlemis. Her eve:
- 1 **toplam sayac** (eve giren toplam akim)
- 9 **bireysel cihaz monitoru** (buzdolabi, camasir makinesi, su isiticisi, vs.)

her 8 saniyede bir watt cinsinden okuma yapmislar. **Toplam yaklasik 1.2 milyar veri noktasi.**

Veriyi cikartip publish etmisler, Creative Commons lisansli ucretsiz indirilebilir. Kaggle aynasindan indirdik (~890 MB).

### Q: 20 evden niye sadece 3'unu kullandik?

Iki neden:
1. **Pratik:** 20 evin hepsini calismak ARIMA rolling forecast ile bilgisayarimizda saatler surer
2. **Yeterli:** Hocanin "tek hane mi calistiniz?" elestirisine cevap vermek icin 3 ev yeterli. Sonuc 3 evde de ayni olursa "tek hane tesaduf degil" demis oluyoruz

Sectigimiz evler:
- **Ev 1:** 372 W ortalama, dondurucu/dryer agirlikli
- **Ev 2:** 434 W ortalama, "tipik" Ingiliz evi (referans)
- **Ev 5:** 673 W ortalama, daha agir tuketim

Yani farkli profiller. Eger ARIMA uc evde de kazaniyorsa, ev tipinden bagimsiz.

### Q: 8 saniyelik veriyle nasil yarini tahmin ediyorsun? Cok detayli degil mi?

Iyi soru. Ham veriyle calismadik. **Ozetledik:**

1. 8 saniye veri (yaklasik 5.7 milyon satir Ev 2 icin)
2. **Gunluk ortalamaya** indirdik → 5.7M satir → ~630 gun
3. **7 gunluk hareketli ortalama** uyguladik → gurultu silindi, haftalik dongu kaldi
4. **80% egitim, %20 test** olarak boldik

"Gunluk ortalama" demek: o gun boyunca evin cektigi ortalama wattaj. Ornegin 24 saat boyunca ortalama 280 W cekmis. Bu sayi modellerin tahmin ettigi sey.

### Q: Niye gunluk? Saatlik daha iyi olmaz miydi?

Saatlik denedik (iterasyon 1), **R² = -0.13** cikti. Negatif demek "modelimiz ortalama tahminden bile daha kotu" demek. Yani saatlik veride gurulti cok fazla, modeller karman corman tahmin yapiyor.

Gunluk ortalama gurultuyu azaltiyor, modelin yakalayabilecegi pattern'i ortaya cikariyor. Bu **iterasyon hikayemizin** kalbi.

---

## BOLUM 3: Tahmin Probleminin Temeli

### Q: "Zaman serisi tahmini" tam olarak nedir?

Bir sayinin zamanla nasil degistigini gosteren veri = zaman serisi. Ornekler:
- Borsa fiyati (her saniye degisir)
- Hava sicakligi (her saat degisir)
- Senin elektrik tuketimin (her gun degisir)

**Tahmin** = "su anki ve gecmis degerleri kullanarak gelecekteki degeri bil." Klasik problem, 100 yildir uzerine calisiliyor.

### Q: Niye zor? Veri var, sayilara bak yap gitsin?

Cunku **veri rastgele degil ama tam tahmin edilebilir de degil.** Iki dengede:
- **Cok kalipli olsa:** "Yarin = bugun" der gecersin
- **Cok rastgele olsa:** Tahmin imkansizdir

Gercek hayat ortada. Ornegin senin tuketimin:
- Mevsim etkisi var (kis > yaz) ← tahmin edilebilir
- Hafta sonu etkisi var (cumartesi > sali) ← tahmin edilebilir
- Belirli saatlerde pik (18:00 yemek) ← tahmin edilebilir
- Bugun bir misafir geldi 2 saat extra TV ← rastgele

Model bu **tahmin edilebilir kalibi ogrenmeye** calisiyor. Rastgele kismi degil.

---

## BOLUM 4: Modeller

Burayi dikkatli oku, hocanin **en cok soru sorabilecegi yer** burasi.

### Q: 4 modelimiz vardi. Tam olarak ne yapiyorlar?

Sirasi onemli. **Basitten karmasiga:**

#### 1. Persistence (Yapiskanlik)
**Kural:** "Yarinki tuketim = bugunku tuketim."

Tek satirlik kod:
```python
tahmin[yarin] = gercek[bugun]
```

Yani hicbir "ogrenme" yok. Sadece son bilineni tekrar et. Buna **baseline** denir, kontrolcuye benzer. Karmasik modellerin gercekten faydali olup olmadigini test etmek icin.

**Niye ekledik?** Cunku **eger karmasik modelin Persistence'i yenemiyorsa, o model ise yaramaz.** Bu projenin **en kritik bulgusu** buradan cikiyor.

#### 2. ARIMA (Klasik istatistik)
**Tam adi:** AutoRegressive Integrated Moving Average

**Mantigi:** "Bugunku deger, son birkac gunun degerlerinin agirlikli ortalamasi + son birkac gun yaptiqi hatalarin agirlikli ortalamasidir."

Matematiksel olarak:
```
y[t] = c + a₁·y[t-1] + a₂·y[t-2] + e[t] + b₁·e[t-1] + b₂·e[t-2]
```

burada:
- `y[t-1]` = dunku deger
- `y[t-2]` = onceki gunun degeri
- `e[t-1]` = dun yaptiqimiz tahmin hatasi
- `a, b` katsayilari → bunlari veriden ogreniyoruz

Bizimkisi **ARIMA(2, 1, 2)** = 2 onceki deger + 1 fark + 2 hata terimi.

**Niye 1 fark?** Cunku veri "durağan" degildi. Veriyi yarmak/farkini almak gerekti.

**Niye en iyi sonucu verdi?** Cunku **gunluk tuketimde bugun-dun iliskisi cok guclu** (lag-1 otokorelasyon yuksek). ARIMA bunu dogrudan kullaniyor.

#### 3. LSTM (Derin ogrenme)
**Tam adi:** Long Short-Term Memory

**Mantigi:** Bir tur sinir agi (neural network). Kelimeyle anlatmak zor ama soyle:

Hayal et: bir adam masada oturuyor, onunde son 14 gunun guc degerleri yazili. Bu adamin bir "hafizasi" var. 14 gunu okuduktan sonra 15. gunu tahmin ediyor.

**LSTM'in ozelligi:** Bu hafizada hangi gunun onemli oldugunu **otomatik ogreniyor**. Ornegin "8. gun pazardi, pazarlar onemli, oraya odaklan" diyebiliyor.

Bizimkisi 3 katman (128 → 64 → 32 nokta). Toplam **128.929 parametre** ogreniyor.

**Niye bu kadar zayif sonuc verdi?**
- 490 gun egitim verisi, 129 bin parametre icin **cok az**
- Derin ogrenme tipik olarak milyonlarca veri ister
- Gasparin ve digerleri (2024) ayni sonucu bulmus: az veride basit baseline'lar derin ogrenmeyi yener

**Cevap olarak:** "LSTM kotu" demiyoruz. "Bu kadar az veride LSTM ise yaramiyor" diyoruz.

#### 4. FB-Prophet (Facebook Prophet)
**Mantigi:** Veriyi 3 parcaya boler:
- **Trend:** Uzun vadeli yon (yaz dususu, kis cikisi)
- **Mevsimsellik:** Tekrarli desenler (haftalik, yillik)
- **Tatil / ozel olaylar:** Yilbasi, bayram gibi

Sonra her parcayi ayri ayri model alir, toplar.

**Niye en kotu sonucu verdi?**
1. **Protokol farki:** Prophet *tum 122 gunluk test ufkunu* tek seferde tahmin ediyor. Yanlis tahmin yaparsa ufuk boyunca hata birikiyor. ARIMA ve LSTM ise her gun dunun gercek degerini gorebiliyor (sonra detayli aciklayacagim).
2. **Veri tipi:** Prophet uzun vadeli mevsimsel trend icin tasarlanmis. Bizim veride dominant sinyal "yarin = bugun" otokorelasyonu, Prophet bunu hedeflemiyor.

### Q: Yani 4 modelden hangisi en iyiydi?

**Test seti R² degerleri (Ev 2):**

| Model | R² |
|-------|---:|
| Persistence | 0.873 |
| **ARIMA** | **0.876** ⬅ en yuksek |
| LSTM | 0.748 |
| Prophet | 0.015 |

ARIMA **rakamlar olarak** kazandi ama Persistence ile farki sadece 0.003. Bu farkin istatistiksel olarak anlamli olup olmadigi sonraki sorunun konusu.

---

## BOLUM 5: Metrikler

### Q: R² (R-kare) ne demek?

**0 ile 1 arasinda bir sayi.** Anlami:
- **R² = 1.0:** Model mukemmel, hicbir hata yapmamis
- **R² = 0.876:** Model verinin %87.6'sini aciklayabiliyor (yani buyuk olcude dogru)
- **R² = 0:** Model ortalama tahminden iyi degil
- **R² < 0:** Model ortalama tahminden bile daha kotu (cok kotu)

Ozet: **Yuksek R² = iyi tahmin.**

### Q: RMSE, MAE, MSE ne?

Hepsi "tahmin ne kadar yanlis" diyen metriqler. Fark birim ve davranisa bagli.

- **MSE (Mean Squared Error):** Hatalarin karelerinin ortalamasi. Birim "W²" (anlamsiz).
- **RMSE:** MSE'nin karekoku. Birim **Watt**. ARIMA RMSE = 48.7 W = "ortalama tahminim 48.7 W yaniltici."
- **MAE (Mean Absolute Error):** Hatalarin mutlak degerlerinin ortalamasi. Yine Watt birimde, daha az "uctan etkilenir."

Hepsi **dusuk olunca iyi.**

### Q: ARIMA RMSE = 48.7 W neye yariyor?

Ev 2'nin ortalama gunluk tuketimi **434.8 W.** Yani:
- Hata = 48.7 W
- Bu, ortalamanin **%11.2'si** kadar sapma
- Gunluk enerji cinsine cevirirsek: 48.7 W × 24 saat / 1000 = **1.17 kWh/gun hata**
- UK elektrik fiyati ~0.27 GBP/kWh ise: **~0.32 GBP/gun yanilma** = ayda ~10 GBP

Yani modelimiz fena degil, ama mukemmel de degil.

---

## BOLUM 6: En Kritik Konu - Rolling vs Multi-step Protokol

Bu kismi anlarsan **hocayi etkilersin.**

### Q: Rolling forecast ile multi-step forecast ne fark?

Iki yaklasim var:

**Rolling (yuvarlanan) tek-adim onde:**
- Diyelim ki 122 gunluk test setin var.
- Gun 1'i tahmin etmeden once: egitim verisinin tamamini gor, tahmin et.
- Gun 1'in **gercek** degerini ogren (cunku gercek hayatta dun olduktan sonra dunu biliyorsun).
- Gun 2'yi tahmin etmeden once: egitim verisi + gun 1 dahil tum gecmisi gor, tahmin et.
- Gun 3 oncesi: egitim + gun 1 + gun 2 gercekleri ile yeniden tahmin yap.
- Boyle 122 gun boyunca.

Yani **her gun, en yeni gercek veriyi gorerek tahmin ediyorsun.** Bunun adi **teacher forcing** (ogretmen zorlamasi). Persistence, ARIMA ve LSTM bu protokol altinda calisiyor.

**Multi-step (cok adimli):**
- Egitim verisini bir kerede goruyorsun.
- 122 gunun tamamini **tek seferde** tahmin ediyorsun.
- Hicbir gunun gercek degerine erisemiyorsun.
- Yanlis tahmin yaparsan ufuk boyunca hata birikiyor.

Prophet bu protokol altinda calisiyor.

### Q: Niye bunlari ayni protokole gerip karsilastirmadik?

Iki sebep:
1. **Prophet'i rolling protokolde calistirmak cok pahali.** Her test gunu icin Prophet'i bastan egitmek gerekir, ~120 kat hesaplama maliyeti.
2. **Pratikte zaten Prophet boyle kullanilir.** Multi-step Prophet'in kanonik kullanimi.

Ama bu Prophet'a haksizlik diyenler dogru. Raporda bunu **acikca yaziyoruz**: "Prophet skor olarak en kotu ama bunun bir kismi protokolden kaynaklaniyor."

### Q: Hocanin "Prophet niye bu kadar dusuk?" sorusu gelirse?

Su cumleyi kafanda hazir tut:

> "Prophet, 122 gunluk test ufkunun tamamini tek seferde tahmin ediyor ve test seti gercek degerlerine erisemiyor. ARIMA ve LSTM ise her gun bir onceki gunun gercek degerini gorebiliyor (rolling protokol). Bu yapisal fark Prophet'in skorunu dusuruyor. Adil bir kiyaslama icin Prophet'i da rolling modda calistirmak gerekir, ancak hesaplama maliyeti yaklasik 100 kat artiyor."

---

## BOLUM 7: Istatistiksel Anlamlilik (Diebold-Mariano)

### Q: ARIMA R²=0.876, Persistence R²=0.873. Farki 0.003. Bu **gercekten** bir fark mi yoksa tesaduf mu?

Bunu cevaplamak icin **istatistiksel test** lazim. Bizim kullandiqimiz: **Diebold-Mariano testi.**

### Q: Diebold-Mariano testi nasil calisir?

**Kisaca:** "Iki modelin tahminleri arasindaki farkin sifirda olup olmadigini" test eder. Yani: "Bir modelin digerinden gercekten daha az hata yapip yapmadigi" sorusuna cevap verir.

**Cikti:** Bir DM istatistigi (sayi) ve bir **p-value** (0 ile 1 arasi).

**P-value:** Eger gercekten iki model esit performans gosteriyor olsaydi, gozlemledigimiz farki rastlanti eseri gormemizin olasiligi.

- **p < 0.05:** Fark anlamli. Modeller gercekten farkli.
- **p > 0.05:** Fark anlamsiz. Gozlemledigimiz fark muhtemelen tesaduf.
- **p < 0.001:** Cok cok anlamli, "kesinlikle farkli" gibi.

### Q: Bizim sonuclarimiz?

| Karsilastirma | DM | p | Sonuc |
|---------------|---:|--:|-------|
| ARIMA vs Persistence | -0.43 | **0.665** | Anlamsiz! ARIMA aslinda Persistence'i yenmiyor. |
| LSTM vs Persistence | +3.94 | <0.001 | Persistence anlamli olarak iyi |
| Prophet vs Persistence | +7.95 | <0.001 | Persistence anlamli olarak iyi |
| ARIMA vs LSTM | -3.77 | <0.001 | ARIMA anlamli olarak iyi |
| ARIMA vs Prophet | -7.96 | <0.001 | ARIMA anlamli olarak iyi |

### Q: Bunlar ne anlama geliyor?

**Bence projemizin en degerli buluqu:**

1. **ARIMA "kazandi" gibi gorunuyor ama istatistiksel olarak Persistence ile esdeger.** Yani bu kadar veriye ve hesaplama gucune ARIMA icin gerek yok, tek satirlik kural ayni isi yapar.

2. **LSTM ve Prophet, tek satirlik kuraldan istatistiksel olarak DAHA KOTU.** Yani derin ogrenme veya Prophet eklemek, hicbir sey eklememekten daha **zararli**.

3. **ARIMA, LSTM ve Prophet'a karsi anlamli olarak iyi.** Yani secenek bunlar arasindaysa ARIMA al, ama tek satirlik kural daha iyi.

Bu bulgu **akademik olarak degerli** cunku honest. Cogu calismayi "ARIMA en iyi" derken yayinliyorlar, ama Persistence ile kiyaslamiyorlar. Biz kiyasladik.

### Q: Hocanin "DM testi nedir, ne yapiyor?" sorusu gelirse?

Kisa cevap:

> "Diebold-Mariano, iki modelin tahmin hatalarinin istatistiksel olarak farkli olup olmadigini test eden bir hipotez testidir. Negatif DM istatistigi ilk modelin daha az hata yaptigini gosterir. P-value 0.05'in altinda olursa fark anlamlidir. Bizim ARIMA-Persistence p-degerimiz 0.665, yani fark anlamsiz; ARIMA pratik olarak Persistence'i yenmiyor."

---

## BOLUM 8: Cross-House Validation

### Q: Niye 3 evde de calistik?

"Tek evde bulgu" diye eleştirilirsek diye. Eger ARIMA sadece Ev 2'de iyi olsa, sans olabilirdi. 3 evde de ayni patern goruluyorsa, **genel bir gercek**.

### Q: Sonuclar?

| Model | Ev 1 R² | Ev 2 R² | Ev 5 R² |
|-------|--------:|--------:|--------:|
| Persistence | 0.963 | 0.873 | 0.901 |
| ARIMA | **0.976** | **0.876** | **0.905** |
| LSTM | 0.859 | 0.748 | 0.647 |
| Prophet | -2.315 | 0.015 | -1.186 |

**3 evde de:**
- ARIMA en yuksek (ama hep Persistence'a cok yakin)
- LSTM ortada
- Prophet en alt (Ev 1 ve Ev 5'te NEGATIF, yani ortalamadan kotu)

Bu siralama tutarsiz olsa endiselenirdik. Tutarli oldugu icin guvenimiz artti.

### Q: Prophet'in Ev 1'de R² = -2.3 olmasi ne demek?

Modelin urettigi tahminler test setinin **kosulsuz ortalamasindan** bile daha kotu. Yani test gunlerinin ortalamasini hesaplayip her gunu o sayi ile tahmin etsek, Prophet'tan daha iyi sonuc alirdik. Ozellikle Ev 1'in mevsimsellik desenini Prophet yanlis ogrenmis.

---

## BOLUM 9: Uretim Surecimiz

### Q: Pipeline'i nasil kurduk, sirayla anlat.

1. **Veri indirme:** Kaggle'dan UK Electrical Load (REFIT mirror) indirdik. 886 MB ZIP. Icinden Ev 2'yi cikardik.

2. **Veri okuma:** pandas ile House_2.csv'yi yukledik. 5.7 milyon satir, kolonlar Time, Aggregate, Appliance1..9.

3. **Aykiri deger temizleme:** Negatif okumalari sildik (klemp polaritesi hatalari). Ust %1'i sildik (sensor hatasi).

4. **Yeniden ornekleme:** 8-saniye veriyi gunluk ortalamaya cevirdik. ~5.7M satir → ~630 satir.

5. **Yumusatma:** 7 gunluk hareketli ortalama uyguladik. Haftalik desen kaldi, gunluk gurultu silindi.

6. **Eksik veri:** Forward-fill + backward-fill.

7. **Egitim/Test bolme:** Ilk %80 (yaklasik 490 gun) egitim, son %20 (yaklasik 122 gun) test.

8. **Model 1 - Persistence:** `predictions[i] = test[i-1]`. Bir satir kod.

9. **Model 2 - ARIMA:**
   - ADF testi ile veri duraganligini olc → p=0.94, duraganlik yok, d=1 fark al
   - Grid search: p in [0,2], q in [0,2], AIC'ye gore en iyi → ARIMA(2,1,2), AIC=4547.6
   - Her test gunu icin: modeli yeniden uydur, 1 gun tahmin yap

10. **Model 3 - LSTM:**
    - Min-Max ile veriyi 0-1 arasina olceklendir
    - 14 gunluk pencereler olustur
    - Adam optimizer, MSE loss, 100 epoch, batch=16, early stopping
    - Seed=42

11. **Model 4 - Prophet:**
    - Veriyi 'ds' (tarih) ve 'y' (deger) kolonlarina cevir
    - Haftalik + yillik mevsimsellik aktif, multiplicative mod
    - 122 gun tek seferde tahmin

12. **Degerlendirme:** Her model icin MSE, RMSE, MAE, R² hesapla.

13. **DM testi:** Tum ikili karsilastirmalar icin DM istatistigi + p-value.

14. **Cross-house:** Ev 1 ve Ev 5'i de cikar, ayni pipeline'i calistir.

15. **Gorseller:** 12 PNG (EDA, pipeline diyagrami, LSTM mimarisi, model karsilastirma, metrikler, DM, cross-house, vs.)

16. **Belgeler:** Rapor (EN + TR PDF), sunum (PPTX), README.

### Q: Iterasyonlarimiz?

3 iterasyon vardi.

**Iter 1:** Saatlik resample + 3 aylik veri.
- ARIMA R² = -0.13, LSTM = 0.09, Prophet = -0.17.
- Gorudugun gibi negatif. Veri cok az, gurultu cok yuksek.

**Iter 2:** Gunluk resample + tum veri + tek seferlik ARIMA forecast.
- ARIMA R² = 0.08, LSTM = -0.03, Prophet = 0.03.
- Ufak ilerleme. ARIMA hala kotu cunku 122 gunu tek seferde tahmin etmeye calisiyor.

**Iter 3 (final):** Gunluk + 7-gun yumusatma + ARIMA rolling forecast.
- ARIMA R² = 0.876, LSTM = 0.748, Prophet = 0.015.
- En buyuk sicrama, rolling forecast'a gecisten geldi.

Bu surec rapor ve sunumda ayri bir bolum (Sekil 10).

---

## BOLUM 10: Hocanin Soracagi Sorular ve Cevaplari

### Q: "Persistence baseline neden ekledigniz?"

> "Akademik olarak iyi pratik. Karmasik modelin gercekten degerli olup olmadigini gostermek icin trivial baseline gerekli. Gasparin ve digerleri (2024) gibi son donem makaleleri bunu vurguluyor."

### Q: "ARIMA R²=0.876 cok yuksek gorunuyor, kuskulu degil mi?"

> "Yuksek gorunuyor cunku biz veriyi 7-gun yumusattik ve rolling forecast kullandik. Her tahminden once dunun gercek degerini gormesine izin verdik (teacher forcing). Bu, gercek hayatta uretim ortaminda olusan duruma denk geliyor."

### Q: "Niye sadece 3 hane?"

> "Hesaplama maliyeti. Her hanenin ARIMA rolling forecast'i 10-15 dakika suruyor; 20 hane = 5+ saat. Ucu kucuk ama temsil eden bir ornektir. Gelecek calismalar tum 20 haneyi kapsayabilir."

### Q: "Hava verisi ya da takvim ozellikleri eklemediniz mi?"

> "Hayir, tek degiskenli kurulum tercih ettik. Bunun nedeni adil karsilastirma yapmak. Egzojen ozellikler ekleyince LSTM daha cok faydalanir (cok degiskenli yapidan). Sonraki calismada SARIMAX ve multivariate LSTM denenebilir."

### Q: "Niye gunluk? Saatlik veya 15-dakikalik tahmin daha pratik olmaz miydi?"

> "Saatlikte gurultu cok yuksek, sonuclar negatif R² verdi. Gunluk en istikrarli sonucu uretti. Pratik olarak gunluk-onceki dengesizlik fiyatlandirmasi icin kullanilabilir. Saatlik icin daha buyuk veri seti gerekir."

### Q: "Sonucta hangi modeli kullanalim?"

> "Bizim verimizde Persistence yeterli. ARIMA biraz daha iyi gorunuyor ama istatistiksel olarak fark anlamli degil. LSTM ve Prophet bu veri olcegi icin uygun degil. Eger ham daha yuksek frekansli veri varsa veya egzojen degiskenler eklemek mumkunse derin ogrenme tekrar gundeme gelir."

### Q: "Neden Calibri font kullandiniz?"

> "Okunaklilik. Cogu ITU sablonu Times New Roman onerir ama Calibri sans-serif olarak ekran ve baski okumalarinda daha temizdir. Hocanin acik bir font kisitlamasi olmadigi icin Calibri'yi tercih ettik."

### Q: "Sunum kac dakika surecek?"

> "10-15 dakika hedefliyoruz. 18 slayt. Slayt basi ortalama 45 saniye. Sorulara 5-10 dakika ayrilabilir."

---

## BOLUM 11: Konsantre Notlar (Sunum Sirasinda)

- **Slayt 7 (Persistence):** "Karmasik modelin degerini ispatlamak icin trivial baseline ekledik."
- **Slayt 10 (Rolling vs Multi-step):** "ARIMA ve LSTM dunun gercek degerini her tahminden once gorebiliyor. Prophet ise tek seferde 122 gunluk ufkunu taahhut ediyor."
- **Slayt 14 (DM testi):** "ARIMA, Persistence'i istatistiksel olarak yenmiyor (p=0.665)."
- **Slayt 15 (Cross-house):** "Siralama uc evde de tutarli, bulgu sans degil."
- **Slayt 17 (Discussion):** "ARIMA kazandi ama Persistence ile esdeger. Lag-1 otokorelasyon her seyi yapiyor."

---

## BOLUM 12: Eger Konuyu Hala Anlamadiysan

Su uc sey kafana yerlessin yeter:

1. **"Yarin = bugun" kurali (Persistence) cok guclu cikti.** Hicbir model bunu istatistiksel olarak yenemedi.

2. **ARIMA "kazandi" ama "kazanc" istatistiksel olarak sifir.** Sayi kaginda 0.876 > 0.873, ama testler bunun anlamsiz oldugunu soyluyor.

3. **LSTM ve Prophet zayif, ama bunun nedeni modellerin kotu olmasi degil.** LSTM icin yetersiz veri, Prophet icin yapisal protokol farki suclu.

Ucunden bir tanesini sorulduqunda anlatabilirsen sunumda hicbir problem yasamazsin.

---

## BOLUM 13: Sunum Onunde Bir Saat Once

- **5 dakika sunum gozat:** Hangi slaytta hangi gorsel oldugunu hatirla
- **3 dakika DM testi tekrar:** P-value nedir, ne anlama gelir
- **2 dakika Persistence anlat:** Kendi kelimelerinle "yarin = bugun" kuralinin neyi yaptigini
- **1 dakika nefes:** Gerek yok endiseye, projeniz iyi.

---

Sorularin olursa whatsapp'tan yaz. Yoksa iyi sunumlar.

Iyi calismalar!
