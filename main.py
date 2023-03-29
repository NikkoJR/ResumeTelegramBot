from aiogram.filters import CommandStart
from config import TOKEN
from buttons import keyboard_main_buttons, markup1, markup2
import random
import string
from random import randint
from aiogram import Bot, Dispatcher
from aiogram.filters import Text
from aiogram.types import (CallbackQuery, Message)
from buttons import balance_work, add_balance_buttons, max, accept, another_type_to_add_balance, back, keyboard_admin_buttons, keyboard_start, keyboard_work_with_balances, take_money_back_buttons, keyboard_adminwork_take_money, keyboard_choose_type_to_update_balances, my_invest_buttons, invest_from, take_invest_to, calculator_keyboard, support, go_to_info, start
from datetime import datetime
import asyncio
import datetime
import sqlite3


# Connect to bot in TG
bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()


# Base of date
bd = sqlite3.connect('importbuttons.bd')
cur = bd.cursor()

bd.execute('CREATE TABLE IF NOT EXISTS {}(user_id INTEGER)'.format('users'))
bd.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS referrals (
                    user_id INTEGER PRIMARY KEY,
                    ref_link TEXT NOT NULL
                )""")
bd.commit()



# Lists
info_about_person: dict = {'accumulated': 0,
                           'deposit': 0,
                           'money_per_day': 0}

user_info: dict = {'user_id': 0,
                   'own_url': '',
                   'user_name': '',
                   'user_wallet': ''}

info_about_referals: dict = {'cash_from_invite': 0,
                             'invited': 0,
                             'referal_link': '',
                             'id_link_owner': 0,
                             'id': False,
                             'invited_by': ''}

wait_buttons: dict = {'admin_time_to_answer_login': False,
                      'admin_time_to_answer_password': False,
                      'add_balance1': False,
                      'add_balance2': False,
                      'wait_user_id': False,
                      'wait_sum_to_add': False,
                      'wait_process_take_money_1': False,
                      'wait_process_take_money_2': False,
                      'wait_process_take_money_3': False,
                      'wait_process_take_money_4': False,
                      'process_wait_to_update_balance': False,
                      'process_wait_to_update_balance2': False,
                      'wait_money_from_mainbalance_to_invest': False,
                      'wait_sum_to_take_back_from_invest_to_mainbalance': False,
                      'wait_money_from_refbalance_to_invest': False,
                      'calculate_sum': False,
                      'calculate_sum_with_reivest': False}

balance_info: dict = {'temporary_money_from_invite': 0}

admin_allow: dict = {'password': ''}

user_to_add_balance: dict = {'user_id': 0,
                            'money_to_add': 0}

listid = []


async def main():

    while True:
        # Получаем текущую дату и время
        now = datetime.datetime.now()

        # Ожидаем 15:00
        send_time = datetime.datetime(now.year, now.month, now.day, 15, 15, 0)
        if now < send_time:
            await asyncio.sleep((send_time - now).total_seconds())

        # Открываем соединение с базой данных
        conn = sqlite3.connect('importbuttons.bd')
        cursor = conn.cursor()

        cursor.execute('SELECT user_id FROM referrals WHERE send_time = ?', ('00:24',))
        rows = cursor.fetchall()

        for row in rows:
            chat_id = row[0]
            message_text = 'Hello!'
            await bot.send_message(chat_id, message_text)



# Function to main process
def calculate_money_per_day_from_invest(user_id):
    cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (user_id,))
    deposit = cur.fetchone()

    deposit = str(deposit)
    for i in deposit:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            deposit = deposit.replace(i, '')

    deposit = int(deposit)

    money_per_day = (3 / 100) * deposit
    money_per_day = int(money_per_day)

    print(deposit)

    return money_per_day




def calculate_function(user_id):
    money_per_day = calculate_money_per_day_from_invest(user_id)

    cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (user_id,))
    deposit = cur.fetchone()

    deposit = str(deposit)
    for i in deposit:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            deposit = deposit.replace(i, '')

    deposit = int(deposit)



    cur.execute("SELECT accumulated FROM referrals WHERE user_id=?", (user_id,))
    accumulated = cur.fetchone()

    accumulated = str(accumulated)
    for i in accumulated:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            accumulated = accumulated.replace(i, '')

    accumulated = int(accumulated)


    return deposit, accumulated, money_per_day


def info_about_referals_function(message: Message):
    cash_from_invite = 0
    invited = 0

    user_id = message.from_user.id
    user_info['user_id'] = user_id

    #
    #
    #

    cur.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
    bd.commit()

    user_id = message.from_user.id

    cur.execute("SELECT * FROM referrals WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if row is None:

        ref_link = generate_ref_link()

        cur.execute("INSERT INTO referrals (user_id, ref_link) VALUES (?, ?)", (user_id, ref_link))
        bd.commit()

    else:
        ref_link = row[1]

    referal_link = f"https://t.me/ArbitrageIncome_bot?start={ref_link}"
    info_about_referals['referal_link'] = referal_link
    print('Пользователь сейчас смотрит вкладку партнеры, его ссылка - ', referal_link)

    #
    #
    #

    cur.execute("SELECT ref_money FROM money WHERE user_id=?", (user_info['user_id'],))
    cash_from_invite = cur.fetchone()

    cash_from_invite = str(cash_from_invite)
    for i in cash_from_invite:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            cash_from_invite = cash_from_invite.replace(i, '')

    cash_from_invite = int(cash_from_invite)

    #
    #
    #

    cur.execute("SELECT lvl_one FROM referrals WHERE user_id=?", (user_info['user_id'],))
    invited_lvl1 = cur.fetchone()

    invited_lvl1 = str(invited_lvl1)
    for i in invited_lvl1:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            invited_lvl1 = invited_lvl1.replace(i, '')

    invited_lvl1 = int(invited_lvl1)

    sum = 0
    sum += invited_lvl1

    #

    cur.execute("SELECT lvl_two FROM referrals WHERE user_id=?", (user_info['user_id'],))
    invited_lvl2 = cur.fetchone()

    invited_lvl2 = str(invited_lvl2)
    for i in invited_lvl2:
        if i == '(' or i == ')' or i == ',':
            invited_lvl2 = invited_lvl2.replace(i, '')

    invited_lvl2 = int(invited_lvl2)

    sum += invited_lvl2

    #

    cur.execute("SELECT lvl_three FROM referrals WHERE user_id=?", (user_info['user_id'],))
    invited_lvl3 = cur.fetchone()

    invited_lvl3 = str(invited_lvl3)
    for i in invited_lvl3:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            invited_lvl3 = invited_lvl3.replace(i, '')

    invited_lvl3 = int(invited_lvl3)

    sum += invited_lvl3

    #
    #
    #

    cur.execute("SELECT invited_by FROM referrals WHERE user_id=?", (user_info['user_id'],))
    invited_by = cur.fetchone()

    invited_by = str(invited_by)
    for i in invited_by:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            invited_by = invited_by.replace(i, '')

    #
    #
    #


    info_about_referals['cash_from_invite'] = cash_from_invite
    info_about_referals['invited'] = sum
    info_about_referals['invited_by'] = invited_by


def generate_ref_link():
    ref_link = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    cur.execute("SELECT * FROM referrals WHERE ref_link=?", (ref_link,))

    if cur.fetchone() is None:
        return ref_link

    else:
        return generate_ref_link()


def add_temporary_money_to_table():

    cur.execute("SELECT ref_money FROM money WHERE user_id=?", (info_about_referals['id_link_owner'],))
    user_ref_money = cur.fetchone()

    user_ref_money = str(user_ref_money)
    for i in user_ref_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_ref_money = user_ref_money.replace(i, '')

    user_ref_money = int(user_ref_money)

    print(user_ref_money)

    user_ref_money += 3
    cur.execute(f'UPDATE money SET ref_money=? WHERE user_id=?', (user_ref_money, info_about_referals['id_link_owner']))
    bd.commit()
    print('updated')


def check_tablemoney(user_id):
    cur.execute(f"SELECT COUNT(*) FROM money WHERE user_id = '{user_id}'")
    result = cur.fetchone()

    return result


def add_to_table_referal_link():
    user_id = user_info['user_id']
    cur.execute(f'UPDATE referrals SET invited_by=? WHERE user_id=?', (info_about_referals['invited_by'], user_id))
    bd.commit()


def update_referal_lvls():
    owner_id = info_about_referals['id_link_owner']

    cur.execute("SELECT lvl_one FROM referrals WHERE user_id=?", (owner_id,))
    lvl_one = cur.fetchone()

    lvl_one = str(lvl_one)
    for i in lvl_one:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            lvl_one = lvl_one.replace(i, '')

    lvl_one = int(lvl_one)
    lvl_one += 1



    cur.execute(f'UPDATE referrals SET lvl_one=? WHERE user_id=?', (lvl_one, owner_id))
    bd.commit()


def update_use_referal_id():
    print(user_info['user_id'])
    cur.execute(f'UPDATE referrals SET use_referal_id=? WHERE user_id=?', (1, user_info['user_id']))
    bd.commit()







def add_procent(user_id, money):
    n = 0

    money = money

    ref_money_procent = 10

    owner_id = user_id

    for i in range(3):
        if ref_money_procent != 0:

            cur.execute("SELECT invited_by FROM referrals WHERE user_id=?", (owner_id,))
            availability = cur.fetchone()

            availability = str(availability)
            for i in availability:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    availability = availability.replace(i, '')



            if availability != '' and ref_money_procent == 10:
                n += 1

                cur.execute("SELECT user_id FROM referrals WHERE ref_link=?", (availability,))
                owner_id = cur.fetchone()

                owner_id = str(owner_id)
                for i in owner_id:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        owner_id = owner_id.replace(i, '')

                owner_id = int(owner_id)




                ref_money = cur.execute(f'SELECT ref_money FROM money WHERE user_id=?',(owner_id,)).fetchone()
                ref_money = str(ref_money)

                for i in ref_money:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        ref_money = ref_money.replace(i, '')

                ref_money = int(ref_money)



                ref_money_to_add = (ref_money_procent / 100) * money
                ref_money_to_add = int(ref_money_to_add)

                ref_money += ref_money_to_add

                cur.execute(f'UPDATE money SET ref_money=? WHERE user_id=?', (ref_money, owner_id))
                bd.commit()


                listid.append(owner_id)

                ref_money_procent -= 5


            elif availability != '' and ref_money_procent == 5:
                n += 1

                cur.execute("SELECT user_id FROM referrals WHERE ref_link=?", (availability,))
                owner_id = cur.fetchone()

                owner_id = str(owner_id)
                for i in owner_id:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        owner_id = owner_id.replace(i, '')

                owner_id = int(owner_id)





                ref_money = cur.execute(f'SELECT ref_money FROM money WHERE user_id=?', (owner_id,)).fetchone()
                ref_money = str(ref_money)

                for i in ref_money:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        ref_money = ref_money.replace(i, '')

                ref_money = int(ref_money)

                ref_money_to_add = (ref_money_procent / 100) * money
                ref_money_to_add = int(ref_money_to_add)

                ref_money += ref_money_to_add

                cur.execute(f'UPDATE money SET ref_money=? WHERE user_id=?', (ref_money, owner_id))
                bd.commit()

                listid.append(owner_id)

                ref_money_procent -= 3


            elif availability != '' and ref_money_procent == 2:
                n += 1

                cur.execute("SELECT user_id FROM referrals WHERE ref_link=?", (availability,))
                owner_id = cur.fetchone()

                owner_id = str(owner_id)
                for i in owner_id:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        owner_id = owner_id.replace(i, '')

                owner_id = int(owner_id)





                ref_money = cur.execute(f'SELECT ref_money FROM money WHERE user_id=?', (owner_id,)).fetchone()
                ref_money = str(ref_money)

                for i in ref_money:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        ref_money = ref_money.replace(i, '')

                ref_money = int(ref_money)

                ref_money_to_add = (ref_money_procent / 100) * money
                ref_money_to_add = int(ref_money_to_add)

                ref_money += ref_money_to_add

                cur.execute(f'UPDATE money SET ref_money=? WHERE user_id=?', (ref_money, owner_id))
                bd.commit()

                listid.append(owner_id)

                ref_money_procent -= 2


            elif availability == '':
                break


        elif ref_money_procent == 0:
            break










        #
#
#
#
#


# total process
print('Bot "import buttons" is ON')


#
#
#
#
#


us_id: dict = {'us_id': 0}


@dp.message(CommandStart())
async def start_process(message: Message):
    await message.answer('👋*Приветсвуем!*\n\n💥*Следите за свежими новостями и бонусами в нашем новостном канале:*', reply_markup=start,  parse_mode='Markdown')
    us_id['us_id'] = message.from_user.id


@dp.callback_query(Text(text='start'))
async def add_money_to_invest(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(text='👇 Нажмите start для начала работы.', reply_markup=keyboard_start)


@dp.message(Text(text='start'))
async def start_process(message: Message):
    await message.answer(
        "👋 Рады приветствовать!\n\n🔹Arbitrage Income - зарабатывает на P2P связках, где ты можешь открыть депозит и получать пассивный доход\n\n🚀 "
        "Выберите нужный пункт меню:\n\nПоддержка: @Arbitrageincome_support", reply_markup=keyboard_main_buttons)

    user_id = message.from_user.id
    user_info['user_id'] = user_id
    referral_link = message.text.strip()
    user_money = 0
    user_name = message.from_user.username
    user_info['user_name'] = user_name



    cur.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
    bd.commit()



    # Work with money table
    result = check_tablemoney(user_id)

    if result[0] > 0:
        pass

    else:
        cur.execute(f'INSERT INTO money (user_id, user_money, ref_money) VALUES (?, ?, ?)', (user_id, user_money, 0))
        bd.commit()
        print('money table was created')




    # Work with referals link
    cur.execute("SELECT * FROM referrals WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if row is None:

        ref_link = generate_ref_link()
        cur.execute("INSERT INTO referrals (user_id, ref_link, user_name, invited_by, lvl_one, lvl_two, lvl_three, use_referal_id, adm_allow, deposit, accumulated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, ref_link, user_name, '', 0, 0, 0, 0, 0, 0, 0))
        bd.commit()

    else:
        ref_link = row[1]

    referal_link = f"https://t.me/ArbitrageIncome_bot?start={ref_link}"
    info_about_referals['referal_link'] = referal_link


    #
    #
    #
    #


    listd = referral_link.split(' ')

    referral_link = listd[1]
    print(referral_link)

    #

    cur.execute("SELECT user_id FROM referrals WHERE ref_link=?", (referral_link,))
    id = cur.fetchone()

    id = str(id)

    for i in id:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            id = id.replace(i, '')

    id = int(id)
    info_about_referals['id_link_owner'] = id

    #

    print('cсылка профиля - ', ref_link)
    print('айдишка профиля', id)
    print('чекер на есть ли рефералка -', referral_link)
    print('-------------------')

    #


    cur.execute("SELECT use_referal_id FROM referrals WHERE user_id=?", (user_id,))
    use_referal_id = cur.fetchone()
    use_referal_id = str(use_referal_id)

    for i in use_referal_id:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            use_referal_id = use_referal_id.replace(i, '')

    use_referal_id = int(use_referal_id)
    print(use_referal_id)


    if referral_link != '' and use_referal_id == 0 and user_id != info_about_referals['id_link_owner']:
        # Отправляем уведомление владельцу ссылки
        await bot.send_message(chat_id=id,
                               text=f"💰 Пользователь {message.from_user.username} перешел по вашей реферальной ссылке.\nВам начислено 3 руб 💰")

        balance_info['temporary_money_from_invite'] += 3
        info_about_referals['invited_by'] = referral_link

        add_to_table_referal_link()
        add_temporary_money_to_table()
        update_referal_lvls()
        update_use_referal_id()

        print('-------------------')

    else: await message.answer('❗ Повторный вход через реферальную ссылку или же вход через свою же реферальную ссылку запрещен ❗')



#
#
#
#

# HENDLERS TO COMMANDS








@dp.message(Text(text='💸 Мой вклад'))
async def button_show_personal_cash(message: Message):
    user_id = message.from_user.id
    deposit, accumulated, money_per_dey = calculate_function(user_id)
    print(deposit, accumulated, money_per_dey)

    photo_url = "https://i.ibb.co/n0bkXw7/deposit.jpg"
    await bot.send_photo(user_id, photo=photo_url,
                         caption= f'▫️*В этом разделе вы можете открыть депозит и реинвестировать прибыль*\n\n💵 Процент прибыли: *3%*\n\n⌛ Начисление процентов: *В 15:00 МСК*\n\n🗓️ Срок вклада: *Бессрочный*\n\n🔵 Тело депозита: *{deposit}₽*\n💸 Накоплено: *{accumulated}₽*\n\n💰 Прибыль в день: *{money_per_dey}₽*',
        parse_mode='Markdown', reply_markup=my_invest_buttons)


#Work with add_invest
@dp.callback_query(Text(text='add_balance_in_my_invest'))
async def add_money_to_invest(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text='👇 Выберите счет, денежные средства с которого вы хотите использовать:',
        reply_markup=invest_from)


#main balance
@dp.message(Text(text='💼 Основной баланс'))
async def invest_from_main_balance(message: Message):
    user_id = message.from_user.id


    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)

    if user_money >= 1000:
        await message.answer(f'💰 Ваш баланс составляет - {user_money}₽\n\nВведите нужную сумму:')
        wait_buttons['wait_money_from_mainbalance_to_invest'] = True

    elif user_money < 1000:
        await message.answer('')


@dp.message(lambda x: x.text and wait_buttons['wait_money_from_mainbalance_to_invest'] == True and x.text.isdigit())
async def process_ask_sum_to_add(message: Message):
    wait_buttons['wait_money_from_mainbalance_to_invest'] = False
    user_id = message.from_user.id
    sum = message.text
    sum = int(sum)
    print('YEEEEEEEE', sum)

    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)


    cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (user_id,))
    deposit = cur.fetchone()
    deposit = str(deposit)

    for i in deposit:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            deposit = deposit.replace(i, '')

    deposit = int(deposit)


    if sum <= user_money:
        user_money -= sum
        cur.execute(f'UPDATE money SET user_money=? WHERE user_id=?', (user_money, user_id))
        bd.commit()


        deposit += sum
        cur.execute(f'UPDATE referrals SET deposit=? WHERE user_id=?', (deposit, user_id))
        bd.commit()


        await message.answer('✅ Средства успешно были зачислены на ваш инвестиционный счет', reply_markup=keyboard_main_buttons)



    elif sum > user_money:
        await message.answer('🔴 Введенная сумма превышает количество денеждных средств на вашем балансе!')






@dp.message(Text(text='🗃 Реферальный баланс'))
async def invest_from_ref_balance(message: Message):
    user_id = message.from_user.id


    cur.execute("SELECT ref_money FROM money WHERE user_id=?", (user_id,))
    ref_money = cur.fetchone()
    ref_money = str(ref_money)

    for i in ref_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            ref_money = ref_money.replace(i, '')

    ref_money = int(ref_money)

    if ref_money >= 1000:
        await message.answer(f'💰 Ваш реферальный баланс составляет - {ref_money}₽\n\nВведите нужную сумму:')
        wait_buttons['wait_money_from_refbalance_to_invest'] = True

    elif ref_money < 1000:
        await message.answer('')




@dp.message(lambda x: x.text and wait_buttons['wait_money_from_refbalance_to_invest'] == True and x.text.isdigit())
async def process_ask_sum_to_addref(message: Message):
    wait_buttons['wait_money_from_refbalance_to_invest'] = False
    user_id = message.from_user.id
    sum = message.text
    sum = int(sum)
    print('YEEEEEEEE, ref_sum - ', sum)

    cur.execute("SELECT ref_money FROM money WHERE user_id=?", (user_id,))
    ref_money = cur.fetchone()
    ref_money = str(ref_money)

    for i in ref_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            ref_money = ref_money.replace(i, '')

    ref_money = int(ref_money)


    cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (user_id,))
    deposit = cur.fetchone()
    deposit = str(deposit)

    for i in deposit:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            deposit = deposit.replace(i, '')

    deposit = int(deposit)


    if sum <= ref_money:
        ref_money -= sum
        cur.execute(f'UPDATE money SET ref_money=? WHERE user_id=?', (ref_money, user_id))
        bd.commit()


        deposit += sum
        cur.execute(f'UPDATE referrals SET deposit=? WHERE user_id=?', (deposit, user_id))
        bd.commit()


        await message.answer('✅ Средства успешно были зачислены на ваш инвестиционный счет', reply_markup=keyboard_main_buttons)



    elif sum > ref_money:
        await message.answer('🔴 Введенная сумма превышает количество денеждных средств на вашем балансе!')












#Work with take_invest
@dp.callback_query(Text(text='take_balance_in_my_invest'))
async def take_money_from_invest(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text='💸 Введите сумму которую хотите вывести:')

    wait_buttons['wait_sum_to_take_back_from_invest_to_mainbalance'] = True



@dp.message(lambda x: x.text and wait_buttons['wait_sum_to_take_back_from_invest_to_mainbalance'] == True and x.text.isdigit())
async def process_ask_sum_to_add(message: Message):
    wait_buttons['wait_sum_to_take_back_from_invest_to_mainbalance'] = False
    sum = message.text
    sum = int(sum)
    user_id = message.from_user.id

    cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (user_id,))
    deposit = cur.fetchone()

    deposit = str(deposit)
    for i in deposit:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            deposit = deposit.replace(i, '')

    deposit = int(deposit)

    if sum <= deposit:
        deposit -= sum

        cur.execute(f'UPDATE referrals SET deposit=? WHERE user_id=?', (deposit, user_id))
        bd.commit()


        cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
        user_money = cur.fetchone()
        user_money = str(user_money)

        for i in user_money:
            if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                user_money = user_money.replace(i, '')

        user_money = int(user_money)


        user_money += sum

        cur.execute(f'UPDATE money SET user_money=? WHERE user_id=?', (user_money, user_id))
        bd.commit()



        await message.answer('✅ Средства успешно были зачислены на ваш счет', reply_markup=keyboard_main_buttons)



    elif sum > deposit:
        await message.answer('🔴 Введенная сумма превышает количество денеждных средств на вашем депозитном счете!')




@dp.callback_query(Text(text='update_balance_in_my_invest'))
async def take_money_from_invest(message: Message):
    user_id = message.from_user.id

    cur.execute("SELECT accumulated FROM referrals WHERE user_id=?", (user_id,))
    accumulated = cur.fetchone()
    accumulated = str(accumulated)

    for i in accumulated:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            accumulated = accumulated.replace(i, '')

    accumulated = int(accumulated)

    cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (user_id,))
    deposit = cur.fetchone()
    deposit = str(deposit)

    for i in deposit:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            deposit = deposit.replace(i, '')

    deposit = int(deposit)


    deposit += accumulated


    cur.execute(f'UPDATE referrals SET deposit=? WHERE user_id=?', (deposit, user_id))
    bd.commit()

    cur.execute(f'UPDATE referrals SET accumulated=? WHERE user_id=?', (0, user_id))
    bd.commit()

    await bot.send_message(user_id, '✅ Средства с накопительного счета были успешно реинвестированы', reply_markup=keyboard_main_buttons)




@dp.message(Text(text='🚹 Партнеры'))
async def button_show_connected_users(message: Message):
    info_about_referals_function(message)

    user_id = message.from_user.id

    cash_from_invite = info_about_referals['cash_from_invite']
    invited = info_about_referals['invited']
    referal_link = info_about_referals['referal_link']
    invited_by = info_about_referals['invited_by']



    photo_url = "https://i.ibb.co/87MbWdn/gues.jpg"
    await bot.send_photo(user_id, photo=photo_url, caption= f'▫️В этом разделе вы можете проверять свои реферальные деньги. Приглашайте друзей и получайте по 3₽ за активацию робота\n\n💵 За депозит каждого реферала предусматривается 3 уровня: 10-5-2%\n\n💰 Всего заработано: {cash_from_invite}₽\n👥 Рефералов: {invited} чел\n👤 Вас пригласил: - {invited_by}')

    await message.answer(
        f'🔗 Ваша реферальная ссылка: {referal_link}',
        reply_markup=markup1, disable_web_page_preview=True)


@dp.callback_query(Text(text='more'))
async def process_more_press(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text='👤 Вы приглашаете человека по реф ссылке\n\n📩 Когда кто-то переходит по ссылке он становится Вашим партнёром\n\n💶 За внесение средств каждым партнёром предусматривается 3 уровня бонуса: 7-4-3% от суммы пополнения партнёра',
        reply_markup=markup2)


# Этот хэндлер будет срабатывать на нажатие кнопки "Хочу еще!"
@dp.callback_query(Text(text='back'))
async def process_back(callback: CallbackQuery):

    cash_from_invite = info_about_referals['cash_from_invite']
    invited = info_about_referals['invited']
    referal_link = info_about_referals['referal_link']
    invited_by = info_about_referals['invited_by']

    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text=f'🔗 Ваша реферальная ссылка: {referal_link}',
        reply_markup=markup1, disable_web_page_preview=True)







@dp.message(Text(text='📚 Дополнительно'))
async def button_show_personal_cash(message: Message):
    user_id = message.from_user.id

    rand = randint(136, 249)

    cur.execute("SELECT investors FROM fakes")
    investors = cur.fetchone()


    investors = str(investors)

    for i in investors:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            investors = investors.replace(i, '')

    investors = int(investors)


    cur.execute("SELECT investors_online FROM fakes")
    investors_online = cur.fetchone()

    investors_online = str(investors_online)

    for i in investors_online:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            investors_online = investors_online.replace(i, '')

    investors_online = int(investors_online)


    cur.execute("SELECT all_sum FROM fakes")
    all_sum = cur.fetchone()

    all_sum = str(all_sum)

    for i in all_sum:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            all_sum = all_sum.replace(i, '')

    all_sum = int(all_sum)

    investors += rand
    investors_online += rand
    all_sum += rand

    cur.execute(f'UPDATE fakes SET investors=?',
                (investors,))
    bd.commit()

    cur.execute(f'UPDATE fakes SET investors_online=?',
                (investors_online,))
    bd.commit()

    cur.execute(f'UPDATE fakes SET all_sum=?',
                (all_sum,))
    bd.commit()


    print(investors, investors_online, all_sum)

    photo_url = "https://i.ibb.co/sb1Rg0x/more.jpg"
    await bot.send_photo(user_id, photo=photo_url,
                         caption=f'▫️ *Здесь можно ознакомиться с дополнительной информацией*\n\n💎 Начало работы: 21.02.2023\n\n💰 Общая сумма вклада всех инвесторов: {all_sum}₽\n🙍‍♂️ Всего инвесторов: {investors} чел\n🟢 Онлайн инвесторов: {investors_online}', reply_markup=support, parse_mode='Markdown')


@dp.message(Text(text='💵 Баланс'))
async def button_show_personal_cash(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_info['user_id'] = user_id
    user_info['user_name'] = user_name





    cur.execute("SELECT id FROM orders_usdt_tethe WHERE user_id=?", (user_id,))
    id = cur.fetchone()
    id = str(id)

    for i in id:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            id = id.replace(i, '')


    if id == "None":

        cur.execute("INSERT INTO orders_usdt_tethe (user_id, id, wallet, sum) VALUES (?, ?, ?, ?)", (user_id, 0, '', 0))
        bd.commit()




    cur.execute("SELECT id FROM orders_kiwi WHERE user_id=?", (user_id,))
    id2 = cur.fetchone()
    id2 = str(id2)

    for i in id2:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            id2 = id.replace(i, '')

    if id2 == "None":
        cur.execute("INSERT INTO orders_kiwi (user_id, id, wallet, sum) VALUES (?, ?, ?, ?)", (user_id, 0, '', 0))
        bd.commit()





    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)
    print(user_money)

    photo_url = "https://i.ibb.co/wcmykXD/balancenew.jpg"
    await bot.send_photo(user_id, photo=photo_url,
                         caption= f'▫️*Здесь вы можете пополнить ваш баланс и вывести заработанные средства*\n\n📝 Инвестор: {user_name}\n🆔 Ваш ID: {user_id}\n\n💰 Ваш текущий баланс: *{user_money}₽*\n\n👥 Партнёров: 0 чел.', parse_mode='Markdown', reply_markup=balance_work)



@dp.callback_query(Text(text='add_balance'))
async def process_add_balance_and_show_typesTOADD(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text='💷 Выберите способ пополнения:',
        reply_markup=add_balance_buttons)


@dp.callback_query(Text(text='add_balance_process1'))
async def process_add_balance1(message: Message):
    await bot.send_message(user_info['user_id'], '👇 *Введите цифрами сумму пополнения:*', parse_mode='Markdown')
    wait_buttons['add_balance1'] = True

@dp.message(lambda x: x.text and wait_buttons['add_balance1'] == True and x.text.isdigit())
async def process_ask_sum_to_add(message: Message):
    wait_buttons['add_balance1'] = False
    sum = message.text
    print(sum)
    sum = int(sum)

    max_sum = 40000
    min_sum = 1000

    if sum >= max_sum:
        await message.answer('❗ *Сумма пополнения превышает 40000₽* \n\n📩 *Для оплаты обратитесь в поддержку*', reply_markup=max, parse_mode='Markdown')

    elif sum < min_sum:
        await message.answer('❗ *Минимальная сумма пополнения 1000₽*',
                             reply_markup=back, parse_mode='Markdown')

    else:
        await message.answer(f'🔹 Способ пополнения: *Usdt Tether 20 *\n\n💵 Usdt Tether 20 кошелек:\nTMfp3kYVU3hQ5dnJv2Dy5DLYpxD6SMpbJY\n💸 Сумма к переводу:*{sum}*₽\n🚀 Вместе со скриншотом в поддержку отправьте ваш ID. Его вы можете узнать перейдя во вкладку баланс.\n\n💎 *После оплаты отправьте скриншот в поддержку*',
                             reply_markup=accept, parse_mode='Markdown')



@dp.callback_query(Text(text='add_balance_process2'))
async def process_add_balance1(message: Message):
    await bot.send_message(user_info['user_id'], '👇 *Введите цифрами сумму пополнения:*', parse_mode='Markdown')
    wait_buttons['add_balance2'] = True

@dp.message(lambda x: x.text and wait_buttons['add_balance2'] == True and x.text.isdigit())
async def process_ask_sum_to_add(message: Message):
    wait_buttons['add_balance2'] = False
    sum = message.text
    print(sum)
    sum = int(sum)

    max_sum = 40000
    min_sum = 1000

    if sum >= max_sum:
        await message.answer('❗ *Сумма пополнения превышает 40000₽* \n\n📩 *Для оплаты обратитесь в поддержку*', reply_markup=max, parse_mode='Markdown')

    elif sum < min_sum:
        await message.answer('❗ *Минимальная сумма пополнения 1000₽*',
                             reply_markup=back, parse_mode='Markdown')

    else:
        await message.answer(f'💵 Способ пополнения: *Киви кошелек*\n\n🥝 Киви кошелек: 89265275416\n💸 Сумма к переводу:*{sum}*₽\n🚀 Вместе со скриншотом в поддержку отправьте ваш ID. Его вы можете узнать перейдя во вкладку "баланс".\n\n💎 *После оплаты отправьте скриншот в поддержку*',
                             reply_markup=accept, parse_mode='Markdown')



@dp.callback_query(Text(text='another_type_to_add_balance'))
async def get_back_after_add_balance(message: Message):
    await bot.send_message(user_info['user_id'], '⚒ *Для пополнения другими способами обратитесь в поддержку*', parse_mode='Markdown', reply_markup=another_type_to_add_balance)



@dp.callback_query(Text(text='get_back_after_addBalance'))
async def get_back_after_add_balance(callback: CallbackQuery):
    user_name = user_info['user_name']
    user_id = user_info['user_id']
    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_info['user_id'],))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)


    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(f'▫️*Здесь вы можете пополнить ваш баланс и вывести заработанные средства*\n\n📝 Инвестор: {user_name}\n🆔 Ваш ID: {user_id}\n\n💰 Ваш текущий баланс: *{user_money}₽*\n\n👥 Партнёров: 0 чел.', parse_mode='Markdown', reply_markup=balance_work)



@dp.callback_query(Text(text='wait_to_accept_money'))
async def process_wait_to_accept(message: Message):
    await message.answer('🕒 Ожидайте подтверждения:')


    #
    #


@dp.callback_query(Text(text='take_balance'))
async def process_add_balance_and_show_typesTOADD(callback: CallbackQuery):
    user_id = user_info['user_id']

    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)

    if 300 <= user_money:

        # Отвечаем на callback, чтобы убрать часики
        await callback.message.delete()
        # Отправляем в чат новое сообщение с шуткой
        await callback.message.answer(
            text='💷 Выберите способ вывода средств:',
            reply_markup=take_money_back_buttons)

    elif 300 > user_money:
        await callback.message.answer('🔴 Минимальная сумма вывода - 300₽')



@dp.callback_query(Text(text='take_balance_process1'))
async def process_take_balance1(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text='👇 Введите Usdt Tether 20 кошелек:')

    wait_buttons['wait_process_take_money_1'] = True


@dp.message(lambda x: x.text and wait_buttons['wait_process_take_money_1'] == True)
async def process_ask_sum_to_add(message: Message):
    wait_buttons['wait_process_take_money_1'] = False

    user_id = message.from_user.id
    user_wallet = message.text
    user_info['user_wallet'] = user_wallet

    await message.answer('📨 Введите сумму для вывода средств')

    wait_buttons['wait_process_take_money_2'] = True

@dp.message(lambda x: x.text and wait_buttons['wait_process_take_money_2'] == True and x.text.isdigit())
async def process_ask_sum_to_add(message: Message):
    wait_buttons['wait_process_take_money_2'] = False
    user_wallet = user_info['user_wallet']
    user_info['user_wallet'] = ''

    user_id = message.from_user.id
    money_to_take = message.text
    money_to_take = int(money_to_take)


    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)


    cur.execute("SELECT id FROM orders_usdt_tethe WHERE user_id=?", (user_id,))
    id = cur.fetchone()
    id = str(id)

    for i in id:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            id = id.replace(i, '')

    id = int(id)


    if money_to_take > user_money or id == 1:
        await message.answer('🔴 *На вашем счету недостаточно средств или на данный момент, вами уже отправлена заявка данным способом!*\n\n*Попробуйте еще раз или же выберите другой способ*', parse_mode='Markdown', reply_markup=keyboard_main_buttons)

    elif money_to_take <= user_money and id == 0:
        cur.execute(f'UPDATE orders_usdt_tethe SET id=? WHERE user_id=?', (1, user_id))
        bd.commit()

        cur.execute(f'UPDATE orders_usdt_tethe SET wallet=? WHERE user_id=?', (user_wallet, user_id))
        bd.commit()

        cur.execute(f'UPDATE orders_usdt_tethe SET sum=? WHERE user_id=?', (money_to_take, user_id))
        bd.commit()

        await message.answer('🕒 *Заявка на вывод средств получена.*\n\n💭 *Ожидайте в течении 24 часов.*\n\n💬 *Если средства переведены не будут - обратитесь в поддержку*', parse_mode='Markdown', reply_markup=keyboard_main_buttons)


    #


@dp.callback_query(Text(text='take_balance_process2'))
async def process_take_balance2(callback: CallbackQuery):
    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(
        text='👇 Введите Киви кошелек:')

    wait_buttons['wait_process_take_money_3'] = True


@dp.message(lambda x: x.text and wait_buttons['wait_process_take_money_3'] == True)
async def process_ask_sum_to_take(message: Message):
    wait_buttons['wait_process_take_money_3'] = False

    user_id = message.from_user.id
    user_wallet = message.text
    user_info['user_wallet'] = user_wallet

    await message.answer('📨 Введите сумму для вывода средств')

    wait_buttons['wait_process_take_money_4'] = True





@dp.message(lambda x: x.text and wait_buttons['wait_process_take_money_4'] == True and x.text.isdigit())
async def process_ask_sum_to_take2(message: Message):
    wait_buttons['wait_process_take_money_4'] = False
    user_wallet = user_info['user_wallet']
    user_info['user_wallet'] = ''

    user_id = message.from_user.id
    money_to_take = message.text
    money_to_take = int(money_to_take)


    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)


    cur.execute("SELECT id FROM orders_kiwi WHERE user_id=?", (user_id,))
    id = cur.fetchone()
    id = str(id)

    for i in id:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            id = id.replace(i, '')

    id = int(id)


    if money_to_take > user_money or id == 1:
        await message.answer('🔴 *На вашем счету недостаточно средств или на данный момент, вами уже отправлена заявка данным способом!*\n\n*Попробуйте еще раз или же выберите другой способ*', parse_mode='Markdown', reply_markup=keyboard_main_buttons)

    elif money_to_take <= user_money and id == 0:
        cur.execute(f'UPDATE orders_kiwi SET id=? WHERE user_id=?', (1, user_id))
        bd.commit()

        cur.execute(f'UPDATE orders_kiwi SET wallet=? WHERE user_id=?', (user_wallet, user_id))
        bd.commit()

        cur.execute(f'UPDATE orders_kiwi SET sum=? WHERE user_id=?', (money_to_take, user_id))
        bd.commit()

        await message.answer('🕒 *Заявка на вывод средств получена.*\n\n💭 *Ожидайте в течении 24 часов.*\n\n💬 *Если средства переведены не будут - обратитесь в поддержку*', parse_mode='Markdown', reply_markup=keyboard_main_buttons)






@dp.callback_query(Text(text='another_type_to_take_balance'))
async def get_back_after_add_balance(message: Message):
    await bot.send_message(user_info['user_id'], '⚒ *Для вывода средств другими способами обратитесь в поддержку*', parse_mode='Markdown', reply_markup=another_type_to_add_balance)



@dp.callback_query(Text(text='get_back_after_addBalance'))
async def get_back_after_add_balance(callback: CallbackQuery):
    user_name = user_info['user_name']
    user_id = user_info['user_id']
    cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_info['user_id'],))
    user_money = cur.fetchone()
    user_money = str(user_money)

    for i in user_money:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            user_money = user_money.replace(i, '')

    user_money = int(user_money)


    # Отвечаем на callback, чтобы убрать часики
    await callback.message.delete()
    # Отправляем в чат новое сообщение с шуткой
    await callback.message.answer(f'▫️*Здесь вы можете пополнить ваш баланс и вывести заработанные средства*\n\n📝 Инвестор: {user_name}\n🆔 Ваш ID: {user_id}\n\n💰 Ваш текущий баланс: *{user_money}₽*\n\n👥 Партнёров: 0 чел.', parse_mode='Markdown', reply_markup=balance_work)


#
#
#


@dp.message(Text(text='📈 Рассчитать'))
async def calculator(message: Message):
    user_id = message.from_user.id
    photo_url = "https://i.ibb.co/vQQgcBp/calculate.jpg"
    await bot.send_photo(user_id, photo=photo_url, caption='▫️ *Здесь вы можете рассчитать вашу прибыль*\n\n👇 Выберите функцию калькулятора:', parse_mode='Markdown', reply_markup=calculator_keyboard)


@dp.message(Text(text='💸 Рассчитать сумму вклада'))
async def calculate_sum(message: Message):
    await message.answer('Введите сумму для расчёта:')
    wait_buttons['calculate_sum'] = True


@dp.message(lambda x: x.text and wait_buttons['calculate_sum'] == True and x.text.isdigit())
async def calculate_sum_text(message: Message):
    wait_buttons['calculate_sum'] = False
    sum = message.text
    sum = int(sum)

    if sum >= 1000:
        money_per_day = (3 / 100) * sum
        money_per_day = int(money_per_day)

        money_per_month = (90 / 100) * sum
        money_per_month = int(money_per_month)

        money_per_year = (1095 / 100) * sum
        money_per_year = int(money_per_year)

        await message.answer('🔁 Обрабатываю запрос...')
        await message.answer(f"✅ *Успешно рассчитано!*\n\n💶 Сумма вклада: *{sum}₽*\n📈 Процент прибыли: *3%*\n\n▫️ Прибыль в день: *{money_per_day}*₽\n▫️ Прибыль в месяц: *{money_per_month}*₽\n▫️ Прибыль в год: *{money_per_year}*₽", parse_mode='Markdown', reply_markup=keyboard_main_buttons)

    elif sum < 1000:
        await message.answer('❌ Минимальная сумма инвестиции: 1000₽', reply_markup=calculator_keyboard)



@dp.message(Text(text='🔄️ Рассчитать сумму вклада с ежедневным реинвестированием'))
async def calculate_sum(message: Message):
    await message.answer('Введите сумму для расчёта:')
    wait_buttons['calculate_sum_with_reivest'] = True


@dp.message(lambda x: x.text and wait_buttons['calculate_sum_with_reivest'] == True and x.text.isdigit())
async def calculate_sum_text(message: Message):
    wait_buttons['calculate_sum_with_reivest'] = False
    sum = message.text
    sum = int(sum)

    if sum >= 1000:
        money_per_7_days = sum
        money_per_2_weeks = sum
        money_per_month = sum

        for _ in range(7):
            prc = (3 / 100) * money_per_7_days
            prc = int(prc)

            money_per_7_days += prc

        print(money_per_7_days)


        for _ in range(14):
            prc = (3 / 100) * money_per_2_weeks
            prc = int(prc)

            money_per_2_weeks += prc

        print(money_per_2_weeks
              )


        for _ in range(30):
            prc = (3 / 100) * money_per_month
            prc = int(prc)

            money_per_month += prc

        print(money_per_month)

        await message.answer('🔁 Обрабатываю запрос...')
        await message.answer(f'✅ *Успешно рассчитано!*\n\n💶 Сумма с реинвестированием: *{sum}*₽\n📈 Процент прибыли: *3%*\n\n▫️ Итоговое тело депозита за 7 дней: *{money_per_7_days}*₽\n▫️ Итоговое тело депозита за 2 недели: *{money_per_2_weeks}*₽\n▫️ Итоговое тело депозита за месяц: *{money_per_month}*₽', parse_mode='Markdown', reply_markup=keyboard_main_buttons)

    elif sum < 1000:
        await message.answer('❌ Минимальная сумма инвестиции: 1000₽', reply_markup=calculator_keyboard)



#
#


@dp.message(Text(text='🔥 Хочу зарабатывать'))
async def button_show_personal_cash(message: Message):
    user_id = message.from_user.id

    photo_url = "https://i.ibb.co/ZLWycmn/start.jpg"
    await bot.send_photo(user_id, photo=photo_url,
                         caption='▫️ *Здесь можно узнать как начать зарабатывать с проектом SpreadX*', parse_mode='Markdown', reply_markup=go_to_info)



#
#


# admin command
@dp.message(Text(text='/admin_log'))
async def button_show_personal_cash(message: Message):
    user_id = message.from_user.id

    # creating table
    bd.execute('CREATE TABLE IF NOT EXISTS {}(login TEXT, password TEXT)'.format('admins'))
    bd.commit()

    await message.answer('Введите ваш login:')

    wait_buttons['admin_time_to_answer_login'] = True


@dp.message(lambda x: x.text and wait_buttons['admin_time_to_answer_login'] == True)
async def agree_work_admin(message: Message):
    wait_buttons['admin_time_to_answer_login'] = False
    login = message.text


    password = cur.execute(f'SELECT password FROM admins WHERE login=?', (login,)).fetchone()
    password = str(password)

    for i in password:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            password = password.replace(i, '')

    print(password)

    if password != 'None':
        await message.answer('Введите ваш password:')
        wait_buttons['admin_time_to_answer_password'] = True
        admin_allow['password'] = password

    elif password == 'None':
        await message.answer('Аккаунта с таким login нету!')


@dp.message(lambda x: x.text and wait_buttons['admin_time_to_answer_password'] == True)
async def agree_work_admin(message: Message):
    user_id = message.from_user.id
    password = message.text
    wait_buttons['admin_time_to_answer_password'] = False

    if password == admin_allow['password']:
        await message.answer('🔺 Вы успешно авторизовались. Вам присвоен статус - администратор 🔺')

        cur.execute(f'UPDATE referrals SET adm_allow=? WHERE user_id=?', (1, user_id))
        bd.commit()

        await message.answer('🔷 Напишите /admin для использования админ-панели 🔷')

    elif password != admin_allow['password']:
        await message.answer('Неверный пароль!')

#
#

@dp.message(Text(text='/admin'))
async def process_work_with_adminPanel(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        print('+')
        print(user_id, 'авторизовался как администратор')
        await message.answer('📝 Вы находитесь в админ-панели:', reply_markup=keyboard_admin_buttons)

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')
        print('-')
        print(user_id, 'попытался зайти как администратор')


@dp.message(Text(text='Управление денежным потоком'))
async def work_with_money(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        await message.answer('Выберите действие:', reply_markup=keyboard_work_with_balances)

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')


@dp.message(Text(text='Зачислить деньги на счет'))
async def add_money_to_balance(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        await message.answer('Введите ID пользователя, на чей счет должны поступить деньги.')
        wait_buttons['wait_user_id'] = True

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')


@dp.message(lambda x: x.text and wait_buttons['wait_user_id'] == True and x.text.isdigit())
async def agree_work_admin(message: Message):
    wait_buttons['wait_user_id'] = False

    user_id_to_add_balance = message.text
    user_id_to_add_balance = int(user_id_to_add_balance)

    user_to_add_balance['user_id'] = user_id_to_add_balance

    wait_buttons['wait_sum_to_add'] = True

    await message.answer('Введите сумму к пополнению:')


@dp.message(lambda x: x.text and wait_buttons['wait_sum_to_add'] == True and x.text.isdigit())
async def agree_work_admin(message: Message):
    wait_buttons['wait_sum_to_add'] = False

    money_to_add = message.text
    money_to_add = int(money_to_add)

    user_to_add_balance['money_to_add'] = money_to_add

    try:
        money = cur.execute(f'SELECT user_money FROM money WHERE user_id=?', (user_to_add_balance['user_id'],)).fetchone()
        money = str(money)

        for i in money:
            if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                money = money.replace(i, '')

        money = int(money)

        user_to_add_balance['money_to_add'] += money

        cur.execute(f'UPDATE money SET user_money=? WHERE user_id=?', (user_to_add_balance['money_to_add'], user_to_add_balance['user_id']))
        bd.commit()






        add_procent(user_to_add_balance['user_id'], user_to_add_balance['money_to_add'])






        user_to_add_balance['user_id'] = 0
        user_to_add_balance['money_to_add'] = 0

        await message.answer('Счет успешно пополнен.')



        for i in range(0, len(listid)):
            await bot.send_message(listid[i], 'Вам был начислен процент от пополнения вашего партнера.')





    except:
        await message.answer('Произошла ошибка при пополнении!')


#
#


@dp.message(Text(text='Очередь на вывод'))
async def adm_work_with_taking_money(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        await message.answer('Выберите систему вывода:', reply_markup=keyboard_adminwork_take_money)

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')


@dp.message(Text(text='Usdt Tether 20'))
async def take_balance_admin_work_using_USDT20(message: Message):
    user_id = message.from_user.id

    await message.answer('Список пользователей в очередь на вывод средств:')

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        cur.execute(f'SELECT user_id FROM orders_usdt_tethe')
        users_to_take_money_fromUSDT20 = cur.fetchall()


        for i in range(0, len(users_to_take_money_fromUSDT20)):
            user = users_to_take_money_fromUSDT20[i]

            user = str(user)
            for i in user:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    user = user.replace(i, '')

            user = int(user)

            cur.execute('SELECT id FROM orders_usdt_tethe WHERE user_id=?', (user,))
            id = cur.fetchone()

            id = str(id)
            for i in id:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    id = id.replace(i, '')

            id = int(id)


            if id == 1:
                cur.execute('SELECT wallet FROM orders_usdt_tethe WHERE user_id=?', (user,))
                wallet = cur.fetchone()

                wallet = str(wallet)
                for i in wallet:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        wallet = wallet.replace(i, '')





                cur.execute('SELECT sum FROM orders_usdt_tethe WHERE user_id=?', (user,))
                sum = cur.fetchone()

                sum = str(sum)
                for i in sum:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        sum = sum.replace(i, '')




                await message.answer(f'Пользователь с ID {user} в очереди на вывод средств.\n\nКошелек - {wallet}\nСумма вывода - {sum}')
                await message.answer('-----------------------------------------', reply_markup=keyboard_admin_buttons)

            elif id == 0:
                pass


    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')








@dp.message(Text(text='Kiwi'))
async def take_balance_admin_work_using_Kiwi(message: Message):
    user_id = message.from_user.id

    await message.answer('Список пользователей в очередь на вывод средств:')

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        cur.execute(f'SELECT user_id FROM orders_kiwi')
        users_to_take_money_fromKIWI = cur.fetchall()


        for i in range(0, len(users_to_take_money_fromKIWI)):
            user = users_to_take_money_fromKIWI[i]

            user = str(user)
            for i in user:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    user = user.replace(i, '')

            user = int(user)

            cur.execute('SELECT id FROM orders_kiwi WHERE user_id=?', (user,))
            id = cur.fetchone()

            id = str(id)
            for i in id:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    id = id.replace(i, '')

            id = int(id)


            if id == 1:
                cur.execute('SELECT wallet FROM orders_kiwi WHERE user_id=?', (user,))
                wallet = cur.fetchone()

                wallet = str(wallet)
                for i in wallet:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        wallet = wallet.replace(i, '')





                cur.execute('SELECT sum FROM orders_kiwi WHERE user_id=?', (user,))
                sum = cur.fetchone()

                sum = str(sum)
                for i in sum:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        sum = sum.replace(i, '')




                await message.answer(f'Пользователь с ID {user} в очереди на вывод средств.\n\nКошелек - {wallet}\nСумма вывода - {sum}')
                await message.answer('-----------------------------------------', reply_markup=keyboard_admin_buttons)

            elif id == 0:
                pass


    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')







@dp.message(Text(text='Обновить информацию о счете'))
async def update_info_balance(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)


    if adm_allow == 1:
        await message.answer('Выберите площадку:', reply_markup=keyboard_choose_type_to_update_balances)

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')




@dp.message(Text(text='Orders_Usdt_Tethe'))
async def update_info_balance_Usdt_Tethe(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        await message.answer('Введите ID пользователя:')
        wait_buttons['process_wait_to_update_balance'] = True

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')


@dp.message(lambda x: x.text and wait_buttons['process_wait_to_update_balance'] == True and x.text.isdigit())
async def agree_work_admin(message: Message):
    wait_buttons['process_wait_to_update_balance'] = False

    user_id = message.text
    user_id = int(user_id)


    try:
        cur.execute(f'UPDATE orders_usdt_tethe SET id=? WHERE user_id=?',
                    (0, user_id))
        bd.commit()


        cur.execute(f'UPDATE orders_usdt_tethe SET wallet=? WHERE user_id=?',
                    ('', user_id))
        bd.commit()





        sum = cur.execute(f'SELECT sum FROM orders_usdt_tethe WHERE user_id=?',
                            (user_id,)).fetchone()
        sum = str(sum)

        for i in sum:
            if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                sum = sum.replace(i, '')

        sum = int(sum)



        money = cur.execute(f'SELECT user_money FROM money WHERE user_id=?',
                            (user_id,)).fetchone()
        money = str(money)

        for i in money:
            if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                money = money.replace(i, '')

        money = int(money)

        money -= sum



        cur.execute(f'UPDATE money SET user_money=? WHERE user_id=?',
                    (money, user_id))
        bd.commit()


        cur.execute(f'UPDATE orders_usdt_tethe SET sum=? WHERE user_id=?',
                    (0, user_id))
        bd.commit()


        await message.answer('Оффер на оплату был обработан успешно')
        await bot.send_message(user_id, '✅ Ваш оффер на вывод средств был обработан успешно!')

    except:
        await message.answer('Оффер на оплату был обработан неуспешно')



@dp.message(Text(text='Orders_Kiwi'))
async def update_info_balance_Kiwi(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        await message.answer('Введите ID пользователя:')
        wait_buttons['process_wait_to_update_balance2'] = True

    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')




@dp.message(lambda x: x.text and wait_buttons['process_wait_to_update_balance2'] == True and x.text.isdigit())
async def agree_work_admin2(message: Message):
    wait_buttons['process_wait_to_update_balance2'] = False

    user_id = message.text
    user_id = int(user_id)


    try:
        cur.execute(f'UPDATE orders_kiwi SET id=? WHERE user_id=?',
                    (0, user_id))
        bd.commit()


        cur.execute(f'UPDATE orders_kiwi SET wallet=? WHERE user_id=?',
                    ('', user_id))
        bd.commit()





        sum = cur.execute(f'SELECT sum FROM orders_kiwi WHERE user_id=?',
                            (user_id,)).fetchone()
        sum = str(sum)

        for i in sum:
            if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                sum = sum.replace(i, '')

        sum = int(sum)



        money = cur.execute(f'SELECT user_money FROM money WHERE user_id=?',
                            (user_id,)).fetchone()
        money = str(money)

        for i in money:
            if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                money = money.replace(i, '')

        money = int(money)

        money -= sum



        cur.execute(f'UPDATE money SET user_money=? WHERE user_id=?',
                    (money, user_id))
        bd.commit()


        cur.execute(f'UPDATE orders_kiwi SET sum=? WHERE user_id=?',
                    (0, user_id))
        bd.commit()


        await message.answer('Оффер на оплату был обработан успешно')
        await bot.send_message(user_id, '✅ Ваш оффер на вывод средств был обработан успешно!')

    except:
        await message.answer('Оффер на оплату был обработан неуспешно')


@dp.message(Text(text='Начислить проценты'))
async def inside_procent(message: Message):
    user_id = message.from_user.id

    adm_allow = cur.execute(f'SELECT adm_allow FROM referrals WHERE user_id=?', (user_id,)).fetchone()
    adm_allow = str(adm_allow)

    for i in adm_allow:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            adm_allow = adm_allow.replace(i, '')

    adm_allow = int(adm_allow)

    if adm_allow == 1:
        users = cur.execute(f'SELECT user_id FROM referrals').fetchall()
        print(users)

        for i in range(0, len(users)):
            a = users[i]

            a = str(a)
            for i in a:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    a = a.replace(i, '')

            a = int(a)

            try:

                await bot.send_message(a, '🚀 Вам был зачислен ежедневный процент.', reply_markup=keyboard_main_buttons)


                cur.execute("SELECT deposit FROM referrals WHERE user_id=?", (a,))
                deposit = cur.fetchone()
                deposit = str(deposit)

                for i in deposit:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        deposit = deposit.replace(i, '')

                deposit = int(deposit)


                cur.execute("SELECT accumulated FROM referrals WHERE user_id=?", (a,))
                accumulated = cur.fetchone()
                accumulated = str(accumulated)

                for i in accumulated:
                    if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                        accumulated = accumulated.replace(i, '')

                accumulated = int(accumulated)

                newAccumulated = (3 / 100) * deposit
                newAccumulated += accumulated


                cur.execute(f'UPDATE referrals SET accumulated=? WHERE user_id=?', (newAccumulated, a))
                bd.commit()

            except:
                print('error. this user uneccessible')




    elif adm_allow == 0:
        await message.answer('Вы не авторизованы как администратор. /admin_log')




#
#
#
#
#


# message to unknown commands or messages
@dp.message(lambda x: x.text)
async def process_login(message: Message):
    await message.answer("⁉ Произошла ошибка, вы использовали функции для которых я не предназначен или же вводили неправильное значение ⁉", reply_markup=keyboard_main_buttons)
    wait_buttons['add_balance1'] = False
    wait_buttons['add_balance2'] = False




if __name__ == '__main__':
    dp.run_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    asyncio.run(main())
