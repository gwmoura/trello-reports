import os
from dotenv import load_dotenv

load_dotenv()

TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
TRELLO_APP_TOKEN = os.getenv('TRELLO_APP_TOKEN')
BOARD_ID = os.getenv('BOARD_ID')
