# Импорт библиотек
import os
import time
import traceback

from script.instagram import insta_download
from script.pinterest import pint_download
from script.send_video import send_videomsg
from script.tiktok import tiktok_download

try:
    import sqlite3
    import telebot
except ModuleNotFoundError:
    os.system("pip install requirements.txt")
    import telebot
    import sqlite3
from config import tgbot_token, id_admin

bot = telebot.TeleBot(tgbot_token)
print("Бот запущен!")  # Это для проверки, что бот запустился


@bot.message_handler(commands=['start'])  # Запуск бота
def start(message):
    con = sqlite3.connect("db/chats.db")  # Подключение к базе данных
    cur = con.cursor()  # Создание курсора

    result = cur.execute("""SELECT id FROM id""").fetchall()  # Получение всех айди из базы данных
    id_list = [elem[0] for elem in result]

    if message.chat.id not in id_list:  # Если айди нет в базе данных, то добавляем его
        cur.execute(
            f'''INSERT INTO id (id) VALUES({message.chat.id}) ''')
        con.commit()
    con.close()  # Закрытие базы данных

    bot.send_message(message.chat.id, "<b>Example</b> - бот для загрузки видео с Instagram*, TikTok и "
                                      "Pinterest\n"
                                      "<i>*Признана экстремистской организацией и запрещена на территории РФ</i>"
                                      "\n\n@st_mate0 - прародитель бота"
                                      "\nПо всем вопросам: @st_mate0"
                                      "\n\nПросто отправь мне ссылку!\n\n", parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def text_message(message):
    txt = message.text.split()
    if "www.instagram.com/reel" in txt[0] or "www.instagram.com/p" in txt[0]:
        msg = bot.send_message(message.chat.id, "Началась загрузка, примерное время ожидания 20 секунд...")
        if insta_download(txt[0], message.chat.id):
            send_videomsg(bot, message.chat.id, msg.message_id)
        else:
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.chat.id, "Ошибка, возможно вы отправили ссылку не на пост или рилс!\n "
                                              "\nЛибо сервер не смог обработать запрос")
    elif "tiktok.com" in txt[0]:
        msg = bot.send_message(message.chat.id, "Началась загрузка, примерное время ожидания 20 секунд...")
        if tiktok_download(txt[0], message.chat.id):
            send_videomsg(bot, message.chat.id, msg.message_id)
        else:
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.chat.id, "Ошибка, возможно вы отправили ссылку не на тикток!"
                                              ""
                                              "\n\nЛибо сервер не смог обработать запрос")
    elif "pinterest.com/pin/" in txt[0] or "pin.it" in txt[0]:
        msg = bot.send_message(message.chat.id, "Началась загрузка, примерное время ожидания 20 секунд...")
        if pint_download(txt[0], message.chat.id):
            send_videomsg(bot, message.chat.id, msg.message_id)
        else:
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.chat.id, "Ошибка, возможно вы отправили ссылку не на пин!"
                                              ""
                                              "\n\nЛибо сервер не смог обработать запрос")


def telegram_polling():
    try:
        bot.polling()  # Опрос сервера Telegram на предмет новых сообщений
    except Exception as e:
        bot.send_message(id_admin, text="restart bot")  # Отправка сообщения администратору о перезапуске бота
        traceback_error_string = traceback.format_exc()  # Здесь хранится информация об ошибке
        with open("Error.Log", "a") as myfile:  # Запись ошибки в файл Error.Log
            myfile.write("\r\n\r\n" + time.strftime(
                "%c") + "\r\n<<ERROR polling>>\r\n" + traceback_error_string + "\r\n<<ERROR polling>>")
        bot.stop_polling()  # Перезапуск бота
        time.sleep(10)
        telegram_polling()


if __name__ == '__main__':
    telegram_polling()  # Запуск бота
