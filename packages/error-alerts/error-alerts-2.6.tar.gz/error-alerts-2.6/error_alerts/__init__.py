import traceback
from telegram import Bot

class setup:
    def __init__(self, telegram_token, telegram_channel, full_error=False, raise_error=False, resend_repeat_errors=True):
        self.bot = Bot(token=telegram_token)
        self.channel = telegram_channel
        self.full_error = full_error
        self.raise_error = raise_error
        self.resend_repeat_errors = resend_repeat_errors
        self.last_error = None
    def send(self, title, exception):
        error = str(exception)
        if self.full_error:
            error = traceback.format_exc()
        message = f'{title}: {error}'
        if self.resend_repeat_errors or error != self.last_error:
            self.bot.send_message(self.channel, message[:4096])
            self.last_error = error
        print(message)
        print()
        if self.raise_error:
            raise Exception('Raiser') from exception
    def send_message(self, *messages):
        final_message = ''
        for message in messages:
            final_message += message
            final_message += ' '
        self.bot.send_message(self.channel, final_message)
        print(final_message)
        print()