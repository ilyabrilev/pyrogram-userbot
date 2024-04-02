import re
import logging
import json 
from typing import List
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from config import conf, ChannelConfig

logger = logging.getLogger("tggt")
logger.setLevel(conf.logging_level)
fh = logging.FileHandler("logs/app.log")
logger.addHandler(fh)

def forward_content(source_channel_ids: List[int], channels: List[ChannelConfig]):
    """
        Функция прослушивает новые сообщения из каналов source_channel_ids
        и отправляет их в channels, если совпадает регулярка
    """

    client = Client(name='app_client', api_id=conf.api_id, api_hash=conf.api_hash)
        
    def forward_message(client: Client, message: Message):
        """
            Отправка сообщения в свои каналы
        """

        print('new message: "', message.text, '"')
        logger.info('new message')
        logger.info(str(message))
        message_to_check = message.text or message.caption
        if not message_to_check:
            return
        
        for channel in channels:            
            if re.search(channel.regex, message_to_check):
                logger.info('found match, sending to ' + str(channel.channel_id))
                print('found match, sending to ' + str(channel.channel_id))
                message.forward(chat_id=channel.channel_id)
                if message.link:
                    client.send_message(chat_id=channel.channel_id, text=message.link)
            else:
                logger.info('message', message_to_check, 'doesnt match with ', channel.regex)

    def filter_channels(self, client, message: Message):
        """
            Фильтр сообщений. Обрабатываются только сообщения, при которых функция выдает True
        """

        #не пересылать собственные сообщения
        if conf.block_outgoing:
            if message.outgoing:
                return False
        # Пока пересылать всё из интересующих каналов
        return message.chat.id in source_channel_ids

    filter_data = filters.create(filter_channels)
    client.add_handler(MessageHandler(forward_message, filter_data))

    client.run()
    
if __name__ == '__main__':
    forward_content(conf.sources_ids, conf.channels)

