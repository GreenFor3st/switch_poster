import os
import configparser
import telegram
import asyncio

from telegram.ext import Updater
from queue import Queue


class Poster:
    """
    Class downloads information from twitter and publishes it in a telegram group
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.__TOKEN = self.config['telegram']['token']
        self.__GROUP_ID = self.config['telegram']['id']

        self.bot = telegram.Bot(token=self.__TOKEN)
        self.updater = Updater(self.bot, update_queue=Queue())

    async def post_message(self, context):
        """
        Publishes tweets text on group Twitter.
        """
        message = f"{context}"
        await self.bot.send_message(chat_id=self.__GROUP_ID, text=message)

    async def post_picture(self, file_path):
        """
        Publishes tweets picture on group Twitter.
        """
        with open(file_path, 'rb') as file:
            await self.bot.send_photo(chat_id=self.__GROUP_ID, photo=file)
        os.remove(file_path)

    def start(self):
        self.updater.start_polling()


async def main():
    poster = Poster()
    await poster.post_message('test')


if __name__ == "__main__":
    asyncio.run(main())
