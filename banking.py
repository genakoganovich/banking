import random
import string
import sqlite3


def calculate_check_sum(sliced_number):
    check_sum = 0
    for j in range(len(sliced_number)):
        digit = int(sliced_number[j])
        if j % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        check_sum += digit
    return check_sum


def calculate_check_digit(sliced_number):
    return (calculate_check_sum(sliced_number) * 9) % 10


def is_valid(number):
    return int(number[15]) == calculate_check_digit(number[0:15])


def generate_number():
    number = '400000'
    for i in range(9):
        number += random.choice(string.digits)
    number += str(calculate_check_digit(number))
    return number


def generate_pin():
    p = ''
    for i in range(4):
        p += random.choice(string.digits)
    return p


main_menu = '''1. Create an account
2. Log into account
0. Exit'''

menu = '''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit'''


tb_create = '''CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);'''
random.seed()
exit_flag = False
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()


while not exit_flag:
    print(main_menu)
    input_string = input()
    print()
    if input_string == '1':
        card_number = generate_number()
        pin = generate_pin()
        tb_insert = 'INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?);'
        cur.execute(tb_insert, (0, str(card_number), str(pin), 0))
        conn.commit()
        print('Your card has been created')
        print('Your card number:')
        print(card_number)
        print('Your card PIN:')
        print(pin)
        print()

    elif input_string == '2':
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        pin = input()
        print()
        tb_select = 'SELECT number, pin, balance FROM card WHERE number={}'.format(card_number)
        cur.execute(tb_select)
        response = cur.fetchone()
        if not response or response[1] != pin:
            print('Wrong card number or PIN!')
            print()
        else:
            print('You have successfully logged in!')
            print()
            while True:
                print(menu)
                input_string = input()
                print()
                if input_string == '1':
                    cur.execute(tb_select)
                    response = cur.fetchone()
                    print('Balance: {}'.format(response[2]))
                    print()
                elif input_string == '2':
                    cur.execute(tb_select)
                    response = cur.fetchone()
                    print('Enter income:')
                    income = int(input())
                    tb_update = 'UPDATE card SET balance={} WHERE number={};'.format((response[2] + income), response[0])
                    cur.execute(tb_update)
                    conn.commit()
                    print('Income was added!')
                    print()
                elif input_string == '3':
                    cur.execute(tb_select)
                    response = cur.fetchone()
                    print('Transfer')
                    print('Enter card number:')
                    transfer_number = input()
                    tb_transfer_select = 'SELECT number, pin, balance FROM card WHERE number={}'.format(transfer_number)
                    cur.execute(tb_transfer_select)
                    transfer_response = cur.fetchone()
                    if not is_valid(transfer_number):
                        print('Probably you made mistake in the card number. Please try again')
                        print()
                    elif not transfer_response:
                        print('Such a card does not exist.')
                        print()
                    elif transfer_response[0] == response[0]:
                        print("You can't transfer money to the same account!")
                        print()
                    else:
                        print('Enter how much money you want to transfer:')
                        transfer_money = int(input())
                        if transfer_money > response[2]:
                            print('Not enough money!')
                            print()
                        else:
                            tb_get = 'UPDATE card SET balance={} WHERE number={};'\
                                .format((response[2] - transfer_money), response[0])
                            tb_add = 'UPDATE card SET balance={} WHERE number={};'\
                                .format((transfer_response[2] + transfer_money), transfer_response[0])
                            cur.execute(tb_get)
                            conn.commit()
                            cur.execute(tb_add)
                            conn.commit()
                            print('Success!')
                            print()
                elif input_string == '4':
                    tb_delete = 'DELETE FROM card WHERE number={};'.format(response[0])
                    cur.execute(tb_delete)
                    conn.commit()
                    print()
                    print('The account has been closed!')
                    print()
                    break
                elif input_string == '5':
                    print('You have successfully logged out!')
                    print()
                    break
                elif input_string == '0':
                    print('Bye!')
                    exit_flag = True
                    break
    elif input_string == '0':
        print('Bye!')
        exit_flag = True
        break
# cur.execute('DROP TABLE card;')
# conn.commit()
conn.close()
