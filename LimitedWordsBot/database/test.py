from base import Base

my_base = Base()

while True:
    id = input("id: ")

    my_base.db.collection('users').document(id).set({}, merge=True)