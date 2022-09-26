from flask import render_template, request
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

import admin
from config import MyApp
from database import find_by_id, User, save, Company, get_all, Advertisement, delete

app = MyApp.app
database = MyApp.database
babel = MyApp.babel
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return find_by_id(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return login()


@babel.localeselector
def get_locale():
    return "ru"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.find_by_username(username)
        if user and user.check_password(password):
            login_user(user, remember=True)
            return index()
    return render_template("login.html")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        user = User.find_by_username(username)
        if user is None and password == password_again:
            user = User(username=username, fullname=fullname)
            user.set_password(password)
            save(user)
            login_user(user, remember=True)
            return index()
    return render_template("registration.html")


@app.route("/save_company", methods=["POST"])
@login_required
def save_company():
    company_name = request.form.get("company")
    ogrn = request.form.get("OGRN")
    inn = request.form.get("INN")
    address = request.form.get("address")
    director = request.form.get("director")
    company = Company(company_name=company_name, user=current_user, ogrn=ogrn, inn=inn, address=address,
                      director=director)
    save(company)
    return index()


@app.route("/show_my_companies")
@login_required
def show_my_companies():
    companies = database.session.query(Company).filter(Company.user_id == current_user.id).all()
    return render_template("main.html", list_company=companies)


@app.route("/show_link/<company_id>")
def show_link(company_id):
    company = database.session.query(Company).filter(Company.id == int(company_id)).first()
    print(company.company_name, company_id)
    return render_template("link.html", company=company)


@app.route("/advertisement", methods=['POST'])
@login_required
def advertisement():
    company_name = request.form.get("company_name")
    message = request.form.get("message")
    about_company = request.form.get("about_company")
    company_number = request.form.get("company_number")
    advertisement1 = Advertisement(company_name=company_name, message=message, company_number=company_number,
                                   about_company=about_company)
    print(company_name)
    save(advertisement1)
    return index()


@app.route("/delete_advertisement/<advertisement_id>")
@login_required
def delete_advertisement(advertisement_id):
    advertisement = database.session.query(Advertisement).filter(Advertisement.id == int(advertisement_id)).first()
    delete(advertisement)
    return admin_advertisement()


@app.route("/publish_advertisement/<advertisement_id>")
@login_required
def publish_advertisement(advertisement_id):
    advertisement = database.session.query(Advertisement).filter(Advertisement.id == int(advertisement_id)).first()
    advertisement.status = True
    save(advertisement)
    return admin_advertisement()


@app.route("/")
@login_required
def index():
    advertisement = database.session.query(Advertisement).filter(Advertisement.status == True).all()
    print(advertisement)
    if advertisement is None:
        advertisement = False
    return render_template("main.html", list_company=get_all(Company), list_advertisement=advertisement)


@app.route("/admin/12345")
@login_required
def admin_advertisement():
    return render_template("admin.html", list_advertisement=get_all(Advertisement))


if __name__ == '__main__':
    database.create_all()
    admin.config()
    app.run()
