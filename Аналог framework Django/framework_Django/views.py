"""Модуль, содержащий контроллеры веб-приложения"""
from datetime import date

from roman_framework.templator import render
from components.models import Engine

site = Engine()


# Класс-контроллер - Главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# Класс-контроллер - Страница "О проекте"
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')

# Класс-контроллер - Страница "Описание проекта"
class Description:
    def __call__(self, request):
        return '200 OK', 'In this project, I, Roman Belyakov, teach several courses on the basics of programming on ' \
                'Python language. Together we will analyze some topics in theory and in practice. Course schedule ' \
                'may vary!'


# Класс-контроллер - Страница "Моя личная страница"
class My_site:
    def __call__(self, request):
        return '200 OK', render('my_site.html')


# Класс-контроллер - Страница "Генератор паролей"
class Genpassword:
    def __call__(self, request):
        return '200 OK', render('genpassword.html')


# Класс-контроллер - Страница "Страница проекта из шага 2"
class Step_2:
    def __call__(self, request):
        return '200 OK', render('step_2.html')


# Класс-контроллер - Страница "Расписания"
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# Класс-контроллер - Страница 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Класс-контроллер - Страница "Список курсов"
class CoursesList:
    def __call__(self, request):

        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# Класс-контроллер - Страница "Создать курс"
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                print(f'ахх {request}')
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# Класс-контроллер - Страница "Создать категорию"
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':

            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)



# Класс-контроллер - Страница "Список категорий"
class CategoryList:
    def __call__(self, request):
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)
