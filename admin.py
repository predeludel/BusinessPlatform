from database import User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import MyApp

app = MyApp.app
database = MyApp.database


def config():
    admin = Admin(app, name='FlaskTemplateApp', template_mode='bootstrap3')
    admin.add_view(ModelView(User, database.session, "Пользователь"))
