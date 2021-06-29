import unittest
import sys
sys.path.append('../JudgeInterface')

from JudgeInterface.users import UsersInterface
from JudgeInterface.lib.db import Connection


class RetrieveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = Connection()
        self.cur = self.conn.cursor()
        self.ui = UsersInterface(self.cur)

    def test_retrieve_with_unknown_projection_fields(self):
        with self.assertRaises(AttributeError) as e:
            self.ui.perform_retrieve(None, ['asdjihui'])

        error_msg = e.exception
        self.assertEqual('{}'.format(error_msg), "{'asdjihui'} field(s) is(are) not allowed")

    def test_retrieve_with_no_projection_fields(self):
        print('test_retrieve_with_no_projection_fields')
        query = self.ui.perform_retrieve()
        print(query)
        # self.assertEqual(query, """SELECT id, username, email\nFROM judge.USERS""")

    def test_retrieve_with_unknown_selection_fields(self):
        with self.assertRaises(AttributeError) as e:
            self.ui.perform_retrieve(None, ['username'], **{
                "asjidho": "aosjdioh"
            })
        
        error_msg = e.exception
        self.assertEqual('{}'.format(error_msg), "{'asjidho'} field(s) is(are) not allowed")

    def test_retrieve_with_no_selection_fields(self):
        print('test_retrieve_with_no_selection_fields')
        query = self.ui.perform_retrieve(None, ['username'])
        print(query)
        # self.assertEqual(query, """SELECT username\nFROM judge.USERS""")

    def test_retrieve_with_selection_fields(self):
        print('test_retrieve_with_selection_fields')
        query = self.ui.perform_retrieve(None, ['username'], **{
            "email": "changed_email1",
            "id": 2
        })
        print(query)
        # self.assertEqual(query, """SELECT username\nFROM judge.USERS\nWHERE id = ?, email = ?""")

    def test_retrieve_with_id(self):
        print('test_retrieve_with_id')
        result = self.ui.perform_retrieve(None, ['username'], **{
                "id": 2
            }
        )[0]
        print(result)


if __name__ == '__main__':
    unittest.main()
