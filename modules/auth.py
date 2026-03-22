from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Company, FinancialYear
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").encode()
        user = User.query.filter_by(username=username, is_active=True).first()
        if user and bcrypt.checkpw(password, user.password_hash.encode()):
            login_user(user)
            company = Company.query.get(user.company_id)
            fy = FinancialYear.query.filter_by(company_id=user.company_id, is_active=True).first()
            session["company_id"]   = user.company_id
            session["company_name"] = company.name if company else ""
            session["fin_year"]     = fy.year_name if fy else "2025-26"
            return redirect(url_for("reports.hub"))
        flash("Invalid username or password", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))

from extensions import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
