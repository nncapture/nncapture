# N&N Capture — Website

## Cara Menjalankan

### 1. Install Python (kalau belum ada)
Download di https://python.org

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Jalankan website
```
python app.py
```

Buka browser, ketik: **http://localhost:5000**

---

## Cara Tambah Foto Portfolio

Taruh foto di folder sesuai kategori:
```
static/images/portrait/   ← foto portrait & cosplay
static/images/headshot/   ← foto headshot
static/images/sports/     ← foto sports
static/images/event/      ← foto event
```

Lalu buka **app.py**, di bagian `portfolio`, ganti nama file sesuai foto kamu.
Contoh:
```python
{"file": "portrait/foto-cosplay-1.jpg", "title": "Cosplay Session", "desc": "..."},
```

## Foto Profil
Taruh foto profil di:
```
static/images/profile.jpg
```

---

## Struktur Folder
```
nncapture/
├── app.py               ← file utama Python/Flask
├── requirements.txt     ← daftar library
├── templates/
│   └── index.html       ← halaman web
└── static/
    ├── css/style.css    ← tampilan/desain
    ├── js/main.js       ← interaksi (filter, form, dsb)
    └── images/          ← taruh semua foto di sini
```
