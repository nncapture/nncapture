from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "nncapture_secret_key")

# ======================
# DATABASE
# ======================

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# UPLOAD FOLDER
# ======================

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ======================
# ALLOWED EXTENSIONS
# FIX: hanya gambar yang boleh diupload
# ======================

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ======================
# ADMIN CREDENTIALS
# FIX: ambil dari environment variable, fallback ke default
# Ganti via: export ADMIN_USERNAME=xxx ADMIN_PASSWORD=xxx
# ======================

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# ======================
# MODELS
# ======================

class Testimonial(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )


class Portfolio(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    category = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    images = db.relationship(
        'PortfolioImage',
        backref='portfolio',
        lazy=True,
        cascade="all, delete"
    )


class PortfolioImage(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    image = db.Column(
        db.String(300)
    )

    # FIX: tambah kolom orientation supaya portrait/landscape jalan di HTML
    orientation = db.Column(
        db.String(20),
        default='landscape'
    )

    portfolio_id = db.Column(
        db.Integer,
        db.ForeignKey('portfolio.id')
    )

# ======================
# SERVICES
# ======================

services = [

    {
        "icon": "fas fa-user",
        "title": "Portrait & Cosplay",
        "desc": "Sesi portrait personal dan cosplay.",
        "price": "Rp 50.000",
        "unit": "/ jam",
    },

    {
        "icon": "fas fa-id-card",
        "title": "Headshot",
        "desc": "Foto headshot profesional.",
        "price": "Rp 30.000",
        "unit": "/ orang",
    },

    {
        "icon": "fas fa-running",
        "title": "Sports Photography",
        "desc": "Dokumentasi olahraga profesional.",
        "price": "Mulai Rp 150.000",
        "unit": "/ sesi",
    },

    {
        "icon": "fas fa-camera",
        "title": "Event Documentation",
        "desc": "Dokumentasi acara dan event.",
        "price": "Mulai Rp 300.000",
        "unit": "/ sesi",
    },

]

# ======================
# HOME
# ======================

@app.route("/")
def index():

    testimonials = Testimonial.query.order_by(
        Testimonial.id.desc()
    ).all()

    portfolios = Portfolio.query.order_by(
        Portfolio.id.desc()
    ).all()

    return render_template(
        "index.html",
        testimonials=testimonials,
        portfolios=portfolios,
        services=services
    )

# ======================
# LOGIN
# FIX: pakai variabel dari env bukan hardcoded
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

    return render_template("login.html")

# ======================
# LOGOUT
# ======================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ======================
# ADMIN PANEL
# ======================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    testimonials = Testimonial.query.order_by(
        Testimonial.id.desc()
    ).all()

    portfolios = Portfolio.query.order_by(
        Portfolio.id.desc()
    ).all()

    return render_template(
        "admin.html",
        testimonials=testimonials,
        portfolios=portfolios
    )

# ======================
# ADD TESTIMONIAL
# ======================

@app.route("/add-testimonial", methods=["POST"])
def add_testimonial():

    name = request.form.get("name")
    message = request.form.get("message")

    if not name or not message:
        return redirect("/")

    testimonial = Testimonial(
        name=name,
        message=message
    )

    db.session.add(testimonial)

    db.session.commit()

    return redirect("/#testimonials")

# ======================
# DELETE TESTIMONIAL
# ======================

@app.route("/delete-testimonial/<int:id>")
def delete_testimonial(id):

    if not session.get("admin"):
        return redirect("/login")

    testimonial = Testimonial.query.get_or_404(id)

    db.session.delete(testimonial)

    db.session.commit()

    return redirect("/admin")

# ======================
# ADD PORTFOLIO
# FIX: validasi ekstensi + deteksi orientasi otomatis
# ======================

@app.route("/add-portfolio", methods=["POST"])
def add_portfolio():

    if not session.get("admin"):
        return redirect("/login")

    title = request.form.get("title")
    category = request.form.get("category")
    description = request.form.get("description")

    files = request.files.getlist("images")

    if not title or not files:
        return redirect("/admin")

    # CREATE PORTFOLIO
    portfolio = Portfolio(
        title=title,
        category=category,
        description=description
    )

    db.session.add(portfolio)

    db.session.commit()

    # SAVE MULTIPLE IMAGES
    for file in files:

        if file.filename == "":
            continue

        # FIX: tolak file yang bukan gambar
        if not allowed_file(file.filename):
            continue

        ext = file.filename.rsplit('.', 1)[1].lower()

        # FIX: pakai uuid supaya nama file ga bentrok
        filename = f"{uuid.uuid4().hex}.{ext}"

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        file.save(filepath)

        # FIX: deteksi orientasi dari dimensi gambar
        try:
            with Image.open(filepath) as img:
                w, h = img.size
                orientation = 'portrait' if h > w else 'landscape'
        except Exception:
            orientation = 'landscape'

        image = PortfolioImage(
            image=filename,
            orientation=orientation,
            portfolio_id=portfolio.id
        )

        db.session.add(image)

    db.session.commit()

    return redirect("/admin")

# ======================
# DELETE PORTFOLIO
# ======================

@app.route("/delete-portfolio/<int:id>")
def delete_portfolio(id):

    if not session.get("admin"):
        return redirect("/login")

    portfolio = Portfolio.query.get_or_404(id)

    # DELETE IMAGE FILES
    for img in portfolio.images:

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            img.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(portfolio)

    db.session.commit()

    return redirect("/admin")

# ======================
# CREATE DATABASE + MIGRATE
# ======================

with app.app_context():
    db.create_all()
    # Auto migrasi kolom orientation kalau belum ada
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE portfolio_image ADD COLUMN orientation VARCHAR(20) DEFAULT 'landscape'"))
            conn.commit()
    except Exception:
        pass  # kolom sudah ada, skip

# ======================
# RUN
# ======================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
