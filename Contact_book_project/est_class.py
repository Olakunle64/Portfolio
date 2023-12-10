#!/usr/bin/python3

"""test the ContactBook class"""

from models.Contact_Book import ContactBook

name = "olakunle"
number = "07062869135"
obj = ContactBook(number)
#obj.phone_number = "07062869135"
obj.name = "olakunle"
print(obj)
obj.save()
print("\n================================================\n")
print(obj.to_dict())
print("\n================================================\n")
obj2 = ContactBook(obj.to_dict())
print(obj)
print(obj is obj2)
