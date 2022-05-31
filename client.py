import sys
import json
import socket
import threading
import time
import argparse
import logging

from common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT, EXIT, DESTINATION
from common.utils import get_message, send_message
from exceptions import ReqFieldMissingError
import project_logs.config.config_client
from decorators import Log

logger = logging.getLogger('client')


@Log()
def message_from_server(sock, my_username):
    """
    Handles messages from server
    """
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nUser {message[SENDER]} sent: \n{message[MESSAGE_TEXT]}\nEnter a command: ')
                logger.info(f'User {message[SENDER]} sent: \n{message[MESSAGE_TEXT]}')
            else:
                logger.error(f'Bad message from the server: {message}')
        except json.JSONDecodeError:
            logger.info('Couldn\'t decode message from the server!')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
            logger.critical(f'Connection with the server lost!')
            break


@Log()
def create_message(sock, account_name='Guest'):
    """
    Функция запрашивает кому отправить сообщение и само сообщение,
    и отправляет полученные данные на сервер
    :param sock:
    :param account_name:
    :return:
    """
    to_user = input('Enter client\'s name: ')
    message = input('Enter your message: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    logger.debug(f'Message dict is created: {message_dict}')
    try:
        send_message(sock, message_dict)
        logger.info(f'Message sent to {to_user}')
    except:
        logger.critical('Connection with the server lost!')
        sys.exit(1)


@Log()
def create_presence(account_name='Guest'):
    """
    Generates request indicating that client is present
    """
    logger.debug(f'{PRESENCE} message is formed for {account_name} user')
    return {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }


@Log()
def process_answer(message):
    """
    Processes response from the server
    """
    logger.debug(f'Processing {message} message from server')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@Log()
def arg_parser():
    """
    Parses command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Wrong client\'s port number: {server_port}. Available addresses 1024 - 65535. '
            f'Client is shutting down.')
        sys.exit(1)

    return server_address, server_port, client_name


@Log()
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@Log()
def user_interactive(sock, username):
    """Interacts with the client"""
    print_help()
    while True:
        command = input('Enter a command: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Closing connection...')
            logger.info('Terminating by client\'s request.')
            time.sleep(0.5)
            break
        else:
            print('Wrong command, try again. help - available commands.')


def print_help():
    print('Supported commands:')
    print('message - send a message. Specify text and recipient later.')
    print('help - available commands')
    print('exit - exits the program')


def main():
    # loading IP and port number from command line
    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    logger.info(f'Client is up: server address: {server_address}, port: {server_port}, name: {client_name}')
    # socket init
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_answer(get_message(transport))
        logger.info(f'Received response from server: {answer}')
        print(f'Connection the server is established.')
    except json.JSONDecodeError:
        logger.info('Couldn\'t decode message from the server!')
        sys.exit(1)
    except ReqFieldMissingError as err:
        logger.critical(f'Required field is missing: {err.missing_field}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(f'Connection to server {server_address}:{server_port} refused!')
        sys.exit(1)
    else:
        # If connection with the server is established
        # starting receiving messages
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # interacting with the client
        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        logger.debug('Threads are up.')

        # Watchdog
        # if any of the threads is down - exiting by breaking out of loop
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
