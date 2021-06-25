import sys
import string
import unittest
import mariadb
import random

sys.path.append('../JudgeInterface')

from JudgeInterface.users import UsersInterface
from JudgeInterface.lib.db import Connection


class UsersInterfaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = Connection()
        self.cur = self.conn.cursor()
        self.ui = UsersInterface(self.cur)        

    def test_create_a_user_with_no_args(self):
        with self.assertRaises(mariadb.IntegrityError) as e:
            self.ui.create(**{})

        self.conn.commit()
        self.conn.close()

    def test_create_a_user_with_un_allowed_fields(self):
        with self.assertRaises(AttributeError) as e:
            self.ui.create(**{
                "asouigyu": "asdiohgiyh"
            })

        self.conn.commit()
        self.conn.close()

        error_msg = e.exception
        self.assertEqual('{}'.format(error_msg), """{'asouigyu'} field(s) is(are) not allowed""")

    def test_create_a_user_with_args_both_un_allowed_and_allowed(self):
        with self.assertRaises(AttributeError) as e:
            self.ui.create(**{
                "password": "oasiduigy",
                "asouigyu": "asdiohgiyh",
                "email": "asjdiohgihj",
                "ojidhguyahs": "asdjihugyh",
                "username": "asojddsio"
            })

        self.conn.commit()
        self.conn.close()
        
        error_msg = e.exception
        self.assertIn('asouigyu', '{}'.format(error_msg))
        self.assertIn('ojidhguyahs', '{}'.format(error_msg))

    def test_create_a_user_with_args_allowed(self):
        letters = string.ascii_letters
        rand_string = ""
        for i in range(16):
            rand_string += random.choice(letters)
        
        context = self.ui.create(**{
            "password": "asdsadasd",
            "email": "lojpihogyuft",
            "username": rand_string
        })

        self.conn.commit()
        self.conn.close()

        self.assertRegex(str(context), r"^{'id': (\d+), 'username': '%s', 'email': 'lojpihogyuft'}$" % rand_string)

    def test_retrieve_a_user_with_no_args(self):
        user = self.ui.retrieve(2)
        self.assertEqual('{}'.format(user), "{'id': 2, 'username': 'mansukim', 'email': 'changed!!'}")

    def test_retrieve_a_user_that_not_exists(self):
        user = self.ui.retrieve(0)
        self.assertEqual('{}'.format(user), 'None')

    def test_retrieve_a_user_with_un_allowed_args(self):
        with self.assertRaises(AttributeError) as e:
            self.ui.retrieve(2, ['asjdihogu'])

        error_msg = e.exception
        self.assertEqual('{}'.format(error_msg), "{'asjdihogu'} field(s) is(are) not allowed")

    def test_retrieve_a_user_with_args_both_un_allowed_and_allowed(self):
        with self.assertRaises(AttributeError) as e:
            self.ui.retrieve(2, ['password', 'asdjihougi', 'email', 'username', 'id'])

        error_msg = e.exception

        self.assertIn('asdjihougi', '{}'.format(error_msg))
        self.assertIn('password', '{}'.format(error_msg))

    def test_retrieve_a_user_with_args_allowed(self):
        user = self.ui.retrieve(2, ['username', 'email', 'id'])
        self.assertEqual('{}'.format(user), "{'id': 2, 'username': 'mansukim', 'email': 'changed!!'}")

    def test_update_a_user_with_no_args(self):
        print('test_update_a_user_with_no_args')
        update_result = self.ui.update(2, **{})
        
        self.conn.commit()
        self.conn.close()

        self.assertEqual('{}'.format(update_result), 'None')

    def test_update_a_user_that_not_exists(self):
        # self.cur.rowcount: 0
        update_result = self.ui.update(0, **{
            "email": "iasudigyu"
        })
        
        self.conn.commit()
        self.conn.close()

        self.assertEqual('{}'.format(update_result), 'None')

    def test_update_a_user_with_un_allowed_args(self):
        with self.assertRaises(AttributeError) as e:
            update_result = self.ui.update(2, **{
                "asdjipohugyuh": "iasudigyu",
                "saodjihuigydf": "osiduigayu"
            })
        
        self.conn.commit()
        self.conn.close()

        error_msg = e.exception
        self.assertIn('asdjipohugyuh', '{}'.format(error_msg))
        self.assertIn('saodjihuigydf', '{}'.format(error_msg))

    def test_update_a_user_with_args_both_un_allowed_and_allowed(self):
        with self.assertRaises(AttributeError) as e:
            update_result = self.ui.update(2, **{
                "asdjipohugyuh": "iasudigyu",
                "password": "sdoajioj",
                "email": "OJIOHDjsa",
                "username": "dkojsiji",
                "saodjihuigydf": "osiduigayu"
            })
        
        self.conn.commit()
        self.conn.close()

        error_msg = e.exception
        self.assertIn('asdjipohugyuh', '{}'.format(error_msg))
        self.assertIn('username', '{}'.format(error_msg))
        self.assertIn('saodjihuigydf', '{}'.format(error_msg))

    def test_update_a_user_with_args_allowed(self):
        # self.cur.rowcount: 1
        update_result = self.ui.update(2, **{
            "password": "asodpjo",
            "email": "odasjiohibj"
        })

        self.assertEqual('{}'.format(update_result), "{'email': 'odasjiohibj'}")

if __name__ == '__main__':
    unittest.main()
