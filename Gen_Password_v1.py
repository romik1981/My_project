'''
Программа для генерации паролей по определённым правилам!
'''
import random

cap_let = [chr(let) for let in range(ord('A'), ord('Z') + 1)]  # Заглавные буквы латиницы
low_let = [chr(let) for let in range(ord('a'), ord('z') + 1)]  # Строчные буквы латиницы
cap_let_ru = [chr(let) for let in range(ord('А'), ord('Я') + 1)]  # Заглавные буквы кирилицы
low_let_ru = [chr(let) for let in range(ord('а'), ord('я') + 1)]  # Строчные буквы кирилицы
num = [str(num) for num in range(0, 10)]
symbol = ['-', '+', '=', '_', '*', '$', '/', '#', '&', '%', '!', '@']
low_let.remove('l'), cap_let.remove('I'), cap_let.remove('O')


# print(cap_let, low_let, num, symbol, len(cap_let), len(low_let), len(num), len(symbol),
# (len(cap_let) + len(low_let) + len(num) + len(symbol)), sep='\n') # Используемые списки, их длинна и
# общее колличество символов.


def get_password(n_cap, n_low, n_num, n_sym, k_sym_pass, pass_lang) -> str:
    """
    Функция генерации парлей уникальных значений или с повторами
    :param n_cap: число заглавных букв
    :param n_low: число строчных букв
    :param n_num: число цифр
    :param n_sym: число символов
    :param can_repeat: флаг возможности повтора символов
    :return: возвращает строку пароля
    """
    cap_let_work = cap_let
    low_let_work = low_let
    if 'ru' in pass_lang:
        cap_let_work = cap_let_ru
        low_let_work = low_let_ru
    if 'y' in pass_lang:
        can_repeat = True
    else:
        can_repeat = False

    if not can_repeat:
        cap_let_list = list(random.sample(cap_let_work, n_cap))  # делаем выборку уникальных элементов из списка
        low_let_list = list(random.sample(low_let_work, n_low))
        num_list = list(random.sample(num, n_num))
        symbol_list = list(random.sample(symbol, n_sym))
        password_list = cap_let_list + low_let_list + num_list + symbol_list
        random.shuffle(password_list)
        password_str = ''.join(password_list)
        return password_str

    if can_repeat:
        password_list = []
        while len(password_list) < int(k_sym_pass):
            if n_cap != 0:
                password_list.append(random.choice(cap_let_work))
            if n_low != 0:
                password_list.append(random.choice(low_let_work))
            if n_num != 0:
                password_list.append(random.choice(num))
            if n_sym != 0:
                password_list.append(random.choice(symbol))
            if len(password_list) == int(k_sym_pass):
                break
        random.shuffle(password_list)
        password_str = ''.join(password_list)
        return password_str


def write_file_password(password, type_f=None):
    ''' Функция записи паролей в файл'''

    if type_f == None:
        with open('password.xml', 'a+', encoding='utf-8') as fa:
            fa.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

    if type_f == 'sed':
        list_out = []
        with open('password_test.csv', 'r', encoding='utf-8') as fr:
            for str_ in fr:
                a = str_.strip().split(";")
                for i, _ in enumerate(a):
                    if _ == 'p':
                        a[i] = get_password(2, 2, 3, 1, 8, 'lat n')
                a.append('\n')
                list_out.append(';'.join(a))
        with open(f'password_out_{type_f}.csv', 'w+', encoding='utf-8') as fw:
            for _ in list_out:
                fw.writelines(_)
        return print(f'Пароли сгенерированны в файл password_out_{type_f}.csv')


def param_password():
    # Функция парсинга параметров пароля
    param_password_in = input('Введите параметры пароля через пробел (например: lat n 8 1 clns y)'
                              'или воспользуйтесь help (h): ')

    if param_password_in == 'h':
        return help_f()

    if param_password_in == 'sed':
        write_file_password('password_sed', type_f='sed')

    param_password_in_list = param_password_in.split(" ")
    while len(param_password_in_list) != 6:
        param_password_in_list.append("")
    pass_lang = ' '.join(param_password_in_list[:2])
    k_sym_pass = param_password_in_list[2]
    quantity_pass = param_password_in_list[3]
    symbol_password = param_password_in_list[4]
    save_file = param_password_in_list[5]

    if k_sym_pass == '':
        k_sym_pass = 8
    if quantity_pass == '':
        quantity_pass = 1

    n_cap_f, n_low_f, n_num_f, n_sym_f = False, False, False, False
    if symbol_password == '':
        n_cap_f, n_low_f, n_num_f, n_sym_f = True, True, True, True
    for el in symbol_password.lower():
        if el == 'c':
            n_cap_f = True
        if el == 'l':
            n_low_f = True
        if el == 'n':
            n_num_f = True
        if el == 's':
            n_sym_f = True

    if not n_cap_f and not n_low_f and not n_num_f and not n_sym_f:
        return param_password()

    if n_cap_f + n_low_f + n_num_f + n_sym_f == 4:
        n_cap = round(int(k_sym_pass) / 4)
        n_low = round(int(k_sym_pass) / 4)
        n_num = round(int(k_sym_pass) * 7 / 20)
        n_sym = round(int(k_sym_pass) * 3 / 20)
    elif n_cap_f + n_low_f + n_num_f + n_sym_f == 3:
        n_cap = round(int(k_sym_pass) / 3) * n_cap_f
        n_low = round(int(k_sym_pass) / 3) * n_low_f
        n_num = round(int(k_sym_pass) / 3) * n_num_f
        n_sym = round(int(k_sym_pass) / 3) * n_sym_f
    elif n_cap_f + n_low_f + n_num_f + n_sym_f == 2:
        n_cap = round(int(k_sym_pass) / 2) * n_cap_f
        n_low = round(int(k_sym_pass) / 2) * n_low_f
        n_num = round(int(k_sym_pass) / 2) * n_num_f
        n_sym = round(int(k_sym_pass) / 2) * n_sym_f
    elif n_cap_f + n_low_f + n_num_f + n_sym_f == 1:
        n_cap = int(k_sym_pass) * n_cap_f
        n_low = int(k_sym_pass) * n_low_f
        n_num = int(k_sym_pass) * n_num_f
        n_sym = int(k_sym_pass) * n_sym_f

    return n_cap, n_low, n_num, n_sym, k_sym_pass, pass_lang, quantity_pass, save_file, param_password_in


def help_f() -> str:
    # Функция вызова помощи при вводе параметров паролей
    print('Введите данные для запуска программы генерации паролей через пробел в одну строку:\n'
          ' 1 - Введите алфавит пароля латинский(lat) или кирилицу(ru),по умолчанию латинский алфавит;\n'
          ' 2 - Введите возможность повтора символов в паролях (да->y или нет->n).\n'
          ' 3 - Введите количество символов в пароле не более 30, 10 и 12 если в пароле только буквы или символы '
          'соответственно либо укажите возможность повтора символов в пароле, по умолчанию символов 8;\n'
          ' 4 - Введите количество паролей, которые будут созданы, по умолчанию пароль 1;\n'
          ' 5 -Введите символы используемые в пароле в той последовательности как показано, по умолчанию все:\n'
          '       c - заглавные буквы алфавита,\n'
          '       l - строчные буквы алфавита,\n'
          '       n - цифры от 0 до 9,\n'
          '       s - символы "[-, +, =, _, *, $, /, #, &, %, !, @]";\n'
          ' 6 - При необходимости можно сохранить результаты в файл (password.xml или другой), да->y или нет->n;\n'
          ' Пример ввода данных: lat y 10 3 cln y;\n'
          ' Параметры пароля по умолчанию: lat n 8 1 clns n;\n'
          ' Примечание: Параметры пароля вводятся через пробел латинскими буквами, если оставляете параметр по умолчанию,'
          'замените его пробелом или не вводите его нажав Enter (в конце строки).\n')
    return param_password()


print('Программа для генерации паролей длиной не более 30 символов!',
      'Состоящие, по умолчанию, из заглавных и строчных букв латинского алфавита, цифр и некоторых символов.',
      'Примечание: В паролях отсутствуют буквы "O", "l", "I", так как они похожи на некоторые цифры и друг на друга.\n',
      sep='\n')

try:
    n_cap, n_low, n_num, n_sym, k_sym_pass, pass_lang, quantity_pass, save_file, param_password_in = param_password()

    if param_password_in != 'sed':
        print('Ваши пароли:', end=' ')
        n = 0
        while n < int(quantity_pass):
            password = get_password(n_cap, n_low, n_num, n_sym, k_sym_pass, pass_lang)
            print(password, end='   ')
            n += 1
            if save_file == 'y':
                write_file_password(password, type_f=None)


except ValueError:
    print('Вы ввели неправильные значения, повторите выполнение программы и введите значения согласно требованиям'
          'или оставте по умолчанию(нажав Enter).')
except TypeError:
    print('Число символов пароля превышает количество уникальных значений исходного списка!')
print('\n')
input('Для завершения нажмите Enter')
