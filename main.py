import telebot
import threading
from time import sleep
import gspread


BOT_TOKEN = ""
BOT_INTERVAL = 0.01
BOT_TIMEOUT = 5
GOOGLE_SHEET_ID = ''
LIST_OF_USERS_ID = []


bot = telebot.TeleBot(BOT_TOKEN)
gc = gspread.service_account()
sh = gc.open_by_key(GOOGLE_SHEET_ID)


def bot_polling():
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")

            botactions(bot)

            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex:
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else:
            bot.stop_polling()
            print("Bot polling loop finished")
            break


def botactions(bot):
    @bot.message_handler(commands=["start"])

    def command_start(message):
        user_id = message.from_user.id
        bot.send_message(message.from_user.id, '''Hello! Choose one miss and send her number. hui
    1 - Some name 1
    2 - Some name 2
    3 - Some name 3
    4 - Some name 4
    5 - Some name 5
    6 - Some name 6''')

        if user_id not in LIST_OF_USERS_ID:
            LIST_OF_USERS_ID.append(user_id)
            bot.register_next_step_handler(message, get_vote)

        elif user_id in LIST_OF_USERS_ID:
            bot.send_message(message.from_user.id, 'Вы уже отдали голос!')



    def get_vote(message):
        global num
        num = message.text
        if (message.text == '1') or (message.text == '2') or (message.text == '3') or \
                (message.text == '4') or (message.text == '5') or (message.text == '6'):
            bot.send_message(message.from_user.id, 'Спасибо! Ваш голос учтен!')
            sh = gc.open_by_key(GOOGLE_SHEET_ID)
            sh.sheet1.append_row([num])
        else:
            bot.send_message(message.from_user.id, 'Выберите номер участницы!')
            bot.register_next_step_handler(message, get_vote)


polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break
