# Реализация blueprint - отчёты
from flask import Blueprint, render_template

report = Blueprint('report', __name__, url_prefix='/reports', static_folder='../static')  # report - name,
# __name__ - текущее название пакета, static_folder - где хранится статика


@report.route('/')  # регистрируем в роуте блюпринт по адресу localhost/report/ с функцией ниже:
def report_list():  # ф-ия, которая не принимает ничего
    return render_template(
        'reports/list.html',
        reports=[1, 2, 3, 4, 5]
    )
