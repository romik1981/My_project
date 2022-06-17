'''
Программа для генерации паролей по определённым правилам!
'''
import random

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
def get_password(n_cap, n_low, n_num, n_sym) -> str:
    cap_let_list =list(random.sample(cap_let, n_cap))
    low_let_list = list(random.sample(low_let, n_low))
    num_list = list(random.sample(num, n_num))
    symbol_list = list(random.sample(symbol, n_sym))
    password_list = cap_let_list + low_let_list + num_list + symbol_list
    random.shuffle(password_list)
    password_str = ''.join(password_list)
    return password_str

print('Программа для генерации паролей длиной не более 30 символов!',
      'Состоящие, по умолчанию, из заглавных и строчных букв латинского алфавита,','цифр и некоторых символов.',
      'Примечание: В паролях отсутствуют буквs "O", "l", "I", так как они похожи на некоторые цифры и друг на друга.\n',
      sep='\n')
#k_sym_pass = int(input('Введите число символов пароля: '))
k_sym_pass = 8
n_cap = round(k_sym_pass / 4)
n_low = round(k_sym_pass / 4)
n_num = round(k_sym_pass  * 7 / 20)
n_sym = round(k_sym_pass * 3 /  20)
print('Ваш пароль:',get_password(n_cap, n_low, n_num, n_sym))
# print(password_str)
#print(password_str1)
