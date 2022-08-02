'''
Программа для генерации паролей по определённым правилам!
'''
import random

cap_let = [chr(let) for let in range(ord('A'), ord('Z') + 1)]
low_let = [chr(let) for let in range(ord('a'), ord('z') + 1)]
num = [str(num) for num in range(0, 10)]
symbol = ['-', '+', '=', '_', '*', '$', '/', '#', '&', '%', '!', '@']
low_let.remove('l'), cap_let.remove('I'), cap_let.remove('O')


#print(cap_let, low_let, num, symbol, len(cap_let), len(low_let), len(num), len(symbol),
      #(len(cap_let) + len(low_let) + len(num) + len(symbol)), sep='\n')


def get_password(n_cap, n_low, n_num, n_sym, can_repeat) -> str:
    """
    Функция генерации парлей уникальных значений или с повторами
    :param n_cap: число заглавных букв
    :param n_low: число строчных букв
    :param n_num: число цифр
    :param n_sym: число символов
    :param can_repeat: флаг возможности повтора символов
    :return: возвращает строку пароля
    """

    if not can_repeat:
        cap_let_list = list(random.sample(cap_let, n_cap))  # делаем выборку уникальных элементов из списка
        low_let_list = list(random.sample(low_let, n_low))
        num_list = list(random.sample(num, n_num))
        symbol_list = list(random.sample(symbol, n_sym))
        password_list = cap_let_list + low_let_list + num_list + symbol_list
        random.shuffle(password_list)
        password_str = ''.join(password_list)
        return password_str

    if can_repeat:
        password_list = []
        while len(password_list) < int(k_sym_pass):
            for _ in [cap_let, low_let, num, symbol]:
                password_list.append(random.choice(_))
                if len(password_list) == int(k_sym_pass):
                    break
        random.shuffle(password_list)
        password_str = ''.join(password_list)
        return password_str



print('Программа для генерации паролей длиной не более 30 символов!',
      'Состоящие, по умолчанию, из заглавных и строчных букв латинского алфавита, цифр и некоторых символов.',
      'Примечание: В паролях отсутствуют буквs "O", "l", "I", так как они похожи на некоторые цифры и друг на друга.\n',
      'Для вывода помощи нажмите "h".',
      sep='\n')
help = input()

if help == 'h':
    print('Введите данные для запуска программы генерации паролей:\n'
          '1 - Введите количестово символов в пароле не более 30, при большем количестве символов возможны повторы символов,'
          ' по умолчанию символов 8;\n'
          '2 - Введите количество паролей, которые будут созданы, по умолчанию пароль 1;\n'
          '3 - Введите символы используемые в пароле в той последовательности как показано, по умолчанию все:\n '
          '     c - заглавные буквы алфавита,\n'
          '     l - строчные буквы алфавита,\n'
          '     n - цифры от 0 до 9,\n'
          '     s - символы "[-, +, =, _, *, $, /, #, &, %, !, @]";\n'
          '4 - при необходимости можно сохранить результаты в файл password.xml;\n'
          '5 - можно выбрать алфавит пароля латинский(lat) или кирилицу(ru),по умолчанию латинский алфавит и укажите '
          'возможность повтора символов (да->y или нет->n).\n'
          'Примечание: если разрешены повторы("y"), в этом случае используются все символы вне зависимости от '
          'комбинации "clns".\n')
try:

    pass_lang = input('Введите язык пароля("lat" or "ru"), возможны повторы в пароле (y/n): ')

    if 'ru' in pass_lang:
        cap_let = [chr(let) for let in range(ord('А'), ord('Я') + 1)]  # Заглавные буквы кирилицы
        low_let = [chr(let) for let in range(ord('а'), ord('я') + 1)]  # Строчные буквы кирилицы
    if 'y' in pass_lang:
        can_repeat = True
    else:
        can_repeat = False


    k_sym_pass, quantity_pass = input('Введите число символов пароля: '), input('Введите число паролей: ')
    symbol_password = input(
        'Введите символы используемые в паролях (c - заглавные, l - строчные, n - цифры, s - символы): ')
    save_file = input('Сохранить данные в файл? y/n: ')



    if k_sym_pass == '':
        k_sym_pass = 8
    if quantity_pass == '':
        quantity_pass = 1
    if symbol_password.lower() == 'clns':
        n_cap = round(int(k_sym_pass) / 4)
        n_low = round(int(k_sym_pass) / 4)
        n_num = round(int(k_sym_pass) * 7 / 20)
        n_sym = round(int(k_sym_pass) * 3 / 20)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1
            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'cln':

        n_cap = round(int(k_sym_pass) / 4)
        n_low = round(int(k_sym_pass) / 4)
        n_num = round(int(k_sym_pass) / 2)
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'cls':

        n_cap = round(int(k_sym_pass) / 4)
        n_low = round(int(k_sym_pass) / 4)
        n_num = 0
        n_sym = round(int(k_sym_pass) / 2)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'cns':

        n_cap = round(int(k_sym_pass) / 4)
        n_low = 0
        n_num = round(int(k_sym_pass) / 4)
        n_sym = round(int(k_sym_pass) / 2)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'lns':

        n_cap = 0
        n_low = round(int(k_sym_pass) / 4)
        n_num = round(int(k_sym_pass) / 4)
        n_sym = round(int(k_sym_pass) / 2)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'cl' or symbol_password.lower() == 'lc':

        n_cap = round(int(k_sym_pass) / 2)
        n_low = round(int(k_sym_pass) / 2)
        n_num = 0
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'cn' or symbol_password.lower() == 'nc':

        n_cap = round(int(k_sym_pass) / 2)
        n_low = 0
        n_num = round(int(k_sym_pass) / 2)
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'cs' or symbol_password.lower() == 'sc':

        n_cap = round(int(k_sym_pass) / 2)
        n_low = 0
        n_num = 0
        n_sym = round(int(k_sym_pass) / 2)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'ls' or symbol_password.lower() == 'sl':

        n_cap = 0
        n_low = round(int(k_sym_pass) / 2)
        n_num = 0
        n_sym = round(int(k_sym_pass) / 2)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'ln' or symbol_password.lower() == 'nl':

        n_cap = 0
        n_low = round(int(k_sym_pass) / 2)
        n_num = round(int(k_sym_pass) / 2)
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'ns' or symbol_password.lower() == 'sn':

        n_cap = 0
        n_low = 0
        n_num = round(int(k_sym_pass) / 2)
        n_sym = round(int(k_sym_pass) / 2)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'c':

        n_cap = int(k_sym_pass)
        n_low = 0
        n_num = 0
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'l':

        n_cap = 0
        n_low = int(k_sym_pass)
        n_num = 0
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 'n':

        n_cap = 0
        n_low = 0
        n_num = int(k_sym_pass)
        n_sym = 0
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    elif symbol_password.lower() == 's':

        n_cap = 0
        n_low = 0
        n_num = 0
        n_sym = int(k_sym_pass)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    else:

        n_cap = round(int(k_sym_pass) / 4)
        n_low = round(int(k_sym_pass) / 4)
        n_num = round(int(k_sym_pass) * 7 / 20)
        n_sym = round(int(k_sym_pass) * 3 / 20)
        n = 0
        print('Ваши пароли:', end=' ')
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, can_repeat)
            print(password, end='   ')
            n += 1

            if save_file == 'y':
                with open('password.xml', 'a+', encoding='utf-8') as fw:
                    #fw.seek(10)
                    fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.
                    #print(fw.tell())

except ValueError:
    print('Вы ввели неправильные значения, повторите выполнение программы и введите значения по запросам или оставте '
          'по умолчанию(нажав Enter).')
except TypeError:
    print('Число символов пароля превышает количество уникальных значений исходного списка!')
