# Реализация blueprint - пользователи
from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import NotFound

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')  # user - name,
# __name__ - текущее название пакета, static_folder - где хранится статика
USERS = {
    1: "James",
    2: "Brian",
    3: "Peter",
}
# USERS = ['Alice', 'John', 'Mike']


@user.route('/')  # регистрируем в роуте блюпринт по адресу localhost/user/ с функцией ниже:
def user_list():  # ф-ия, которая не принимает ничего
    return render_template(  # Ф-ия render_template принимает в себя template name или list
        # (название нашего шаблона, который должен быть отрисован)
        'users/list.html',
        users=USERS,
    )


@user.route('/<int:pk>')  # pk - primary key
def get_user(pk: int):  # Принимает id юзера
    """Получение конкретного юзера"""
    try:  # обрабатываем исключение, если юзера с таким id не будет
        user_name = USERS[pk]
    except KeyError:
        raise NotFound(f'User id {pk} not found')  # Выдаём текст с отработанной ошибкой
        # return redirect('/users/')  # В случае ошибки - редиректим на указанный адрес
    user_pk = pk
    return render_template(
        'users/details.html',
        user_name=user_name,
        user_pk=user_pk,
    )
