"""Модуль, содержащий контроллеры веб-приложения"""
from roman_framework.templator import render


class Index:
    def __call__(self):
        return '200 OK', render('index.html')


class About:
    def __call__(self):
        return '200 OK', render('about.html')


class Description:
    def __call__(self):
        return '200 OK', 'In this project, I, Roman Belyakov, teach several courses on the basics of programming on ' \
                'Python language. Together we will analyze some topics in theory and in practice. Course schedule ' \
                'may vary!'


class My_site:
    def __call__(self):
        return '200 OK', render('site(hw)-html/index.html')


class Genpassword:
    def __call__(self):
        return '200 OK', render('site(hw)-html/genpass(hw).html')


class Step_2:
    def __call__(self):
        return '200 OK', render('step_2/index.html')