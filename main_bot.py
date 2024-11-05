# main_bot.py

import os
import time
import traceback
import logging
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

import reinsulation_replacement  # Модуль для "Метода переизоляции с частичной заменой труб"
import selective_repair  # Модуль для "Метода выборочного ремонта"

from flask import Flask
from threading import Thread

# Настройка логирования
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# Получаем токен из переменной окружения
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

# ID администратора для отправки сообщений об ошибках
admin_chat_id = 1890861135  # Замените на ваш реальный chat_id

# Создание словаря для хранения введенных пользователем значений
user_data = {}

# Создание клавиатур
repair_methods_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
repair_methods_keyboard.add(
    KeyboardButton('Метод выборочного ремонта'),
    KeyboardButton('Метод переизоляции с частичной заменой труб')
)

# Путь к файлам с документацией и соответствующие подписи
documentation_files = [
    ('documentation/СТО Газпром 27.3-2.2-006-2023 Инструкция по оценке дефектов труб и СДТ.pdf', 'СТО Газпром 27.3-2.2-006-2023'),
    ('documentation/Таблицы СП 36(1).jpg', 'Таблицы 10 и 12 по СП 36.13330.2012'),
    ('documentation/Таблицы СП 36(2).jpg', 'Таблица 14 по СП 36.13330.2012')
]

# Функция для отправки файлов с документацией с подписями
def send_documentation_files(chat_id):
    try:
        for file_path, caption in documentation_files:
            with open(file_path, 'rb') as doc:
                bot.send_document(chat_id, doc, caption=caption)
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при отправке документации: {str(e)}')

# Функция для отправки отчёта об ошибке администратору
def send_error_report(bot, error, user=None):
    """
    Отправить сообщение об ошибке администратору с деталями об ошибке и пользователе.
    """
    error_message = f"Бот столкнулся с ошибкой:\n{error}"
    if user:
        error_message += (
            f"\nПользователь: {user.username or 'Без ника'}"
            f"\nИмя: {(user.first_name or '') + ' ' + (user.last_name or '')}".strip() +
            f"\nID: {user.id}"
        )
    bot.send_message(admin_chat_id, error_message)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message: Message):
    try:
        user_data[message.chat.id] = {}
        send_documentation_files(message.chat.id)  # Отправляем файлы при старте

        # Отправляем сообщение с инструкцией по возврату на предыдущий шаг
        bot.send_message(
            message.chat.id,
            'Если вы захотите отменить действие или вернуться на предыдущий шаг, отправьте боту сообщение "Назад".'
        )

        # Предлагаем выбрать метод ремонта
        bot.send_message(
            message.chat.id,
            'Какой метод ремонта оценки дефектов труб и СДТ при проведении ремонта участков вас интересует?',
            reply_markup=repair_methods_keyboard
        )
    except Exception as e:
        logging.error(f"Ошибка в команде /start: {e}")
        traceback.print_exc()
        send_error_report(bot, e, user=message.from_user)

# Обработчик выбора метода ремонта
@bot.message_handler(func=lambda message: message.text in [
    'Метод выборочного ремонта',
    'Метод переизоляции с частичной заменой труб'
])
def handle_repair_method(message: Message):
    try:
        chat_id = message.chat.id
        method = message.text
        user_data[chat_id]['repair_method'] = method
        if method == 'Метод переизоляции с частичной заменой труб':
            reinsulation_replacement.start_reinsulation_replacement(bot, message, user_data[chat_id])
        elif method == 'Метод выборочного ремонта':
            selective_repair.start_selective_repair(bot, message, user_data[chat_id])
        else:
            bot.send_message(
                chat_id,
                'Пожалуйста, выберите метод ремонта из предложенных вариантов.',
                reply_markup=repair_methods_keyboard
            )
    except Exception as e:
        logging.error(f"Ошибка при выборе метода ремонта: {e}")
        traceback.print_exc()
        send_error_report(bot, e, user=message.from_user)

# Главный обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message: Message):
    try:
        chat_id = message.chat.id
        if chat_id not in user_data:
            user_data[chat_id] = {}
        repair_method = user_data[chat_id].get('repair_method')
        if repair_method == 'Метод переизоляции с частичной заменой труб':
            reinsulation_replacement.handle_state(bot, message, user_data[chat_id])
        elif repair_method == 'Метод выборочного ремонта':
            selective_repair.handle_state(bot, message, user_data[chat_id])
        else:
            bot.send_message(chat_id, 'Пожалуйста, начните сначала, введя команду /start.')
    except Exception as e:
        logging.error(f"Ошибка в обработчике сообщений: {e}")
        traceback.print_exc()
        send_error_report(bot, e, user=message.from_user)

# Функции для запуска веб-сервера и поддержания работы бота
app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Запуск бота с обработкой исключений и автоматическим перезапуском
if __name__ == '__main__':
    keep_alive()
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            logging.error(f"Возникла ошибка: {e}")
            traceback.print_exc()
            send_error_report(bot, e)
            time.sleep(5)  # Подождать 5 секунд перед перезапуском
