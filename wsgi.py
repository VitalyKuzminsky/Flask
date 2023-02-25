from blog.app import create_app

app = create_app()

# wsgi для первого урока
# # Это точка входа для приложения, для его запуска.
#
# from blog.app import app


if __name__ == "__main__":  # изолирует повторое использование кода при импорте
    app.run(
        host="0.0.0.0",  # Адрес обращения к хосту
        debug=True,  # Режим дебага.
    )
