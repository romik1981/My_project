from wsgiref.simple_server import make_server
from roman_framework.main import Framework
from views import routes

# Создаем объект WSGI-приложения
application = Framework(routes)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()

# Пробуем записать логи в файл.
# with open('log.txt', 'a+', encoding='utf-8') as fa:
#     for _ in a:
#         fa.writelines(f'{_}\n')  # Записывает в файл ответ сервера.
