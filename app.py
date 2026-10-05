import os
from datetime import datetime, timezone
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-this")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///site.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(30))
    business = db.Column(db.String(160))
    service = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.String(80))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="New", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


PROJECTS = [
    {
        "title": "AI Portfolio Chatbot",
        "category": "AI / Web App",
        "description": "A Flask-based chatbot project with conversational UI, theme controls and chat history concepts.",
        "tech": "Python · Flask · AI",
        "url": "https://github.com/vijay-kumar-vangala/chatbot-by-vijay",
        "label": "GitHub",
    },
    {
        "title": "Loan Risk Analysis",
        "category": "Data / ML",
        "description": "A data-driven loan risk analysis project focused on default prediction, model evaluation and business insights.",
        "tech": "Python · SQL · ML · Streamlit",
        "url": "",
        "label": "Case Study",
    },
    {
        "title": "Employee Attrition Analysis",
        "category": "Analytics",
        "description": "An analytics project exploring employee attrition patterns through data analysis and an interactive dashboard.",
        "tech": "Python · Power BI · Data Viz",
        "url": "",
        "label": "Case Study",
    },
    {
        "title": "Cyber Attack Detection",
        "category": "Machine Learning",
        "description": "A machine-learning project comparing multiple classification approaches for cyber attack detection.",
        "tech": "Python · ML · Django",
        "url": "",
        "label": "Case Study",
    },
    {
        "title": "Phishing Detection with LLM",
        "category": "AI / Security",
        "description": "An AI-focused phishing detection concept using language-model embeddings and a web interface.",
        "tech": "Python · NLP · Streamlit",
        "url": "",
        "label": "Case Study",
    },
    {
        "title": "Job Tracker",
        "category": "Web Application",
        "description": "A Flask application concept for tracking job applications and organizing recruitment workflow information.",
        "tech": "Python · Flask · SQL",
        "url": "",
        "label": "Case Study",
    },
]

SERVICES = [
    ("Business Websites", "Modern, responsive websites designed to help local businesses build trust and generate enquiries."),
    ("Portfolio Websites", "Clean personal and professional portfolios that showcase skills, work and achievements."),
    ("Web Applications", "Custom Flask-powered applications with forms, databases, authentication and business workflows."),
    ("AI & Automation", "Practical AI and automation solutions for repetitive tasks, data workflows and business ideas."),
    ("Data & Dashboards", "Interactive data solutions and dashboards that turn business data into useful insights."),
    ("Website Support", "Updates, improvements, bug fixes and ongoing technical support after launch."),
]


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_site_data():
    return {
        "brand": "VYB Labs",
        "email": "vyblabs1@gmail.com",
        "phone": "9121898283",
        "location": "Hyderabad, Telangana",
        "portfolio_url": "https://vijay-kumar-vangala.github.io/personal-portfolio/",
        "github_url": "https://github.com/vijay-kumar-vangala",
        "linkedin_url": "",
        "whatsapp_url": "https://wa.me/919121898283",
        "year": datetime.now().year,
    }


@app.route("/")
def home():
    return render_template("index.html", projects=PROJECTS[:3])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)


@app.route("/portfolio")
def portfolio():
    return redirect("https://vijay-kumar-vangala.github.io/personal-portfolio/")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        business = request.form.get("business", "").strip()
        service = request.form.get("service", "").strip()
        budget = request.form.get("budget", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not service or not message:
            flash("Please fill in all required fields.", "error")
            return render_template("contact.html")

        inquiry = Inquiry(
            name=name,
            email=email,
            phone=phone,
            business=business,
            service=service,
            budget=budget,
            message=message,
        )
        db.session.add(inquiry)
        db.session.commit()
        flash("Thanks! Your enquiry has been received. VYB Labs will get back to you soon.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        configured_password = os.getenv("ADMIN_PASSWORD", "")
        if configured_password and request.form.get("password") == configured_password:
            session["admin_logged_in"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash("Invalid admin password.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template("admin.html", inquiries=inquiries)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
