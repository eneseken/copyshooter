# CopyShooter 📋

> Ekranda bir alan seç, yazıyı anında panoya kopyala.

![Banner](banner.png)

---

## Ne yapar?

Ekranın herhangi bir bölümünü seçince içindeki metni OCR ile okuyup otomatik olarak **Ctrl+V** ile yapıştırılabilir hale getirir.

- Sistem tepsisinde arka planda çalışır
- **Ctrl+Y** ile anında alan seçimi başlar
- Metin kopyalandığında sağ alt köşede bildirim çıkar
- Windows başlangıcına eklenebilir (tepsi menüsünden)

---

## Kurulum

### 1. Gereksinimler

- Python 3.8+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) — `C:\Program Files\Tesseract-OCR\` yoluna kur, kurulum sırasında **Turkish** dil paketini seç

### 2. Kütüphaneleri kur

```bat
kur.bat
```

### 3. Çalıştır

```bat
python app.py
```

---

## EXE Derleme

```bat
build.bat
```

Masaüstüne `SS Kopyala` klasörü oluşur. İçindeki `SS Kopyala.exe` dosyasını çalıştır.

> **Not:** Antivirus yazılımı PyInstaller exe'lerini yanlışlıkla tehdit olarak işaretleyebilir. Bu bir false positive'dir — uygulamayı antivirus istisnalarına ekle.

---

## Kullanım

| Eylem | Kısayol |
|-------|---------|
| Alan seç | `Ctrl+Y` |
| Çıkış | Tepsi → Çıkış |
| Başlangıca ekle/kaldır | Tepsi → Başlangıca Ekle |

---

## Teknolojiler

- [Python](https://python.org)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Pillow](https://python-pillow.org)
- [pystray](https://github.com/moses-palmer/pystray)
- [keyboard](https://github.com/boppreh/keyboard)

---

## Lisans

MIT
