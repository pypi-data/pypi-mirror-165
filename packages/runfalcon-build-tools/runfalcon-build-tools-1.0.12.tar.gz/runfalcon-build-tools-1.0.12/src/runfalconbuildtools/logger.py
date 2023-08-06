from datetime import datetime

class Logger:

    def __init__(self, owner:str):
        self.owner = owner

    def get_log_message(self, type:str, message:str) -> str:
        now = datetime.now()
        msg:str = now.strftime("%d/%m/%Y %H:%M:%S")
        msg += ' ({owner})'.format(owner = self.owner)
        msg += ' - [{msg_type}]'.format(msg_type = type)
        msg += ' :: {the_message}'.format(the_message = message)
        return msg

    def print_message(self, message:str):
        print(message)

    def debug(self, message:str):
        self.print_message(self.get_log_message('debug', message))

    def info(self, message:str):
        self.print_message(self.get_log_message('info', message))

    def error(self, message:str):
        self.print_message(self.get_log_message('error', message))
        
    def error(self, message:str, error:any):
        self.print_message(self.get_log_message('error', message + '\n' + error))
