from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo


start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='📩 Подписаться',
            url='https://t.me/arbitrageincome_invest'
        )
    ],
    [
        InlineKeyboardButton(
            text='✅ Продолжить',
            callback_data='start'
        )
    ]
])

start2: KeyboardButton = KeyboardButton(text='start')
keyboard_start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[start2]], resize_keyboard=True, one_time_keyboard=True)



#Main buttons
button_show_personal_cash: KeyboardButton = KeyboardButton(text='💸 Мой вклад')
button_to_teammeates: KeyboardButton = KeyboardButton(text='🚹 Партнеры')
button_other: KeyboardButton = KeyboardButton(text='📚 Дополнительно')
button_show_balance: KeyboardButton = KeyboardButton(text='💵 Баланс')
button_to_check_possibilities_to_earn: KeyboardButton = KeyboardButton(text='📈 Рассчитать')
button_to_show_possibilities: KeyboardButton = KeyboardButton(text='🔥 Хочу зарабатывать')



# Создание массивов кнопок для каждого ряда
row1 = [button_show_personal_cash, button_to_teammeates]
row2 = [button_other, button_show_balance]
row3 = [button_to_check_possibilities_to_earn, button_to_show_possibilities]

# Создание клавиатуры из трех рядов по две кнопки
keyboard_main_buttons: ReplyKeyboardMarkup  = ReplyKeyboardMarkup(keyboard=[row1, row2, row3], resize_keyboard=True, one_time_keyboard=False)





#Admins commands
button_to_agree: KeyboardButton = KeyboardButton(text='Да')
button_to_disagree: KeyboardButton = KeyboardButton(text='Нет')



# Создание клавиатуры из трех рядов по две кнопки
keyboard_admins: ReplyKeyboardMarkup  = ReplyKeyboardMarkup(keyboard=[[button_to_agree], [button_to_disagree]], resize_keyboard=True, one_time_keyboard=True)



#Add or take balance
balance_work = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='➕ Пополнить',
            callback_data='add_balance'
        ),
        InlineKeyboardButton(
            text='➖ Вывести',
            callback_data='take_balance'
        )
    ]
])





#Types to add balance
add_balance_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔹 Способ пополнения: Usdt Tether 20',
            callback_data='add_balance_process1'
        )
    ],
    [
        InlineKeyboardButton(
            text='🥝 Киви кошелек',
            callback_data='add_balance_process2'
        )
    ],

    [
        InlineKeyboardButton(
                    text='Другой способ',
                    callback_data='another_type_to_add_balance'
        )
    ],
    [
        InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='get_back_after_addBalance'
        )
    ]

])





#1
keyboard1: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text='⚙ Как это работает?', callback_data='more')]]

markup1: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard1)

#2
keyboard2: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]]

markup2: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard2)


#Button cancel, max, accept(balance work)


max = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔵 Перейти в поддержку',
            url='https://t.me/ArbitrageIncome_support'
        )
    ],
    [

        InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='get_back_after_addBalance'
        )
    ]
])



accept = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔵 Перейти в поддержку',
            url='https://t.me/svyaton_nstsnko'
        )
    ],
    [

        InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='get_back_after_addBalance'
        )
    ]
])


another_type_to_add_balance = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔵 Перейти в поддержку',
            url='https://t.me/ArbitrageIncome_support'
        )
    ],
    [

        InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='get_back_after_addBalance'
        )
    ]

])

back = InlineKeyboardMarkup(inline_keyboard=[
    [

        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='get_back_after_addBalance'
        )
    ]
])












#Button to work with take balance
take_money_back_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔹 Usdt Tether 20',
            callback_data='take_balance_process1'
        )
    ],
    [
        InlineKeyboardButton(
            text='🥝 Киви кошелек',
            callback_data='take_balance_process2'
        )
    ],

    [
        InlineKeyboardButton(
                    text='Другой способ',
                    callback_data='another_type_to_take_balance'
        )
    ],
    [
        InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='get_back_after_addBalance'
        )
    ]

])














#Menu admin buttons
button_to_work_with_money: KeyboardButton = KeyboardButton(text='Управление денежным потоком')
find_by_user_id: KeyboardButton = KeyboardButton(text='Найти пользователя по уникальному ID')
three: KeyboardButton = KeyboardButton(text='Начислить проценты')
four: KeyboardButton = KeyboardButton(text='four')
five: KeyboardButton = KeyboardButton(text='five')
six: KeyboardButton = KeyboardButton(text='six')



# Создание массивов кнопок для каждого ряда
row1 = [button_to_work_with_money, find_by_user_id]
row2 = [three, four]
row3 = [five, six]

# Создание клавиатуры из трех рядов по две кнопки
keyboard_admin_buttons: ReplyKeyboardMarkup  = ReplyKeyboardMarkup(keyboard=[row1, row2, row3], resize_keyboard=True, one_time_keyboard=True)



#work with money by admin panel
button_to_add_money_on_balance: KeyboardButton = KeyboardButton(text='Зачислить деньги на счет')
button_to_take_money_from_balance: KeyboardButton = KeyboardButton(text='Очередь на вывод')
button_to_clear_take_money_from_balance: KeyboardButton = KeyboardButton(text='Обновить информацию о счете')
workorders_usdt_tethe: KeyboardButton = KeyboardButton(text='Orders_Usdt_Tethe')
workkiwi: KeyboardButton = KeyboardButton(text='Orders_Kiwi')

keyboard_work_with_balances: ReplyKeyboardMarkup  = ReplyKeyboardMarkup(keyboard=[[button_to_add_money_on_balance], [button_to_take_money_from_balance], [button_to_clear_take_money_from_balance]], resize_keyboard=True, one_time_keyboard=True)

keyboard_choose_type_to_update_balances: ReplyKeyboardMarkup  = ReplyKeyboardMarkup(keyboard=[[workorders_usdt_tethe], [workkiwi]], resize_keyboard=True, one_time_keyboard=True)


#Systems to take money (buttons)
usdt_tether: KeyboardButton = KeyboardButton(text='Usdt Tether 20')
kiwi: KeyboardButton = KeyboardButton(text='Kiwi')

keyboard_adminwork_take_money: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[usdt_tether], [kiwi]], resize_keyboard=True, one_time_keyboard=True)








#Inline buttons in my invest
my_invest_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='➕ Вложить',
            callback_data='add_balance_in_my_invest'
        ),
        InlineKeyboardButton(
            text='➖ Собрать',
            callback_data='take_balance_in_my_invest'
        )
    ],
    [
        InlineKeyboardButton(
            text='⏯ Реинвестировать',
            callback_data='update_balance_in_my_invest'
        )
    ]
])


#ADD
invest_from_main_balance: KeyboardButton = KeyboardButton(text='💼 Основной баланс')
invest_from_referal_balance: KeyboardButton = KeyboardButton(text='🗃 Реферальный баланс')

invest_from: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[invest_from_main_balance], [invest_from_referal_balance]], resize_keyboard=True, one_time_keyboard=True)

#TAKE
take_invest_to_main_balance: KeyboardButton = KeyboardButton(text='🗃 Основной баланс')

take_invest_to: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[take_invest_to_main_balance]], resize_keyboard=True, one_time_keyboard=True)



#Calculator (buttons)
calculate_sum: KeyboardButton = KeyboardButton(text='💸 Рассчитать сумму вклада')
calculate_sum_with_reinvest: KeyboardButton = KeyboardButton(text='🔄️ Рассчитать сумму вклада с ежедневным реинвестированием')

calculator_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[calculate_sum], [calculate_sum_with_reinvest]], resize_keyboard=False, one_time_keyboard=True)


support = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔵 Перейти в поддержку',
            url='https://t.me/ArbitrageIncome_support'
        )
    ],
    [
        InlineKeyboardButton(
            text='📒 Информация о нас',
            url='https://telegra.ph/Arbitrage-Income-podrobnaya-informaciya-03-20'
        )
    ]
])

go_to_info = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='📝 Узнать о нас больше',
            url='https://telegra.ph/Arbitrage-Income-podrobnaya-informaciya-03-20'
        )
    ]
])