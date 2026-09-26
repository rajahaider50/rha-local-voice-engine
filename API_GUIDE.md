# RHA Voice Engine: Python Server & Android App Connection

جب آپ موبائل پر بھاری AI ماڈلز (LLM, STT) کو براہ راست Android Native (Chaquopy) کے ذریعے چلاتے ہیں، تو اکثر RAM کم ہونے کی وجہ سے ایپ کریش ہو سکتی ہے یا ماڈلز لوڈ ہونے میں منٹوں کا وقت لگ سکتا ہے۔ 

اس کا سب سے بہترین حل **Local Client-Server Architecture** ہے۔ یعنی:
1. آپ Termux میں Python کا `FastAPI` سرور رن کرتے ہیں۔
2. آپ کی خوبصورت Android ایپ (APK) مائیکرو فون سے آواز ریکارڈ کر کے سیکنڈز میں اس سرور کو بھیجتی ہے۔
3. سرور پراسیس کر کے جواب واپس ایپ پر دکھاتا ہے۔

یہاں تک کہ اگر آپ چاہیں تو Python سرور اپنے لیپ ٹاپ پر چلا کر موبائل ایپ کو اسی وائی فائی (Wi-Fi) پر کنیکٹ کر سکتے ہیں!

---

## 🚀 سرور کو سٹارٹ کیسے کریں؟

### طریقہ 1: Termux (موبائل کے اندر)
1. Termux کھولیں۔
2. `cd rha-local-voice-engine`
3. `source venv/bin/activate`
4. سرور چلانے کے لیے یہ کمانڈ دیں:
   ```bash
   python api/server.py
   ```
5. آپ کو میسج آئے گا: `Uvicorn running on http://0.0.0.0:8000`

### طریقہ 2: Laptop/PC کے ذریعے
اگر آپ کا موبائل سلو ہے، تو آپ یہی پروجیکٹ اپنے لیپ ٹاپ پر کلون کر کے سرور چلا سکتے ہیں:
```bash
pip install -r requirements.txt
python api/server.py
```
*(نوٹ: اپنے لیپ ٹاپ کا IP Address نوٹ کر لیں۔ مثلاً `192.168.1.5`)*

---

## 📱 Android App کو سرور سے کیسے کنیکٹ کریں؟

میں نے آپ کی Android ایپ کے اندر ایک جدید **Network Bridge** شامل کر دیا ہے۔

جب آپ اپنا Android App اوپن کریں گے:
1. اگر آپ نے Python سرور **Termux** میں چلایا ہے، تو ایپ خود بخود `http://localhost:8000` کے ذریعے اس سے جڑ جائے گی۔
2. جب آپ **"START ENGINE"** کا بٹن دبائیں گے، تو ایپ آپ کی آواز ریکارڈ کرے گی، اور سیدھا Python سرور کے `/api/v1/voice` اینڈپوائنٹ (Endpoint) پر بھیج دے گی۔
3. سرور آپ کی آواز کو ٹیکسٹ میں بدلے گا (Whisper)، آپ کی بات کا مطلب سمجھے گا (Intent Engine)، اور Qwen AI سے جواب تیار کر کے ایپ پر بھیج دے گا۔

### ایپ کو اپڈیٹ کرنے کا طریقہ:
میں نے GitHub پر نیا کوڈ پش کر دیا ہے جس میں Retrofit Network اور Audio Recorder کی مکمل Kotlin Integration موجود ہے۔
GitHub Actions آپ کا نیا APK تیار کر رہا ہے جو سیدھا Python سرور سے بات کرے گا!
