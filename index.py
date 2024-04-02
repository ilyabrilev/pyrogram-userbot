from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from config import conf
from typing import List

def forward_content(source_channel_ids: List[int], copy_to_channel_id: int):
    """
        Функция прослушивает новые сообщения из каналов source_channel_ids
        и отправляет их в copy_to_channel_id
    """

    client = Client(name='app_client', api_id=conf.api_id, api_hash=conf.api_hash)
        
    def forward_message(client: Client, message: Message):
        """
            Отправка сообщения в свой канал
        """

        print('new message: "', message.text, '"')
        message.forward(chat_id=copy_to_channel_id)
        if message.link:
            client.send_message(chat_id=copy_to_channel_id, text=message.link)

    def filter_channels(self, client, message: Message):
        """
            Фильтр сообщений. Обрабатываются только сообщения, при которых функция выдает True
        """

        #не пересылать собственные сообщения
        if conf.block_outgoing:
            if message.outgoing:
                return False
        # Пока пересылать всё из интересующих каналов
        print(message)
        return message.chat.id in source_channel_ids

    filter_data = filters.create(filter_channels)
    client.add_handler(MessageHandler(forward_message, filter_data))

    client.run()
    
if __name__ == '__main__':
    forward_content(conf.sources_ids, conf.copy_to_channel)

