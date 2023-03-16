# 7 Урок - так у преподавателя
# import click
# from werkzeug.security import generate_password_hash
#
# from blog.extensions import db
#
#
# @click.command('create-init-user')
# def create_init_user():
#     from blog.models import User
#     from wsgi import app
#
#     with app.app_context():
#         db.session.add(
#             User(email='name@example.com', password=generate_password_hash('test123'))
#         )
#         db.session.commit()
#
#
# @click.command('create-init-tags')
# def create_init_tags():
#     from blog.models import Tag
#     from wsgi import app
#
#     with app.app_context():
#         tags = ('flask', 'django', 'python', 'gb', 'sqlite')
#         for item in tags:
#             db.session.add(Tag(name=item))
#         db.session.commit()
#     click.echo(f'Created tags: {", ".join(tags)}')


# # Регистрируем команды
# from blog.app import db
# from wsgi import app
#
#
# @app.cli.command("init-db")
# def init_db():
#     """
#     Run in your terminal:
#     flask init-db
#     """
#     db.create_all()
#     print("done!")
#
#
# @app.cli.command("create-users")
# def create_users():
#     """
#     Run in your terminal:
#     flask create-users
#     > done! created users: <User #1 'admin'> <User #2 'james'>
#     """
#     from blog.models import User
#     admin = User(username="admin", is_staff=True)
#     james = User(username="james")
#     db.session.add(admin)
#     db.session.add(james)
#     db.session.commit()
#     print("done! created users:", admin, james)