from decouple import config
import logging

class ChannelConfig:
    def __init__(self, regex, channel_id):
        self.regex = regex
        if channel_id == 'me':
            self.channel_id = channel_id
        else:
            self.channel_id = int(channel_id)
    
    def __str__(self):
        return str(self.channel_id) + ' ' + self.regex

class Config:
    def __init__(self):        
        self.api_id = config('API_ID')
        self.api_hash = config('API_HASH')
        self.block_outgoing = config('BLOCK_OUTGOING', default=False) #не пересылать собственные сообщения если True

        tmp_sources = config('SOURCE_CHANNELS').split(',')

        self.sources_ids = []
        for source in tmp_sources:
            if source == 'me':
                self.sources_ids.append(source)
            else:
                self.sources_ids.append(int(source))

        self.channels = []
        for i in range(config('MAX_REGEX', cast=int, default=10)):
            regex = config('REGEX_' + str(i), default=None)
            copy_to_channel = config('COPY_TO_CHANNEL_' + str(i), default=None)
            if regex and copy_to_channel:
                new_channel = ChannelConfig(regex, copy_to_channel)
                self.channels.append(new_channel)
                print('channel', str(i), 'config:', new_channel)

        logging_level = config('LOGGING_LEVEL', default='ERROR')

        if logging_level == 'DEBUG':
            self.logging_level = logging.ERROR
        elif logging_level == 'INFO':
            self.logging_level = logging.ERROR
        else: 
            self.logging_level = logging.ERROR

conf = Config()