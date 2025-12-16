import sys
import cv2
import os
import pyttsx3      # Sesli okuma kütüphanesi
import threading    # Arayüz donmasın diye sesi arka planda okutacağız
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from ultralytics import YOLO

# --- Türkçe Sesli Okuma Fonksiyonu ---
def sesli_soyle(metin):
    def run():
        try:
            engine = pyttsx3.init()
            
            # Bilgisayardaki tüm sesleri al
            voices = engine.getProperty('voices')
            
            # İçinde 'Turkish' veya 'TR' geçen sesi arayıp seç
            found_turkish = False
            for voice in voices:
                if "turkish" in voice.name.lower() or "tr" in voice.id.lower() or "tolga" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    found_turkish = True
                    break
            
            # Eğer Türkçe ses bulamazsa konsola bilgi versin (ama yine de okur)
            if not found_turkish:
                print("Uyarı: Türkçe ses paketi bulunamadı, varsayılan ses kullanılıyor.")

            engine.setProperty('rate', 150) # Hız ayarı
            engine.say(metin)
            engine.runAndWait()
        except Exception as e:
            print(f"Ses hatası: {e}")
            
    # Arayüz donmasın diye arka planda çalıştır
    thread = threading.Thread(target=run)
    thread.start()

class ParaTespitUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLG-407: Görme Engelliler İçin Para Tanıma Sistemi 💸")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        # --- Arayüz Elemanları ---
        self.initUI()
        
        # --- Model Yükleme ---
        # best.pt dosyasının proje klasöründe olduğundan emin olun!
        try:
            # Eğer best.pt yoksa hata vermesin diye kontrol
            if os.path.exists("best.pt"):
                self.model = YOLO("best.pt")
                print("Eğitilmiş model (best.pt) başarıyla yüklendi.")
            else:
                print("UYARI: best.pt bulunamadı, standart yolov8n.pt kullanılıyor.")
                self.model = YOLO("yolov8n.pt")
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Model yüklenemedi!\n{e}")

        self.current_image_path = None
        self.processed_image = None

    def initUI(self):
        # Ana Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # --- Başlık ---
        title = QLabel("YOLOv8 Destekli Para Tanıma Sistemi")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin: 10px;")
        main_layout.addWidget(title)

        # --- Görüntü Panelleri (Yan Yana) ---
        image_layout = QHBoxLayout()

        # Sol Panel (Orijinal)
        self.label_original = QLabel("Orijinal Görüntü")
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setStyleSheet("border: 2px solid #555; background-color: #1e1e1e; font-size: 16px;")
        self.label_original.setFixedSize(550, 500)
        image_layout.addWidget(self.label_original)

        # Sağ Panel (Tespit Edilen)
        self.label_processed = QLabel("Analiz Sonucu")
        self.label_processed.setAlignment(Qt.AlignCenter)
        self.label_processed.setStyleSheet("border: 2px solid #4CAF50; background-color: #1e1e1e; font-size: 16px;")
        self.label_processed.setFixedSize(550, 500)
        image_layout.addWidget(self.label_processed)

        main_layout.addLayout(image_layout)

        # --- Sonuç Metni (Engelsiz Yaşam İçin Bilgilendirme) ---
        self.result_text = QLabel("Sonuç bekleniyor...")
        self.result_text.setAlignment(Qt.AlignCenter)
        self.result_text.setStyleSheet("font-size: 18px; color: #FFC107; font-weight: bold; margin: 5px;")
        main_layout.addWidget(self.result_text)

        # --- Butonlar ---
        button_layout = QHBoxLayout()

        btn_select = QPushButton("📷 Resim Seç")
        btn_select.setStyleSheet(self.get_button_style("#2196F3"))
        btn_select.clicked.connect(self.select_image)
        button_layout.addWidget(btn_select)

        btn_detect = QPushButton("🔍 Parayı Tanı (Analiz)")
        btn_detect.setStyleSheet(self.get_button_style("#4CAF50"))
        btn_detect.clicked.connect(self.detect_objects)
        button_layout.addWidget(btn_detect)

        btn_save = QPushButton("💾 Sonucu Kaydet")
        btn_save.setStyleSheet(self.get_button_style("#FF9800"))
        btn_save.clicked.connect(self.save_image)
        button_layout.addWidget(btn_save)

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: white;
                color: {color};
                border: 2px solid {color};
            }}
        """

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.jpg *.jpeg *.png);;Tüm Dosyalar (*)", options=options)
        if file_path:
            self.current_image_path = file_path
            pixmap = QPixmap(file_path)
            self.label_original.setPixmap(pixmap.scaled(self.label_original.size(), Qt.KeepAspectRatio))
            self.label_processed.setText("Analiz bekleniyor...")
            self.result_text.setText("Görüntü yüklendi, analize hazır.")
            # Resim seçilince de sesli uyarı verelim
            sesli_soyle("Görüntü yüklendi.")

    def detect_objects(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim seçin!")
            sesli_soyle("Lütfen önce bir resim seçin.")
            return

        # YOLO ile Tahmin Yap
        results = self.model(self.current_image_path)
        result = results[0]
        
        # Sonuç görselini al (OpenCV formatında gelir - BGR)
        img_bgr = result.plot() 
        self.processed_image = img_bgr 

        # OpenCV (BGR) -> Qt (RGB) dönüşümü
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Ekrana bas
        self.label_processed.setPixmap(QPixmap.fromImage(qt_img).scaled(self.label_processed.size(), Qt.KeepAspectRatio))

        # --- SESLİ VE YAZILI RAPORLAMA ---
        # Tespit edilen sınıfları listele
        detected_classes = [result.names[cls] for cls in result.boxes.cls.tolist()]
        
        ozet_listesi = []
        kagit_sayisi = detected_classes.count("kagit_para")
        bozuk_sayisi = detected_classes.count("bozuk_para")

        if kagit_sayisi > 0:
            ozet_listesi.append(f"{kagit_sayisi} Adet Kağıt Para")
        if bozuk_sayisi > 0:
            ozet_listesi.append(f"{bozuk_sayisi} Adet Bozuk Para")
            
        # Sonuç Metnini Oluştur
        if not ozet_listesi:
            final_text = "Para tespit edilemedi."
            sesli_mesaj = "Maalesef, görüntüde para tespit edemedim."
        else:
            ozet_metni = ", ".join(ozet_listesi)
            final_text = f"TESPİT: {ozet_metni} bulundu."
            sesli_mesaj = f"Görselde, {ozet_metni} tespit edildi."
            
        # Ekrana Yaz ve Sesli Söyle
        self.result_text.setText(final_text)
        sesli_soyle(sesli_mesaj)

    def save_image(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek analiz sonucu yok!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "sonuc.jpg", "Resim Dosyaları (*.jpg *.png)")
        if file_path:
            cv2.imwrite(file_path, self.processed_image)
            QMessageBox.information(self, "Başarılı", "Görüntü başarıyla kaydedildi.")
            sesli_soyle("Sonuç başarıyla kaydedildi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParaTespitUygulamasi()
    window.show()
    sys.exit(app.exec_())