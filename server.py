import select
import socket
import sys
import json
import logging
import argparse
import time

from common.settings import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, \
    DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
import project_logs.config.config_server
from decorators import log

logger = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    """
    Checks if message is in correct format and returns response
    """
    logger.debug(f'Processing message {message} from client')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def arg_parser():
    """Command line args parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        logger.critical(
            f'Wrong server port number- {listen_port}. Available addresses: 1024 - 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    # loading port number from command line
    listen_address, listen_port = arg_parser()

    logger.info(f'Server is up. Port for connections: {listen_port}, address, '
                f'server is listening to: {listen_address if listen_address else "any"}')

    # socket init
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.3)
    transport.listen(MAX_CONNECTIONS)

    # clients and messages lists
    clients = []
    messages = []

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            logger.info(f'Connection with {client_address} is established')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    logger.info(f'Client {client_with_message.getpeername()} disconnected from the server.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    logger.info(f'Client {waiting_client.getpeername()} disconnected from the server.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
