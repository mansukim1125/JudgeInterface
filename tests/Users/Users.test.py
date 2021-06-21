from JudgeInterface.users import UsersInterface
from JudgeInterface.lib.db import Connection

conn = Connection()
cur = conn.cursor()

u = UsersInterface(cur)

users = u.retrieve(fields=['id', 'email', 'username'])
print(users)


conn.commit()
conn.close()
