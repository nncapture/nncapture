from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "nncapture_secret_key"

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# UPLOAD
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# ======================
# MODELS
# ======================

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))

# ======================
# STATIC SERVICES
# ======================

services = [
    {
        "icon": "fas fa-user",
        "title": "Portrait & Cosplay",
        "desc": "Sesi portrait personal dan cosplay.",
        "price": "Rp 75.000",
        "unit": "/ jam",
    },
    {
        "icon": "fas fa-running",
        "title": "Sports Photography",
        "desc": "Dokumentasi olahraga profesional.",
        "price": "Mulai Rp 200.000",
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
# ADD TESTIMONIAL
# ======================

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

# ======================
# LOGIN
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":

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
# ======================

@app.route("/add-portfolio", methods=["POST"])
def add_portfolio():

    if not session.get("admin"):
        return redirect("/login")

    title = request.form.get("title")
    category = request.form.get("category")
    description = request.form.get("description")

    image = request.files.get("image")

    filename = ""

    if image:

        filename = secure_filename(image.filename)

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

    new_portfolio = Portfolio(
        title=title,
        category=category,
        description=description,
        image=filename
    )

    db.session.add(new_portfolio)

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

    db.session.delete(portfolio)

    db.session.commit()

    return redirect("/admin")

# ======================
# CREATE DATABASE
# ======================

with app.app_context():
    db.create_all()

# ======================
# RUN
# ======================

if __name__ == "__main__":
    app.run(debug=True)