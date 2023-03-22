from werkzeug.security import generate_password_hash  # Для хеширования пароля

# from blog.app import create_app, db
from blog.app import create_app
from blog.extensions import db
import click

app = create_app()


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("Well done!")


@app.cli.command("create-users")  # Создание юзеров в БД
def create_users():
    """
    Run in your terminal:
    flask create-users
    """
    # > done! created users: <User #1 'admin'> <User #2 'james'>

    from blog.models import User
    # В методичке:
    # admin = User(username="admin", is_staff=True)
    # james = User(username="james")
    # db.session.add(admin)
    # db.session.add(james)
    # db.session.commit()
    # print("done! created users:", admin, james)

    # С урока:  --------- закоментил на 5 уроке
    # db.session.add(
    #     User(email='name@email.com', password=generate_password_hash('test123'))
    # )
    # db.session.commit()


# 7 урок - так сделал я
@app.cli.command('create-init-tags')
def create_init_tags():
    """
    Created tags
    """
    from blog.models import Tag
    from wsgi import app

    with app.app_context():
        tags = ('flask', 'django', 'python', 'gb', 'sqlite')
        for item in tags:
            db.session.add(Tag(name=item))
        db.session.commit()
    click.echo(f'Created tags: {", ".join(tags)}')


# wsgi для первого урока
# # Это точка входа для приложения, для его запуска.
#
# from blog.app import app


if __name__ == "__main__":  # изолирует повторое использование кода при импорте
    app.run(
        # host="0.0.0.0",  # Адрес обращения к хосту
        debug=True,  # Режим дебага.
    )
