import logging

from telegram import (
    Update, 
    KeyboardButton, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove,
)
from telegram.ext import (
    CallbackContext, 
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters,
)

from cinnabot import Command, Conversation

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# '/weather: 2h weather forecast',
# '/spaces: list of space bookings',
# '/feedback: to give feedback',
# '/laundry: to check washer and dryer availability in cinnamon',

class PublicBus(Command):

    command = 'publicbus'
    help_text = 'public bus timings for bus stops around your location'
    help_full = ''

    def callback(self, update: Update, context, CallbackContext):
        return

class NUSBus(Conversation):

    command = 'nusbus'
    help_text = 'NUS bus timings for bus stops around your location.'
    help_full = (
        '/nusbus: NUS bus timings for bus stops around your location.'
    )

    # States
    GET_BUS_TIMING = 0

    # Class helper variables
    KEYBOARD = [
        ['Utown', 'Science'],
        ['Arts', 'Comp'],
        ['CenLib', 'Biz'],
        ['Law', 'Yih/Engin'],
        ['MPSH', 'KR-MRT'],
    ]

    TAGS = [button for row in KEYBOARD for button in row]

    KEYBOARD_PATTERN = '^(' + '|'.join(TAGS) + ')$' # Regex to match all valid replies

    @property
    def handler(self):
        return ConversationHandler(
            entry_points = [CommandHandler(self.command, self.entry)],
            states = {
                self.GET_BUS_TIMING: [

                ],
            },
            fallbacks = [
                CommandHandler('cancel', self.cancel),
                MessageHandler(Filters.text, self.error),
            ],
        )

    def entry(self, update: Update, context: CallbackContext):
        text = "🤖: Where are you?"
        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton('here', request_location=True)], *self.KEYBOARD],
            resize_keyboard = True,
            one_time_keyboard = True,
            selective = True,
        )
        update.message.reply_text(text, reply_markup=reply_markup)
        return self.GET_BUS_TIMING
    
    def error(self, update: Update, context: CallbackContext):
        """Alerts the user of a bad reply and continues trying to parse user replies."""
        logger.info('error')
        text = f'🤖: "{update.message.text}" not recognized'
        update.message.reply_text(text)
        return self.GET_BUS_TIMING

    def get_bus_timing(self, update: Update, context: CallbackContext):
        """Ends the user flow by sending a message with the desired resources and removing the keyboard."""
        logger.info('get_resources')
        text = '🤖: Link this to firebase! The current json solution is not the best ):'
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    def cancel(self, update: Update, context: CallbackContext):
        """Ends the user flow by removing the keyboard."""
        logger.info('cancel')
        text = f'🤖: Function /{self.command} cancelled!'
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

class NUSMap(Command):

    command = 'map'
    help_text = 'to get a map of NUS if you\'re lost!'
    help_full = ''
    
    def callback(self, update: Update, context, CallbackContext):
        return
