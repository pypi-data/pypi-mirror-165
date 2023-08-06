""" Константы проекта """

import logging

# сокет
DEFAULT_PORT = 7777
DEFAULT_IP_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 5
MAX_PACKET_LENGTH = 1024
ENCODING = 'utf-8'
CONNECTION_TIMEOUT = 0.5
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG
# Конфигурационный файл сервера:
SERVER_CONFIG = 'server.ini'

# протокол JIM
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'msg'
MESSAGE_TEXT = 'message'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
LIST_INFO = 'data_list'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'


# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202, LIST_INFO: None}
#
RESPONSE_205 = {RESPONSE: 205}
# 400
RESPONSE_400 = {RESPONSE: 400, ERROR: None}
# 511
RESPONSE_511 = {RESPONSE: 511, DATA: None}