import unittest
from client import create_presence, process_answer
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE


class TestClient(unittest.TestCase):

    def test_create_presence(self):
        result = create_presence()
        result[TIME] = '1652427234.1710649'

        self.assertEqual(result, {
            ACTION: PRESENCE,
            TIME: '1652427234.1710649',
            USER: {
                ACCOUNT_NAME: 'Guest'
            }})

    def test_create_presence_account_name_set(self):
        result = create_presence('account_name')
        result[TIME] = '1652427234.1710649'

        self.assertEqual(result, {
            ACTION: PRESENCE,
            TIME: '1652427234.1710649',
            USER: {
                ACCOUNT_NAME: 'account_name'
            }})

    def test_process_answer_no_response(self):
        self.assertRaises(ValueError, process_answer, {'wrong_msg': 1})

    def test_process_answer_bad_request(self):
        self.assertEqual('400: Bad Request', process_answer({
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }))

    def test_process_answer_ok(self):
        self.assertEqual('200: OK', process_answer({RESPONSE: 200}))


if __name__ == '__main__':
    unittest.main()
