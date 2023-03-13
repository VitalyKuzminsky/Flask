from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from blog.extensions import migrate, csrf, db

# from blog.article.views import article
# from blog.auth.views import auth
# from blog.report.views import report
# from blog.user.views import user

# db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:  # Принимает ничего. Возвращает Flask-объект.
    """Создаёт экземпляр аппки и возвращает его - фабрика по созданию приложений"""
    app = Flask(__name__)  # Создаётся экземпляр приложения
    # app.config.from_pyfile('config.cfg')
    app.config['SECRET_KEY'] = '&5kkn1@hu(i_u!v=q!53_zpl7i+_+yo976py1r*@o&-@go_=*w'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Путь к БД
    app.config['WTF_CSRF_ENABLED'] = True

    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'  # Вьюха для авторизации
    login_manager.init_app(app)  # Инициализируем приложение

    from .models import User  # так сделал проподаватель, но не смог объяснить, почему без этого не работало

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # @login_manager.unauthorized_handler
    # def unauthorized():
    #     return redirect(url_for('auth.login'))

    register_blueprints(app)  # экземпляр приложения передаётся в функцию регистрации blueprint
    return app


def register_blueprints(app: Flask):  # Регистрация blueprint в приложении. Принимает в себя экземпляр приложения Flask
    from blog.article.views import article
    from blog.auth.views import auth
    from blog.report.views import report
    from blog.user.views import user
    from blog.author.views import author

    app.register_blueprint(user)  # Принимает в себя blueprint с приложением user
    app.register_blueprint(report)  # Принимает в себя blueprint с приложением report
    app.register_blueprint(article)  # Принимает в себя blueprint с приложением report
    app.register_blueprint(auth)  # Принимает в себя blueprint с приложением auth
    app.register_blueprint(author)  # Принимает в себя blueprint с приложением author


# Ниже код первого урока:
# from time import time
#
# from flask import Flask, request, g
# from werkzeug.exceptions import BadRequest
#
# app = Flask(__name__)  # Создаём экземпляр нашего приложения app. __name__ - название модуля в котором работаем.
#
#
# @app.route('/')  # Чтобы ф-ия работала через / - добавляем сюда этот декоратор. Т.е. мы зарегистрировали на route/
# # выполнение index
# def index():
#     return 'Hello!'
#
#
# @app.route("/greet/<name>/")  # Ссылка с приветствием по имени, которое нужно будет вписать в путь.
# def greet_name(name: str):
#     return f"Hello {name}!"
#
#
# @app.route("/user/")
# def read_user():
#     """Для обработки параметров query string необходимо использовать объект request. Создадим новый
#     view. Для обращения к query string необходимо использовать request.args. Мы используем .get,
#     потому что с request.args нужно обращаться как со словарём."""
#     name = request.args.get("name")
#     surname = request.args.get("surname")
#     return f"User {name or '[no name]'} {surname or '[no surname]'}"
#
#
# @app.route("/status/", methods=["GET", "POST"])
# def custom_status_code():
#     """Регистрируем новый view. Необходимо указать допустимые методы через именованную переменную
#     methods. Через request.method проверяем, что метод GET. Если так, возвращаем инструкцию, как
#     пользоваться данным endpoint. Если же метод POST, то выполняем обработку данных. Сначала
#     проверяем request.form, а затем request.json. В обоих случаях работаем с объектом как со
#     словарём. Проверяем наличие ключа code, и если он там присутствует, отдаём ответ с таким кодом.
#     По умолчанию отдаём пустой ответ с кодом 204."""
#     if request.method == "GET":
#         return """\
#         To get response with custom status code
#         send request using POST method
#         and pass `code` in JSON body / FormData
#         """
#
#     print("raw bytes data:", request.data)
#
#     if request.form and "code" in request.form:
#         return "code from form", request.form["code"]
#
#     if request.json and "code" in request.json:
#         return "code from json", request.json["code"]
#
#     return "", 204
#
#
# # Добавляем обработчики, вызываемые до запроса и после. Используем объект g. Он, как и объект
# # request, является локальным для текущего запроса. На него мы можем установить любые атрибуты.
# @app.before_request
# def process_before_request():
#     """
#     Sets start_time to `g` object
#     """
#     g.start_time = time()
#
#
# @app.after_request
# def process_after_request(response):
#     """
#     adds process time in headers
#     """
#     if hasattr(g, "start_time"):
#         response.headers["process-time"] = time() - g.start_time
#     return response
#
#
# @app.route("/power/")
# def power_value():
#     """Создаём view для возведения x в степень y. Добавляем обработку и валидацию входных данных,
#     логгирование, выброс исключения"""
#     x = request.args.get("x") or ""
#     y = request.args.get("y") or ""
#     if not (x.isdigit() and y.isdigit()):
#         app.logger.info("invalid values for power: x=%r and y=%r", x, y)
#         raise BadRequest("please pass integers in `x` and `y` query params")
#
#     x = int(x)
#     y = int(y)
#     result = x ** y
#     app.logger.debug("%s ** %s = %s", x, y, result)
#     return str(result)
#
#
# # Создаём view do_zero_division, который будет вызывать исключение. А также регистрируем
# # обработчик handle_zero_division_error при помощи декоратора @app.errorhandler(ZeroDivisionError)
# # (передаём туда исключение, которое собираемся ловить).
# @app.route("/divide-by-zero/")
# def do_zero_division():
#     return 1 / 0
#
#
# @app.errorhandler(ZeroDivisionError)
# def handle_zero_division_error(error):
#     print(error)  # prints str version of error: 'division by zero'
#     app.logger.exception("Here's traceback for zero division error")
#     return "Never divide by zero!", 400
# #
# #
# # @app.errorhandler(404)
# # def handle_404(error):
# #     app.logger.error(error)
# #     return '404 =('
