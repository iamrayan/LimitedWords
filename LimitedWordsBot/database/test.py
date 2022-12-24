from base import Base
import time


my_base = Base()

while True:
    id = input("id: ")

    my_base.db.collection('users').document(id).set(
    {
        'lastpetactive': int(time.time() - 3600),
    },
    merge=True)