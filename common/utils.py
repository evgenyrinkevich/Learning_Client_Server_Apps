import json

from decorators import log
from .settings import MAX_PACKAGE_LENGTH, ENCODING


@log
def get_message(client):
    """
    Gets message from client in bytes. Returns dict
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """
    Converts message from dict to bytes and sends it to sock
    """
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
