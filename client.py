import sys
import json
import socket
import time
from common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

from exceptions import ReqFieldMissingError
import logging
import project_logs.config.config_client


logger = logging.getLogger('client')


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


def main():

    # loading IP and port number from command line
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            logger.critical('Port number should be from 1024 to 65535')
            sys.exit(1)
    except IndexError:
        logger.info(f'Assigning DEFAULT_IP_ADDRESS: {DEFAULT_IP_ADDRESS}, DEFAULT_PORT: {DEFAULT_PORT}')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        logger.critical('Port number should be from 1024 to 65535')
        sys.exit(1)

    logger.info(f'Client is up: server address: {server_address}, port: {server_port}')
    # socket init
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)

        answer = process_answer(get_message(transport))
        logger.info(f'Received response from server: {answer}')
    except json.JSONDecodeError:
        logger.info('Couldn\'t decode message from the server!')
    except ReqFieldMissingError as err:
        logger.critical(f'Required field is missing: {err.missing_field}')
    except ConnectionRefusedError:
        logger.critical(f'Connection to server {server_address}:{server_port} refused!')


if __name__ == '__main__':
    main()

