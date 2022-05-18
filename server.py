import socket
import sys
import json
from common.settings import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
import project_logs.config.config_server


logger = logging.getLogger('server')


def process_client_message(message):
    """
    Checks if message is in correct format and returns response
    """
    logger.debug(f'Processing message {message} from client')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    # loading port number from command line
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            logger.critical('Port number should be from 1024 to 65535')
            sys.exit(1)

    except IndexError:
        logger.info(f"Port number after '-p' parameter is not specified. Assigning default value - {DEFAULT_PORT}")
        listen_port = DEFAULT_PORT
    except ValueError:
        logger.critical('Port number should be from 1024 to 65535')
        sys.exit(1)

    # loading IP from command line
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        logger.info("IP after '-a' parameter not specified. Assigning default value - ''")
        listen_address = ''

    logger.info(f'Server is up. Port for connections: {listen_port}, address, '
                f'server is listening to: {listen_address if listen_address else "any"}')

    # socket init
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        logger.info(f'Connection with {client_address} is established')
        try:
            message_from_client = get_message(client)
            logger.info(f'Message {message_from_client} received from client')
            response = process_client_message(message_from_client)
            logger.info(f'Response {response} to client is formed')
            send_message(client, response)
            logger.info(f'Connection with {client_address} is closed')
            client.close()
        except json.JSONDecodeError:
            logger.error(f'Couldn\'t decode message from {client_address}! Closing connection')
            client.close()
        except ValueError:
            logger.error(f'Bad data from {client_address}! Closing connection')
            client.close()


if __name__ == '__main__':
    main()
