# 💸 Görme Engelliler İçin Yapay Zeka Destekli Para Tanıma Asistanı

Bu proje, **BLG-407 Makine Öğrenmesi** dersi kapsamında geliştirilmiştir. Görme engelli bireylerin günlük yaşamda kağıt ve bozuk paraları ayırt etmelerini kolaylaştırmak amacıyla **YOLOv8** tabanlı nesne tespiti ve **Sesli Geri Bildirim** teknolojileri kullanılmıştır.

## 🎯 Proje Özellikleri
* **Gerçek Zamanlı Tespit:** Fotoğraftaki paraları yüksek doğrulukla (%99 mAP) tespit eder.
* **Sesli Asistan:** Tespit edilen paraları Türkçe olarak sesli okur (Örn: *"Görselde 2 adet kağıt para tespit edildi"*).
* **Kullanıcı Dostu Arayüz:** PyQt5 ile geliştirilmiş basit ve anlaşılır masaüstü uygulaması.

## 🛠️ Kullanılan Teknolojiler
* **Model:** YOLOv8 Nano (Transfer Learning ile eğitilmiştir)
* **Veri Seti:** 400+ Görüntü (Özgün çekim ve Augmentation)
* **Arayüz:** Python & PyQt5
* **Ses Sentezi:** pyttsx3 (Offline çalışır)

## 📂 Kurulum ve Çalıştırma

1.  Projeyi indirin:
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ.git](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ.git)
    cd REPO_ADINIZ
    ```

2.  Gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    ```

3.  Uygulamayı başlatın:
    ```bash
    python gui_app.py
    ```

## 📊 Eğitim Sonuçları
Eğitim Google Colab üzerinde GPU desteği ile 50 Epoch boyunca sürdürülmüştür.
* **mAP50 Skoru:** 0.99
* **Loss:** Düzenli düşüş eğilimi göstermiştir.
*(Detaylı eğitim grafikleri ve kodları `.ipynb` dosyasında mevcuttur.)*

