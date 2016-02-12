import logging
import os
from telegram import Updater
import subprocess
import configparser

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me")


def print_pdf(bot, update):
    document = update.message.document

    if document.mime_type == 'application/pdf':

        if not os.path.exists('../file_downloads'):
            os.makedirs('../file_downloads')

        file_id = document.file_id
        file = bot.getFile(file_id)

        file_path = '../file_downloads/{0}_{1}_{2}.PDF'.format(update.message.from_user.id,
                                                               document.file_name, update.message.date
                                                               )

        file.download(file_path)
        subprocess.call(['lp', file_path])

    else:
        bot.sendMessage(update.message.chat_id, text='Sorry currently only PDF is supported.')


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['authorization']['token']

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramMessageHandler(print_pdf)

    updater.start_polling()


if __name__ == '__main__':
    main()
