from flask import Flask, render_template
import os

app = Flask(__name__)

portfolio = {
    "portrait": [
        {"file": "portrait/foto1.jpg", "title": "Portrait Session", "desc": "Personal & Cosplay"},
        {"file": "portrait/foto2.jpg", "title": "Character Portrait", "desc": "Cosplay Photography"},
        {"file": "portrait/foto3.jpg", "title": "Lifestyle Portrait", "desc": "Personal Branding"},
    ],
    "headshot": [
        {"file": "headshot/foto1.jpg", "title": "Headshot Profesional", "desc": "Untuk Flyer & Poster"},
        {"file": "headshot/foto2.jpg", "title": "Team Headshot", "desc": "Dokumentasi Tim"},
        {"file": "headshot/foto3.jpg", "title": "Individual Headshot", "desc": "Keperluan Promosi"},
    ],
    "sports": [
        {"file": "sports/foto1.jpg", "title": "Action Shot", "desc": "Sports Photography"},
        {"file": "sports/foto2.jpg", "title": "Team Documentation", "desc": "Foto Tim Olahraga"},
        {"file": "sports/foto3.jpg", "title": "Tournament Moment", "desc": "Dokumentasi Turnamen"},
    ],
    "event": [
        {"file": "event/foto1.jpg", "title": "Event Documentation", "desc": "Seminar & Gathering"},
        {"file": "event/foto2.jpg", "title": "Community Event", "desc": "Acara Komunitas"},
        {"file": "event/foto3.jpg", "title": "Corporate Event", "desc": "Acara Perusahaan"},
    ],
}

services = [
    {
        "icon": "fas fa-user",
        "title": "Portrait & Cosplay",
        "desc": "Sesi portrait personal, cosplay, dan lifestyle. Setiap momen diabadikan dengan pencahayaan dan angle terbaik.",
        "price": "Rp 75.000",
        "unit": "/ 1 jam",
    },
    {
        "icon": "fas fa-id-card",
        "title": "Headshot Individu",
        "desc": "Foto headshot profesional untuk kebutuhan flyer, poster, dan promosi tim. Minimum 5 orang.",
        "price": "Rp 30.000",
        "unit": "/ orang",
    },
    {
        "icon": "fas fa-running",
        "title": "Sports Photography",
        "desc": "Dokumentasi aksi olahraga, turnamen, dan foto tim lengkap. Cocok untuk futsal, basket, badminton.",
        "price": "Mulai Rp 200.000",
        "unit": "/ sesi",
    },
    {
        "icon": "fas fa-camera",
        "title": "Event & Dokumentasi",
        "desc": "Liputan event seminar, gathering, dan acara komunitas. Tersedia paket half day dan full day.",
        "price": "Mulai Rp 300.000",
        "unit": "/ sesi",
    },
]

testimonials = [
    {
        "name": "Rizky A.",
        "role": "Ketua Komunitas Cosplay Lampung",
        "text": "Hasil fotonya luar biasa! Paham banget cara mengambil angle yang pas untuk kostum cosplay. Sudah beberapa kali pakai jasa N&N Capture dan selalu puas.",
    },
    {
        "name": "Coach Hendra",
        "role": "Pelatih Tim Futsal",
        "text": "Dokumentasi turnamen kami jadi jauh lebih profesional. Foto aksi pemain ditangkap dengan sempurna, timing-nya tepat banget.",
    },
    {
        "name": "Panitia Event BEM",
        "role": "Universitas Lampung",
        "text": "Responsif, tepat waktu, dan hasil foto berkualitas tinggi. Sangat direkomendasikan untuk dokumentasi event kampus.",
    },
]

@app.route("/")
def index():
    return render_template(
        "index.html",
        portfolio=portfolio,
        services=services,
        testimonials=testimonials,
    )

if __name__ == "__main__":
    app.run(debug=True)
