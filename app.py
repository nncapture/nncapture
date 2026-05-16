from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "nncapture_secret_key")

# ======================
# DATABASE
# ======================

database_url = os.environ.get("DATABASE_URL", "")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# CLOUDINARY
# ======================

cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "dfealk8kj"),
    api_key     = os.environ.get("CLOUDINARY_API_KEY", "148458875545128"),
    api_secret  = os.environ.get("CLOUDINARY_API_SECRET", "jzHCfYa8oBwcwFCZ541rpeXSfDs"),
    secure      = True
)

# ======================
# ALLOWED EXTENSIONS
# ======================

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ======================
# ADMIN CREDENTIALS
# ======================

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# ======================
# MODELS
# ======================

class Testimonial(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)


class Portfolio(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    images = db.relationship(
        'PortfolioImage',
        backref='portfolio',
        lazy=True,
        cascade="all, delete"
    )


class PortfolioImage(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # sekarang simpan URL cloudinary, bukan nama file lokal
    image = db.Column(db.String(500))

    # cloudinary public_id untuk delete
    public_id = db.Column(db.String(300))

    orientation = db.Column(db.String(20), default='landscape')
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))

# ======================
# SERVICES
# ======================

services = [
    {
        "icon": "fas fa-user",
        "title": "Portrait & Cosplay",
        "desc": "Sesi portrait personal dan cosplay.",
        "price": "Rp 40.000",
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
    testimonials = Testimonial.query.order_by(Testimonial.id.desc()).all()
    portfolios = Portfolio.query.order_by(Portfolio.id.desc()).all()
    return render_template(
        "index.html",
        testimonials=testimonials,
        portfolios=portfolios,
        services=services
    )

# ======================
# LOGIN
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
    testimonials = Testimonial.query.order_by(Testimonial.id.desc()).all()
    portfolios = Portfolio.query.order_by(Portfolio.id.desc()).all()
    return render_template("admin.html", testimonials=testimonials, portfolios=portfolios)

# ======================
# ADD TESTIMONIAL
# ======================

@app.route("/add-testimonial", methods=["POST"])
def add_testimonial():
    name = request.form.get("name")
    message = request.form.get("message")
    if not name or not message:
        return redirect("/")
    testimonial = Testimonial(name=name, message=message)
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
# upload ke Cloudinary, simpan URL
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

    portfolio = Portfolio(title=title, category=category, description=description)
    db.session.add(portfolio)
    db.session.commit()

    for file in files:
        if file.filename == "":
            continue
        if not allowed_file(file.filename):
            continue

        try:
            # upload langsung ke Cloudinary dari memory
            result = cloudinary.uploader.upload(
                file,
                folder="nncapture",
                resource_type="image"
            )

            url        = result.get("secure_url")
            public_id  = result.get("public_id")
            width      = result.get("width", 1)
            height     = result.get("height", 1)
            orientation = 'portrait' if height > width else 'landscape'

            image = PortfolioImage(
                image=url,
                public_id=public_id,
                orientation=orientation,
                portfolio_id=portfolio.id
            )
            db.session.add(image)

        except Exception as e:
            print(f"Upload error: {e}")
            continue

    db.session.commit()
    return redirect("/admin")

# ======================
# DELETE PORTFOLIO
# hapus dari Cloudinary juga
# ======================

@app.route("/delete-portfolio/<int:id>")
def delete_portfolio(id):
    if not session.get("admin"):
        return redirect("/login")

    portfolio = Portfolio.query.get_or_404(id)

    for img in portfolio.images:
        if img.public_id:
            try:
                cloudinary.uploader.destroy(img.public_id)
            except Exception as e:
                print(f"Delete error: {e}")

    db.session.delete(portfolio)
    db.session.commit()
    return redirect("/admin")

@app.route("/migrate")
def migrate():
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE portfolio_image ADD COLUMN public_id VARCHAR(300)"))
            conn.execute(db.text("ALTER TABLE portfolio_image ALTER COLUMN image TYPE VARCHAR(500)"))
            conn.commit()
        return "Migrasi berhasil!"
    except Exception as e:
        return f"Error: {e}"

# ======================
# CREATE DATABASE
# ======================

with app.app_context():
    db.create_all()

# ======================
# RUN
# ======================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
