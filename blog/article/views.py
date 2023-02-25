# Реализация blueprint - статьи
from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')  # article - name,
# __name__ - текущее название пакета, static_folder - где хранится статика
ARTICLES = {
    1: {
        'title': 'Django',
        'text': 'свободный фреймворк для веб-приложений на языке Python, использующий шаблон проектирования MVC. '
                'Проект поддерживается организацией Django Software Foundation. Сайт на Django строится из одного '
                'или нескольких приложений, которые рекомендуется делать отчуждаемыми и подключаемыми.',
        'author': {
            'name': 'Adrian Holovaty, Simon Willison',
            'id': 1,
        }
    },
    2: {
        'title': 'Flask',
        'text': 'фреймворк для создания веб-приложений на языке программирования Python, использующий набор '
                'инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых '
                'микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь '
                'самые базовые возможности.',
        'author': {
            'name': 'Армин Ронахер',
            'id': 2,
        }
    },
}
# ARTICLES = {
#     1: "Flask",
#     2: "Django",
#     3: "JSON:API",
# }


@article.route('/')  # регистрируем в роуте блюпринт по адресу localhost/article/ с функцией ниже:
def article_list():  # ф-ия, которая не принимает ничего
    return render_template(  # Ф-ия render_template принимает в себя template name или list
        # (название нашего шаблона, который должен быть отрисован)
        'articles/list.html',
        articles=ARTICLES,
    )


@article.route('/<int:pk>')  # pk - primary key
def get_article(pk: int):  # Принимает id статьи
    """Получение конкретной статьи"""
    try:  # обрабатываем исключение, если статьи с таким id не будет
        article_body = ARTICLES[pk]
    except KeyError:
        raise NotFound(f'Article id {pk} not found')  # Выдаём текст с отработанной ошибкой
    article_pk = pk
    return render_template(
        'articles/details.html',
        article_body=article_body,
        article_pk=article_pk,
    )
