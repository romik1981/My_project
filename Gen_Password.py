'''
Программа для генерации паролей по определённым правилам!
'''
import random
import sys

cap_let = [chr(let) for let in range(ord('A'), ord('Z') +1)]
low_let = [chr(let) for let in range(ord('a'), ord('z') + 1)]
num = [str(num) for num in range(0, 10)]
symbol = ['-', '+', '=', '_', '*', '$', '/', '#', '&', '%', '!', '@']
low_let.remove('l'), cap_let.remove('I'), cap_let.remove('O')
#print(cap_let, low_let, num, symbol, (len(cap_let) + len(low_let) + len(num) + len(symbol)), sep='\n')

#password_list = list(map(lambda x: random.choice(x), [cap_let, low_let, num, symbol]))
#random.shuffle(password_list)
#password_str = ''.join(password_list)
#a = round(random.random() * 10)
#print(random.sample(cap_let, 5))
def get_password(n_cap, n_low, n_num, n_sym, can_repeat=False) -> str:
    cap_let_list = list(random.sample(cap_let, n_cap))
    low_let_list = list(random.sample(low_let, n_low))
    num_list = list(random.sample(num, n_num))
    symbol_list = list(random.sample(symbol, n_sym))
    password_list = cap_let_list + low_let_list + num_list + symbol_list
    random.shuffle(password_list)
    password_str = ''.join(password_list)
    return password_str

   # for _ in range(k_sym_pass):


print('Программа для генерации паролей длиной не более 30 символов!',
      'Состоящие, по умолчанию, из заглавных и строчных букв латинского алфавита, цифр и некоторых символов.',
      'Примечание: В паролях отсутствуют буквs "O", "l", "I", так как они похожи на некоторые цифры и друг на друга.\n',
      sep='\n')

k_sym_pass, quantity_pass = input('Введите число символов пароля: '), input('Введите число паролей: ')
symbol_password = input('Введите символы используемые в паролях (c - заглавные, l - строчные, n - цифры, s - символы): ')
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
        print(password, end='   ')
        n += 1

        if save_file == 'y':
            with open('password.xml', 'a+', encoding='utf-8') as fw:
                fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

elif symbol_password.lower() == 'c':

    n_cap = k_sym_pass
    n_low = 0
    n_num = 0
    n_sym = 0
    n = 0
    print('Ваши пароли:', end=' ')
    while n < int(quantity_pass):
        password = get_password(n_cap, n_low, n_num, n_sym)
        print(password, end='   ')
        n += 1

        if save_file == 'y':
            with open('password.xml', 'a+', encoding='utf-8') as fw:
                fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

elif symbol_password.lower() == 'l':

    n_cap = 0
    n_low = k_sym_pass
    n_num = 0
    n_sym = 0
    n = 0
    print('Ваши пароли:', end=' ')
    while n < int(quantity_pass):
        password = get_password(n_cap, n_low, n_num, n_sym)
        print(password, end='   ')
        n += 1

        if save_file == 'y':
            with open('password.xml', 'a+', encoding='utf-8') as fw:
                fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

elif symbol_password.lower() == 'n':

    n_cap = 0
    n_low = 0
    n_num = k_sym_pass
    n_sym = 0
    n = 0
    print('Ваши пароли:', end=' ')
    while n < int(quantity_pass):
        password = get_password(n_cap, n_low, n_num, n_sym)
        print(password, end='   ')
        n += 1

        if save_file == 'y':
            with open('password.xml', 'a+', encoding='utf-8') as fw:
                fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.

elif symbol_password.lower() == 's':

    n_cap = 0
    n_low = 0
    n_num = 0
    n_sym = k_sym_pass
    n = 0
    print('Ваши пароли:', end=' ')
    while n < int(quantity_pass):
        password = get_password(n_cap, n_low, n_num, n_sym)
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
        password = get_password(n_cap, n_low, n_num, n_sym)
        print(password, end='   ')
        n += 1

        if save_file == 'y':
            with open('password.xml', 'a+', encoding='utf-8') as fw:
                fw.writelines(f'{password}\n')  # Записывает в файл сгенерированный пароль.


# print(password_str)
#print(password_str1)
