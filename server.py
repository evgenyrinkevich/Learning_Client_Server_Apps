import select
import socket
import sys
import logging
import argparse

from common.settings import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, \
    DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_200, RESPONSE_400, DESTINATION, EXIT
from common.utils import get_message, send_message
import project_logs.config.config_server
from decorators import log

logger = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client, clients, names):
    """
    Checks that message is in correct format and sends response if needed
    """
    logger.debug(f'processing a client\'s message : {message}')
    # if presence message
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'This username is already taken!'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    # if message
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    # if client is exiting
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    # bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Bad request!'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    """
    Sends message to the client
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        logger.info(f'Message sent to {message[DESTINATION]} from {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        logger.error(
            f'User {message[DESTINATION]} is not available.')


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

    # A dict, containing users names and corresponding sockets
    names = dict()

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
                                           messages, client_with_message, clients, names)
                except:
                    logger.info(f'Client {client_with_message.getpeername()} disconnected from the server.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except:
                logger.info(f'Connection with {i[DESTINATION]} is lost!')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
