from decouple import config

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

        self.copy_to_channel = config('COPY_TO_CHANNEL')
        if self.copy_to_channel != 'me':
            self.copy_to_channel = int(self.copy_to_channel)

conf = Config()