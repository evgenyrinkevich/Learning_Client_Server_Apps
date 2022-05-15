import unittest
from server import process_client_message
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE


class TestServer(unittest.TestCase):

    def setUp(self) -> None:
        self.resp_ok = {RESPONSE: 200}
        self.resp_failed = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    def test_no_action(self):
        self.assertEqual(process_client_message(
            {TIME: '1652427234.1710649', USER: {ACCOUNT_NAME: 'Guest'}}),
            self.resp_failed)

    def test_wrong_action(self):
        self.assertEqual(process_client_message(
            {ACTION: 'not_presence', TIME: '1652427234.1710649', USER: {ACCOUNT_NAME: 'Guest'}}),
            self.resp_failed)

    def test_no_time(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}),
            self.resp_failed)

    def test_no_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1652427234.1710649'}),
            self.resp_failed)

    def test_wrong_user_account_name(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1652427234.1710649', USER: {ACCOUNT_NAME: 'not_guest'}}),
            self.resp_failed)

    def test_ok(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1652427234.1710649', USER: {ACCOUNT_NAME: 'Guest'}}),
            self.resp_ok)


if __name__ == '__main__':
    unittest.main()
