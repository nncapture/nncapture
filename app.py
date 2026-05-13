from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testimonials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODEL TESTIMONIAL
class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

# PORTFOLIO
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

# SERVICES
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

# HOME
@app.route("/")
def index():

    testimonials = Testimonial.query.order_by(
        Testimonial.id.desc()
    ).all()

    return render_template(
        "index.html",
        portfolio=portfolio,
        services=services,
        testimonials=testimonials,
    )

# ADD TESTIMONIAL
@app.route("/add-testimonial", methods=["POST"])
def add_testimonial():

    name = request.form.get("name")
    message = request.form.get("message")

    if not name or not message:
        return redirect("/")

    new_testimonial = Testimonial(
        name=name,
        message=message
    )

    db.session.add(new_testimonial)

    db.session.commit()

    return redirect("/#testimonials")

# DELETE TESTIMONIAL
@app.route("/delete-testimonial/<int:id>")
def delete_testimonial(id):

    testimonial = Testimonial.query.get_or_404(id)

    db.session.delete(testimonial)

    db.session.commit()

    return redirect("/#testimonials")

# CREATE DATABASE
with app.app_context():
    db.create_all()

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)