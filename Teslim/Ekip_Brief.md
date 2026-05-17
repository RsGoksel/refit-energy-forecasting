# Ekip Brief, Sade Anlatim

Selam ekip,

Proje bitti, ekip olarak ne yaptik, neyi bulduk, nereye geldik kisaca yaziyorum. Resmi olmayan dilde, kahve esliginde okunsun diye.

## Konu Neydi?

Hocanin verdigi yon: **Yapay Zeka + Enerji Sistemleri**. Bizim sectiğimiz problem:

> Tek bir evin gunluk elektrik tuketimini onceden tahmin etmek. Hangi yontem en iyi calisiyor?

Yani bir akilli sayac evde takili, 24 saat veri akiyor. Yarinki tuketimi bugun bilebilir miyiz? Eger bilebilirsek **demand response** programlari, **batarya optimizasyonu**, **catı PV self-consumption** gibi seyler mumkun.

## Veri Seti

**REFIT** diye bir aciq kaynak veri seti kullandik. Birleşik Krallik Loughborough'da 20 evden 2 yil boyunca elektrik olcumleri toplamislar. Her ev icin:
- 1 tane toplam sayac
- 9 tane cihaz monitoru (buzdolabi, camasir makinesi, vs.)
- Her 8 saniyede bir watt cinsinden okuma

Toplam yaklasik 1.2 milyar satir veri. Biz sade Ev 1, Ev 2 ve Ev 5'i sectik (cross-house validation icin).

## Ne Yaptik?

Aslen makaledeki uc modeli kiyaslayacaktik: **ARIMA, LSTM, FB-Prophet**. Sonra hocadan korkup bir de **Persistence** (yarini bugun gibi tahmin et) baseline ekledik. Bu cok onemli bir tasarim karari oldu, gercegen.

**Pipeline:**
1. Ham 8 saniye veri (yaklasik 5.7 milyon satir Ev 2 icin)
2. Aykiri deger temizleme (negatif degerler, p99 ustu)
3. Gunluk ortalama (5.7M -> ~630 gun)
4. 7 gunluk hareketli ortalama (gurultuyi yumusatmak icin)
5. %80 egitim, %20 test bolme
6. 4 model calistir
7. Diebold-Mariano testi ile istatistiksel anlamlilik

## Ne Bulduk?

### Headline Sonucu

| Model | Ev 1 R² | Ev 2 R² | Ev 5 R² |
|-------|--------:|--------:|--------:|
| Persistence (baseline) | 0.963 | 0.873 | 0.901 |
| **ARIMA(2,1,2)** | **0.976** | **0.876** | **0.905** |
| LSTM (3-katmanli) | 0.859 | 0.748 | 0.647 |
| FB-Prophet | -2.315 | 0.015 | -1.186 |

**ARIMA uc evde de "kazandi"** ama dikkat: persistence ile farki kil pasi.

### Kritik Bulgu

Diebold-Mariano testini calistirinca ortaya cikti:

> **ARIMA, Persistence'i istatistiksel olarak yenmiyor (p = 0.665).**

Yani "ARIMA en iyi" diyebiliyoruz ama gercekte yarini bugun gibi tahmin etmekten farki yok. Lag-1 otokorelasyonu cok guclu, butun isi o yapiyor.

**LSTM ve Prophet ise Persistence'a anlamli olarak KAYBEDIYOR** (p < 0.001). Yani 129 bin parametreli sinir agi, tek satirlik kuraldan daha kotu!

### Pratik Yorum

ARIMA hatasi (Ev 2): RMSE = 48.7 W = ortalama tuketimin %11.2'si = yaklasik 1.17 kWh/gun. UK 2025 fiyatlariyla yaklasik 0.32 GBP/gun fatura hatasi, ayda 10 GBP civari.

## Yol Boyunca Yaptiqlarimiz

1. **Veriyi Kaggle'dan indirdik**, House_2.csv'yi cikardik (300 MB)
2. Pipeline kodu yazdik (`energy_forecasting.py`), seed=42 sabit
3. Ilk denemede R²=-0.13 falan cikti, panikledik :)
4. Iterasyonlar:
   - Iter 1: Saatlik resample, 3 ay veri -> kotu
   - Iter 2: Gunluk resample, tum veri -> orta
   - Iter 3: Gunluk + 7-gun yumusatma + rolling forecast -> ARIMA R²=0.876
5. Sonra "ama baseline yok" elestirisi gelince Persistence ekledik
6. "Istatistiksel test yok" elestirisi gelince DM testi ekledik
7. "Tek hane yetersiz" elestirisi gelince Ev 1 ve Ev 5'i de cektik
8. Tum dosyalari Calibri font, 2cm margin ile gunyel hale getirdik
9. GitHub'a public push ettik

## Teslim Edecegimiz Dosyalar (Teslim/ klasoru icinde)

| Dosya | Ne icin? |
|-------|----------|
| EBT629E_Final_Project_Report_TR.pdf | Final rapor Turkce, 15 sayfa |
| EBT629E_Final_Project_Report.pdf | Final rapor Ingilizce, 15 sayfa |
| EBT629E_Project_Presentation.pptx | Sunum, 18 slayt |
| EBT629E_Literature_Review.docx | Lit review (20 Nisan'da teslim ettik, 100 aldik) |
| EBT629E_Project_Proposal.docx | 6 Nisan teslim |
| README.md | GitHub'da gorulen kapak |

GitHub: https://github.com/RsGoksel/refit-energy-forecasting

## Sunum Sirasinda

15 dakikalik sunum tahmininde su slaytlar **kritik**:

- **Slayt 7 (Persistence):** "Neden basit baseline kullandik?" sorusunun cevabi
- **Slayt 10 (Rolling vs Multi-step):** Prophet'in dusuk skorunu aciklayan slayt
- **Slayt 14 (Diebold-Mariano):** Hocanin "istatistiksel testin var mi?" sorusunun cevabi
- **Slayt 15 (Cross-house):** Hocanin "tek hane mi?" sorusunun cevabi

## Olasi Sorular ve Hazir Cevaplarimiz

**Soru:** Niye Prophet bu kadar dusuk?  
**Cevap:** Rolling vs multi-step protokol farki (Slayt 10). Ayrica gunluk konut verisi Prophet'in odaklandigi mevsimsellik degil, lag-1 ile domine ediliyor.

**Soru:** LSTM neden bu kadar zayif?  
**Cevap:** 490 egitim gunu ve 14-gun lookback ile 476 dizi. 129 bin parametreli ag icin veri yetmez. Gasparin ve digerleri (2024) ayni buldu: 6 aydan kisa veride basit modeller deep learning'i yener.

**Soru:** Baseline ne icin?  
**Cevap:** Karmasik bir modelin gercekten faydali olup olmadigini gostermenin tek yolu. ARIMA bile bizdeki gibi Persistence'i yenemiyorsa, kompleks modelin orada degeri yok demektir.

**Soru:** Tek hane mi calistiniz?  
**Cevap:** Hayir, uc hane: Ev 1, Ev 2, Ev 5. Siralama uc evde de ayni (ARIMA ~ Persistence > LSTM > Prophet). Cross-house validation grafigi 15. slaytta.

**Soru:** Hangi yeni katki yaptiniz?  
**Cevap:** Buluc et al. (2025) makalesi tek istasyon ile ARIMA/LSTM/Prophet kiyasi yapmis. Biz onun ustune:
1. Persistence baseline ekledik
2. Diebold-Mariano testi ekledik
3. Cross-house validation yaptik
4. Pratik maliyet yorumu cikardik

## Notlar / Ipuclari

- Sunum sirasinda *italik* ve **kalin** kullanmaya gerek yok, butun slaytlar zaten okunakli
- Slayt 10 (rolling vs multi-step) en cok soru gelecek slayt, ekstra hazirlikli ol
- Tablolarda **R² sayilari koyu**, hoca renge bakmadan goruyor olmali
- Github linkini sunum sonunda paylas: `github.com/RsGoksel/refit-energy-forecasting`

---

Sorun olursa whatsapp'tan yaz, ben her zaman uygunum.

Iyi sunumlar, ekip!
