import sys
import json
import socket
import time
import argparse
import logging

from common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from common.utils import get_message, send_message
from exceptions import ReqFieldMissingError
import project_logs.config.config_client
from decorators import Log

logger = logging.getLogger('client')


@Log()
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Message from {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        logger.info(f'Message from {message[SENDER]}:\n{message[MESSAGE_TEXT]} received')
    else:
        logger.error(f'Wrong message from the server: {message}')


@Log()
def create_message(sock, account_name='Guest'):
    """
    Manages messages from client
    """
    message = input('Enter message (\'!!!\' to quit): ')
    if message == '!!!':
        sock.close()
        logger.info('Exiting by client\'s request.')
        print('See you soon!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    logger.debug(f'Message is created: {message_dict}')
    return message_dict


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
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        logger.critical(f'Wrong client port number: {server_port}. '
                        f'Available addresses: 1024 - 65535. Connection is closed.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        logger.critical(f'Wrong client\'s mode: {client_mode}, available modes: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    # loading IP and port number from command line
    server_address, server_port, client_mode = arg_parser()

    logger.info(f'Client is up: server address: {server_address}, port: {server_port}, mode: {client_mode}')
    # socket init
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_answer(get_message(transport))
        logger.info(f'Received response from server: {answer}')
        print(f'Connection the server is established.')
    except json.JSONDecodeError:
        logger.info('Couldn\'t decode message from the server!')
        sys.exit(1)
    except ReqFieldMissingError as err:
        logger.critical(f'Required field is missing: {err.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        logger.critical(f'Connection to server {server_address}:{server_port} refused!')
        sys.exit(1)
    else:
        # Connection is established
        # Start sending/receiving messages
        if client_mode == 'send':
            print('Mode: send.')
        else:
            print('Mode: receive.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Connection with server {server_address} was lost.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError, json.JSONDecodeError):
                    logger.error(f'Connection with server {server_address} was lost.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
