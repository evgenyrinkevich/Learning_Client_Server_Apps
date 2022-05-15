import json
import unittest
from unittest import mock

from common.utils import get_message, send_message
from common.settings import RESPONSE, ERROR, ENCODING


class TestUtils(unittest.TestCase):

    def test_send_message(self):
        """
        Mocks a socket and checks that function send_message sends message to the socket in correct format -
        python dict -> JSON formatted str -> bytes
        """
        with mock.patch('socket.socket') as mock_socket:
            send_message(mock_socket, {f'{RESPONSE}': 200})
            json_message = json.dumps({f'{RESPONSE}': 200})
            encoded_message = json_message.encode(ENCODING)
            mock_socket.send.assert_called_with(encoded_message)

    def test_get_message_error(self):
        with mock.patch('socket.socket') as mock_socket:
            with self.assertRaises(ValueError):
                mock_socket.recv.return_value = b'not_a_dict'
                get_message(mock_socket)

    def test_get_message_ok(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.recv.return_value = b'{"response": 200}'
            self.assertEqual(get_message(mock_socket), {f'{RESPONSE}': 200})

    def test_get_message_failed(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.recv.return_value = b'{"response": 400,"error": "Bad Request"}'
            self.assertEqual(get_message(mock_socket), {
                f'{RESPONSE}': 400,
                f'{ERROR}': 'Bad Request'
            })


if __name__ == '__main__':
    unittest.main()
