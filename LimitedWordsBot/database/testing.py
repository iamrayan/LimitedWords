import base


my_base = base.Base()


print(my_base.db.collection('users').document("732876803412328499").get().to_dict( ))
print("Hello")