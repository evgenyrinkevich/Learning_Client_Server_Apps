import socket
import sys
import json
from common.settings import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


def process_client_message(message):
    """
    Checks if message is in correct format and returns response
    """
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
            print(f'Assigned server port to {listen_port}')
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print(f"Please specify port number after '-p' parameter. Assigning default value - {DEFAULT_PORT}")
        listen_port = DEFAULT_PORT
    except ValueError:
        print('Port number should be in 1024-65535 range')
        sys.exit(1)

    # loading IP from command line
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
            print('Assigned server address to ""')
    except IndexError:
        print("Please specify IP after '-a' parameter. Assigning default value - ''")
        listen_address = ''

    # socket init
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    print(f'Listening at {listen_address}:{listen_port}')
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client, f'sent by {client_address}')
            response = process_client_message(message_from_client)
            send_message(client, response)
        except (ValueError, json.JSONDecodeError):
            print('Incorrect message from client!')
            client.shutdown()
            client.close()


if __name__ == '__main__':
    main()
